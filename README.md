# Voice Assistant with LiveKit

Minimal Python voice assistant powered by LiveKit Agents, OpenAI speech + text models, and Silero VAD. The worker joins a LiveKit room, greets participants, and keeps a concise, natural, spoken conversation. A helper script issues access tokens for local testing.

## Prerequisites
- Python 3.11+ (matching the `venv` in this project)
- LiveKit server running locally or remotely
- OpenAI API access (for Whisper/STT, GPT/LLM, and TTS)
- `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` with `room_join` grants

## Setup
1) Create and activate a virtual environment (optional but recommended):
```
python -m venv .venv
.venv\Scripts\activate   # Windows
# or: source .venv/bin/activate  # macOS/Linux
```
2) Install dependencies:
```
pip install -r requirements.txt
```
3) Create a `.env` file in the project root:
```
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=ws://localhost:7880
OPENAI_API_KEY=your_openai_api_key
```
4) Start your LiveKit server (e.g., `docker run livekit/livekit-server` or via the installer) and ensure it is reachable at `LIVEKIT_URL`.

## Running the voice assistant worker
```
python agent.py
```
- The worker connects to the LiveKit room and waits for a participant.
- It greets the first participant and keeps listening/responding with speech.

## Generating a test token
```
python generate_token.py
```
- Outputs a JWT for room `my-first-room`.
- Use it with LiveKit Meet or your own client, e.g.:
  `https://meet.livekit.io/custom?liveKitUrl=ws://localhost:7880&token=<PASTE_TOKEN>`

## How it works
- `agent.py` builds a `voice.Agent` with Silero VAD, Whisper STT, GPT LLM, and OpenAI TTS.
- Auto-subscribes to audio, greets the first participant, then converses with concise, natural replies.
- `generate_token.py` issues a demo JWT using the LiveKit API credentials.

## Notes
- Keep responses short; the assistant is optimized for spoken dialogue.
- Protect your `.env` and never commit API keys.


