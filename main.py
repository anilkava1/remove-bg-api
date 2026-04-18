import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAM bachane ke liye lighter model (u2netp) use karenge
# 'u2netp' is small and fast for free servers
session = new_session("u2netp") 

@app.get("/")
async def root():
    return {"status": "online"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        input_image = await file.read()
        
        # Session pass karna zaroori hai taki baar-baar model load na ho
        output_bytes = remove(input_image, session=session)
        
        return Response(content=output_bytes, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Render default port 10000 use karta hai
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)