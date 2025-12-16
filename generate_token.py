import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

# Configuration from your .env
API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")


def get_token():
    token = api.AccessToken(API_KEY, API_SECRET) \
        .with_identity("human-user") \
        .with_name("Human") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room="my-first-room",
        ))
    
    return token.to_jwt()


if __name__ == "__main__":
    jwt = get_token()
    print(f"\nGenerated Token for room 'my-first-room':\n\n{jwt}\n")
    print("Use this token at: https://meet.livekit.io/custom?liveKitUrl=ws://localhost:7880&token=<PASTE_TOKEN_ABOVE>")
