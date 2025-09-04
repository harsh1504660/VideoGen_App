from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests
import os
import uvicorn
import re
app = FastAPI()

# Twilio credentials (replace with your actual values)
ACCOUNT_SID = os.getenv('sid')
AUTH_TOKEN = os.getenv('token')
TWILIO_WHATSAPP_NUMBER = os.getenv('number')  # Sandbox number
#secret : pPfx6VMyfUDQIEPU73g1aeIe1fWpzAaq
client = Client(ACCOUNT_SID, AUTH_TOKEN)

VIDEO_API_URL = "https://videogen-app.onrender.com/generate"

@app.get('/health')
def root():
    return {'status':'ok'}
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
        payload = {"input": topic}
        if api_key:
            payload["api_key"] = api_key
        response = requests.post(VIDEO_API_URL, json=payload)
        print(response.json())
        video_data = response.json()
        video_url = video_data.get("url")

        if video_url:
            # Step 3: Send video to user via Twilio
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
    port = int(os.environ.get("PORT", 10001))  # use Render's PORT, fallback to 10001 locally
    uvicorn.run(app, host="0.0.0.0", port=port)





