from fastapi import FastAPI,Form, Response
import uvicorn
import replicate
import time
from pydantic import BaseModel
import os
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests
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
    return {"response":"ok"}

class VidRequest(BaseModel):
    input:str
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


ACCOUNT_SID = os.getenv('sid')
AUTH_TOKEN = os.getenv('token')
TWILIO_WHATSAPP_NUMBER = os.getenv('number')  # Sandbox number
#secret : pPfx6VMyfUDQIEPU73g1aeIe1fWpzAaq
client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.post("/webhook")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    """
    This endpoint handles incoming WhatsApp messages.
    """

    user_msg = Body.strip()
    from_number = From
    resp = MessagingResponse()
    if user_msg.lower()=='/help':
        resp.message("✅ Usage:\n\n"
                     "1. Just type the topic: `solar system`\n"
                     "2. Or include your API key: `solar system key: abc123`\n")
        return Response(content=str(resp), media_type="application/xml")
    elif user_msg.lower() == '/about':
        resp = MessagingResponse()
        resp.message(
            "🤖 *About AI Video Bot*\n\n"
            "I generate short AI-powered videos based on any topic you send me! 🎬\n\n"
            "✅ *How to use:*\n"
            "1. Just type a topic → Example: `solar system`\n"
            "2. Or include your API key → Example: `solar system key:abc123`\n\n"
            "⚡️ I’ll reply with a video link once it’s ready!"
        )
        return Response(content=str(resp), media_type="application/xml")
    elif user_msg.lower() == '/example':
        resp = MessagingResponse()
        resp.message(
            "📌 *Example Prompts:*\n\n"
            "1️⃣ `solar system`\n"
            "2️⃣ `history of the internet`\n"
            "3️⃣ `black holes key:abc123`\n"
            "4️⃣ `AI in healthcare`\n"
            "5️⃣ `World War II overview`\n\n"
            "👉 Just type one of these, or send your own topic!"
        )
        return Response(content=str(resp), media_type="application/xml")
    # Step 1: Acknowledge message
    match = re.search(r"key\s*:\s*(\S+)", user_msg, re.IGNORECASE)
    api_key = match.group(1) if match else None
    
    topic = re.sub(r"key\s*:\s*\S+", "", user_msg, flags=re.IGNORECASE).strip()
    print(topic)
    print(api_key)
    if not topic:
        resp.message("⚠️ Please provide a topic. Example: `solar system key: abc123`")
        return Response(content=str(resp), media_type="application/xml")
    
    resp = MessagingResponse()
    resp.message("✅ Got it! Generating your AI video, please wait...")
    # Step 2: Call your video generation API
    try:
        video_data = generate_video(input_text=topic, api_key=api_key)
        video_url = video_data.get("url")
    
        if video_url:
            client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                to=from_number,
                body=f"🎬 Here’s your AI-generated video! :{video_url}",
            )
        else:
            client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                to=from_number,
                body="❌ Sorry, something went wrong while generating your video."
            )
    except Exception as e:
        print("Error:", e)
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=from_number,
            body="⚠️ Oops! There was an error processing your request."
        )

    return Response(content=str(resp), media_type="application/xml")
if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=10000)
