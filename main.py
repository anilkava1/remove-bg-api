import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
import io

# 1. FastAPI App Initialize karna
app = FastAPI(title="Remove BG API", description="AI based background removal API")

# 2. CORS Settings (Taki aapki website is API ko access kar sake)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Real project mein yaha apni website ka link dalein
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Home Route (Checking ke liye)
@app.get("/")
async def root():
    return {"status": "success", "message": "API is running. Use /docs for testing."}

# 4. Background Removal Endpoint
@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    # Check karein ki file image hi hai
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Image data read karna
        input_image = await file.read()
        
        # Background remove karna (AI processing)
        output_bytes = remove(input_image)
        
        # Processed image ko PNG format mein wapas bhejna
        return Response(content=output_bytes, media_type="image/png")
    
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"status": "error", "message": str(e)}
        )

# 5. Server run karne ke liye logic
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)