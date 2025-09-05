# 🎥 Text-to-Video Generator (Replicate API + FastAPI + Frontend UI)

Turn your ideas into AI-generated videos in just a few clicks!  
This project uses the **Replicate API** (with the `minimax/video-01` model) to generate short videos from text prompts.  
It comes with a **FastAPI backend** and a **beautiful, interactive frontend**.

---

## 🚀 Live Demo
🔗 [Live Demo Here](https://video-gen-app.vercel.app/)  

---

## 📖 Project Overview
This application allows users to:
- Enter a **custom text prompt** describing the video they want.
- Select from **predefined demo prompts** for quick generation.
- Optionally **enter their own Replicate API key** for generation.
- Watch the generated video directly in the browser.
- View **time taken** for generation (in minutes).
- Share videos instantly on **Twitter** and **LinkedIn**.

The backend handles the API requests to Replicate, and the frontend provides a smooth user experience with **loading animations**, **share buttons**, and **persistent last video storage**.

---

## ✨ Features
✅ **Text-to-Video Generation** – Using `minimax/video-01` on Replicate.  
✅ **Custom or Predefined Prompts** – Enter your own prompt or click a demo one.  
✅ **Optional API Key Input** – Use your own Replicate key or fallback to the server default.  
✅ **Loading Animation** – Beautiful spinning loader while the video is being created.  
✅ **Share Buttons** – Share your creation to Twitter & LinkedIn directly.  
✅ **Time Taken Display** – Shows how long generation took.  
✅ **Local Video Storage** – Remembers your last generated video in browser localStorage.  

---

## 🛠️ Getting your API KEY

### 1️⃣ Visit https://replicate.com/

### 2️⃣ Sign in with prefered account

### 3️⃣ Click on your profile and select API tokens

### 4️⃣ Use default or create new toekn
