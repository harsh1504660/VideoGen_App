from fastapi import FastAPI, Form, Response, BackgroundTasks
import uvicorn
import replicate
import time
from pydantic import BaseModel
import os
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {"response": "ok"}

class VidRequest(BaseModel):
    input: str
    api_key: Optional[str] = None

def generate_video(input: str, api_key: str = None):
    start = time.time()
    api_key = api_key or os.getenv("API_TOKEN")
    try:
        client = replicate.Client(api_token=api_key)
        output = client.run(
            "minimax/video-01",
            input={"prompt": input, "prompt_optimizer": True}
        )
        end = time.time() - start
        video_url = output[0] if isinstance(output, list) else str(output)
        return {"url": video_url, "time_taken": end}
    except Exception as e:
        print(f"Error generating video: {e}")
        return {"url": "https://files.catbox.moe/m0fcuk.mp4", "time_taken": 0.0}

@app.post('/generate')
def vedio(req: VidRequest):
    return generate_video(req.input, req.api_key)

# Twilio setup
ACCOUNT_SID = os.getenv('sid')
AUTH_TOKEN = os.getenv('token')
TWILIO_WHATSAPP_NUMBER = os.getenv('number')  # Sandbox number
client = Client(ACCOUNT_SID, AUTH_TOKEN)


@app.post("/webhook")
async def whatsapp_webhook(
    background_tasks: BackgroundTasks,
    From: str = Form(...),
    Body: str = Form(...)
):
    """
    Handles incoming WhatsApp messages.
    """

    user_msg = Body.strip()
    print("user msg:", user_msg)
    from_number = From

    resp = MessagingResponse()
    clean_msg = user_msg.lower().strip()

    # Handle commands
    if clean_msg == "/help":
        resp.message(
            "✅ Usage:\n\n"
            "1. Just type the topic: `solar system`\n"
            "2. Or include your API key: `solar system key: abc123`\n"
        )
        return Response(content=str(resp), media_type="application/xml")
    elif clean_msg == "/about":
        resp.message(
            "🤖 *About AI Video Bot*\nI generate AI videos based on any topic you send! 🎬\n"
            "Usage: `topic` or `topic key:YOUR_KEY`"
        )
        return Response(content=str(resp), media_type="application/xml")
    elif clean_msg == "/example":
        resp.message(
            "📌 Example Prompts:\n1️⃣ solar system\n2️⃣ history of the internet\n3️⃣ AI in healthcare"
        )
        return Response(content=str(resp), media_type="application/xml")

    # Extract topic and optional API key
    match = re.search(r"key\s*:\s*(\S+)", user_msg, re.IGNORECASE)
    api_key = match.group(1) if match else None
    topic = re.sub(r"key\s*:\s*\S+", "", user_msg, flags=re.IGNORECASE).strip()
    print("topic:", topic, "api_key:", api_key)

    if not topic:
        resp.message("⚠️ Please provide a topic. Example: `solar system key: abc123`")
        return Response(content=str(resp), media_type="application/xml")

    # Step 1: Immediate acknowledgement
    resp.message("✅ Got it! Generating your AI video, please wait...")

    # Step 2: Background task to generate video and send later
    def process_video():
        try:
            video_data = generate_video(input=topic, api_key=api_key)
            video_url = video_data.get("url")

            if video_url:
                print("twillio msg :", TWILIO_WHATSAPP_NUMBER)
                client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=from_number,
                    body="🎬 Here is your AI video:",
                    media_url=[video_url]
                )
            else:
                client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=from_number,
                    body="❌ Sorry, something went wrong while generating your video."
                )
        except Exception as e:
            print("Error in background task:", e)
            client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                to=from_number,
                body="⚠️ Something went wrong, please try again."
            )

    background_tasks.add_task(process_video)

    # Immediately respond with acknowledgement
    return Response(content=str(resp), media_type="application/xml")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
