# AI Object Detection Main Project

This repository contains the full-stack AI object detection project. The main application is split into a FastAPI backend and a React/Vite frontend.

## Project Structure

```text
D:\MAIN-WORK
+-- backend/             # FastAPI API for YOLO object detection
+-- frontend/            # React + Vite web interface
+-- storage/             # Shared upload/result storage
+-- AI-Prescription/     # Optional offline medical speech-to-text project
+-- run_model.py         # Model runner/helper script
+-- test_integration.py  # Backend/frontend connectivity test
+-- test_prediction.py   # API prediction test script
```

## Features

- Upload an image from the web interface.
- Send the image to the backend API.
- Run YOLOv11 object detection.
- Return detected objects, confidence scores, bounding boxes, and an annotated image.
- Store processed result images in `storage/results`.

## Tech Stack

### Frontend

- React 18
- Vite
- Axios
- Lucide React

### Backend

- Python
- FastAPI
- Uvicorn
- Ultralytics YOLO
- OpenCV
- Pillow
- NumPy

## Prerequisites

Install these before running the project:

- Python 3.9 or newer
- Node.js 16 or newer
- npm

## Backend Setup

Open a terminal in the project root:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

The backend runs at:

```text
http://localhost:8000
```

Useful backend routes:

```text
GET  /          API information
GET  /health    Health check
POST /predict   Upload an image for object detection
GET  /docs      FastAPI Swagger documentation
```

## Frontend Setup

Open a second terminal in the project root:

```bash
cd frontend
npm install
npm run dev
```

The frontend usually runs at:

```text
http://localhost:5173
```

If Vite chooses another port, use the URL shown in the terminal.

## Running The Full App

1. Start the backend from `backend/`.
2. Start the frontend from `frontend/`.
3. Open the frontend URL in your browser.
4. Upload an image.
5. View the detected objects and annotated result image.

## Testing

With the backend running, you can run:

```bash
python test_integration.py
```

To test prediction with a local image, update the image path inside `test_prediction.py`, then run:

```bash
python test_prediction.py
```

## Storage Folders

The app uses these folders for uploaded and processed files:

```text
backend/storage/uploads/
backend/storage/results/
storage/uploads/
storage/results/
```

Result images are saved with names like:

```text
detected_1772171114.jpg
```

## Optional: AI-Prescription Module

The `AI-Prescription/` folder is a separate offline medical prescription speech-to-text project using Vosk.

To run it:

```bash
cd AI-Prescription
pip install -r requirements.txt
python main.py
```

See `AI-Prescription/README.md` for its full setup instructions.

## Notes

- The frontend expects the backend API at `http://localhost:8000`.
- The backend loads the YOLO model on startup.
- The first backend startup may take longer because model files may need to be downloaded or loaded.
- Keep large generated files, virtual environments, and dependency folders out of Git.
