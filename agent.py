import asyncio
import logging
from dotenv import load_dotenv
from livekit import api, rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents import voice
from livekit.plugins import openai, silero

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceAgent:
    """Voice Agent class to handle conversations"""
    
    def __init__(self):
        self.assistant = None
        
    async def create_assistant(self):
        """Create and configure the voice assistant"""
        
        # System instructions for the assistant
        instructions = (
            "You are a helpful voice assistant. Keep your responses concise "
            "and natural, as they will be spoken aloud. Engage in friendly "
            "conversation and answer questions to the best of your ability."
        )
        
        # Create the assistant with all components
        self.assistant = voice.Agent(
            instructions=instructions,
            vad=silero.VAD.load(),
            stt=openai.STT(model="whisper-1"),
            llm=openai.LLM(model="gpt-4o-mini"),
            tts=openai.TTS(voice="alloy"),
        )
        
        return self.assistant


async def entrypoint(ctx: JobContext):
    """Main entry point for the voice agent"""
    
    logger.info(f"Starting voice agent for room: {ctx.room.name}")
    
    # Connect to the room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info(f"Connected to room: {ctx.room.name}")
    
    # Create voice agent
    agent = VoiceAgent()
    assistant = await agent.create_assistant()
    
    # Create and start session
    session = voice.AgentSession()
    
    # Start the session with the assistant
    await session.start(assistant, room=ctx.room)
    logger.info("Voice assistant started")
    
    # Wait for a participant to join
    participant = await ctx.wait_for_participant()
    logger.info(f"Participant {participant.identity} joined the room")
    
    # Greet the participant
    await session.say(
        "Hello! I'm your voice assistant. How can I help you today?",
        allow_interruptions=True
    )
    
    logger.info("Agent is ready and listening...")


async def request_fnc(req: JobProcess):
    """Handle job requests"""
    logger.info(f"Received job request for room: {req.room.name}")
    await req.accept(entrypoint)


if __name__ == "__main__":
    # Run the worker
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            request_fnc=request_fnc,
        ),
    )
