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
def vedio(req:VidRequest):
    inputp = req.input
    start = time.time()
    output = replicate.Client(api_token=os.getenv('API_TOKEN')).run(

    "minimax/video-01",
    input={
        "prompt": inputp,
        "prompt_optimizer": True
    }
    )
    end = time.time() - start  # fixed time calculation

    # Extract URL if the output is a list
    print(output)
    video_url = output[0] if isinstance(output, list) else str(output)

    print(video_url)
    print(f"Time taken: {end} seconds")

    # Always return JSON-serializable types
    return {
        "url": video_url,
        "time_taken": end
    }

@app.post('/mock')
def mockk(req:VidRequest):
    time.sleep(10)
    return {
        "url":'https://replicate.delivery/xezq/kgwFkSaT4hLcDVvba2xD79O87uXKwn9HJIQSrHXwqOB2rtSF/tmpoezcjp53.mp4',
        "time_taken": '200.09689021110535'
    }

if __name__ == "__main__":
    uvicorn.run(app)