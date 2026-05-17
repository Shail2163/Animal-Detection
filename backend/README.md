# Backend - YOLO Object Detection API

This is a FastAPI-based backend service for YOLO object detection.

## Project Structure

`
backend/
 app/
   main.py              # FastAPI app
   detection.py         # YOLO detection logic
   config.py            # Configuration
   __init__.py          # Package init
 storage/
   uploads/             # Uploaded images
   results/             # Detection results  
   models/              # YOLO models
 venv/                   # Virtual environment
 requirements.txt        # Python dependencies
 .env                    # Environment variables
 README.md              # This file
`

## Setup

1. Create and activate virtual environment:
   `ash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   `

2. Install dependencies:
   `ash
   pip install -r requirements.txt
   `

3. Run the application:
   `ash
   python -m app.main
   # or
   uvicorn app.main:app --reload
   `

## API Endpoints

- POST /predict - Upload an image for object detection
- GET / - Serve frontend (if available)

## Configuration

Edit .env file to modify:
- Model paths
- Confidence thresholds
- CORS origins
- Server settings
