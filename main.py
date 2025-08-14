from fastapi import FastAPI
import uvicorn
import replicate
import time
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def root():
    return {"response":"ok"}

class VidRequest(BaseModel):
    input:str

@app.post('/generate')
def vedio(req: VidRequest):
    inputp = req.input
    start = time.time()

    try:
        client = replicate.Client(api_token=os.getenv('API_TOKEN'))
        output = client.run(
            "minimax/video-01",
            input={
                "prompt": inputp,
                "prompt_optimizer": True
            }
        )

        end = time.time() - start
        video_url = output[0] if isinstance(output, list) else str(output)

        return {
            "url": video_url,
            "time_taken": end
        }

    except Exception as e:
        print(f"Error generating video: {e}")
        # Fallback mock vediovideo
        fallback_url = "https://replicate.delivery/xezq/qqtm1akrG1bGBFAr7KqVaNuhU8SsoeZyTFrTgF2vJqxz5blKA/tmpxu_336z0.mp4"
        fallback_time = 0.0
        return {
            "url": fallback_url,
            "time_taken": fallback_time
        }

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=10000)