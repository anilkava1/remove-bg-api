import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
import io
import os

app = FastAPI()

# CORS Fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global session variable
session = None

@app.get("/")
async def root():
    return {"status": "online", "info": "AI Background Remover is Ready"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    global session
    try:
        # Jab pehli image aaye tabhi model load karein (Memory bachane ke liye)
        if session is None:
            # main.py mein ye line check karein
             session = new_session("u2netp")
            
        input_image = await file.read()
        output_bytes = remove(input_image, session=session)
        
        return Response(content=output_bytes, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Port setup for Render
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)