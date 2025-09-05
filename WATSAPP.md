# AI Video WhatsApp Bot

## 📌 Overview
This project implements a **WhatsApp bot** using **FastAPI** and **Twilio’s WhatsApp API**.  
The bot allows users to generate **AI-powered videos** by simply sending a topic via WhatsApp.  

It integrates with the **Replicate API (minimax/video-01 model)** to generate videos from text prompts, and responds with both an acknowledgement and the video link.

---

## 🚀 How to Use
1. Save the Twilio sandbox number in your contacts:  
   `whatsapp:+14155238886`

2. Join the Twilio WhatsApp sandbox by sending this message : join to-example.

3. Send a message with your desired topic. Example:  solar system

4. You’ll instantly receive an acknowledgement:  
✅ Got it! Generating your AI video, please wait...

5. Once the video is generated, you’ll receive the video file directly in WhatsApp.

---

## 📜 Commands
- `/help` → Shows usage instructions.  
- `/about` → Information about the bot.  
- `/example` → Example prompts for quick testing.  
- `<topic>` → Directly generate a video from the given topic.

  ---

## 🔑 API Key Handling
- By default, the bot uses the environment variable: `API_TOKEN`.  
- If a user includes `key:<your_api_key>` in their message, the bot will use their provided key instead.  

---

## 🎥 Fallback Video
If AI video generation fails due to errors or API issues, the bot responds with a fallback video:  
👉 [Fallback Video](https://files.catbox.moe/m0fcuk.mp4)

This ensures the user always receives some video output.

---

## ⚙️ Approach
1. **Framework** → FastAPI for handling webhooks & routes.  
2. **Messaging** → Twilio WhatsApp API for sending & receiving messages.  
3. **AI Model** → Replicate minimax/video-01 model for video generation.  
4. **Background Flow**:
   - Immediate acknowledgement via `resp.message`
   - Background task fetches video & delivers via Twilio.  
5. **Error Handling**:
   - Catches exceptions during video generation.  
   - Returns fallback video in failure cases.  

---

## ✨ Features
✔️ Generate AI video from any text topic  
✔️ Instant acknowledgement messages  
✔️ Supports commands (`/help`, `/about`, `/example`)  
✔️ Custom API key support from user input  
✔️ Fallback video when generation fails  
✔️ FastAPI + Twilio integration ready for deployment  
- `<topic> key:<your_api_key>` → Generate a video using your **custom Replicate API key**.  

Example:  
