# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from PIL import Image
import io, asyncio, functools
import numpy as np
import cv2
import tempfile
import os
import base64
from model import YOLOv11Detector

app = FastAPI(title="AI Object Detection API")

# Dev CORS — restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create storage directories
os.makedirs("storage/uploads", exist_ok=True)
os.makedirs("storage/results", exist_ok=True)

# Global model variable
model = None

# --- Load model once at startup ---
@app.on_event("startup")
def load_model():
    global model
    print("Loading YOLOv11 model...")
    model = YOLOv11Detector(
        model_path='yolo11n.pt',
        conf_threshold=0.1,
        iou_threshold=0.45
    )
    print("✅ Model loaded successfully!")

# Synchronous inference helper (runs in a threadpool)
def run_inference(image_array: np.ndarray, save_result: bool = True):
    try:
        # Convert numpy array to BGR image for OpenCV
        image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # Save image temporarily
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            temp_image_path = tmp.name
            cv2.imwrite(temp_image_path, image_bgr)
        
        # Run detection - FIXED: Direct model inference instead of detect_image method
        results = model.model(temp_image_path, conf=model.conf_threshold, iou=model.iou_threshold)
        
        # Remove temp file
        os.remove(temp_image_path)
        
        if not results:
            raise Exception("No results from model")
        
        # Get detection results using the model's method
        detections = model.get_detections_info(results)
        
        # Load image for annotation
        annotated_image = model.draw_detections(image_bgr, results[0])
        
        # Save annotated image if requested
        result_path = None
        if save_result:
            import time
            result_filename = f"detected_{int(time.time())}.jpg"
            result_path = os.path.join("storage/results", result_filename)
            cv2.imwrite(result_path, annotated_image)
        
        # Convert annotated image to base64 for response
        _, buffer = cv2.imencode('.jpg', annotated_image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        h, w, c = annotated_image.shape
        return {
            "success": True,
            "detections": detections,
            "total_objects": len(detections),
            "image_info": {
                "height": int(h),
                "width": int(w),
                "channels": int(c)
            },
            "annotated_image": f"data:image/jpeg;base64,{img_base64}",
            "result_path": result_path
        }
        
    except Exception as e:
        print(f"Detection error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "detections": [],
            "total_objects": 0
        }

@app.get("/")
async def root():
    return {
        "message": "YOLOv11 Object Detection API",
        "status": "running",
        "endpoints": {
            "predict": "/predict - Upload image for object detection",
            "health": "/health - Health check",
            "docs": "/docs - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        arr = np.array(image)

        # Run inference in thread pool
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, functools.partial(run_inference, arr, True))
        
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/results/{filename}")
async def get_result_image(filename: str):
    """Serve processed images"""
    file_path = os.path.join("storage/results", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

# Serve static files for results (optional)
app.mount("/static", StaticFiles(directory="storage"), name="static")

# COMMENT OUT OR REMOVE THIS LINE DURING DEVELOPMENT
# Only enable this in production after building your frontend
# app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)