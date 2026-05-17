import cv2
import numpy as np
from ultralytics import YOLO
import argparse
import os
from pathlib import Path

class YOLOv11Detector:
    def __init__(self, model_path='yolo11n.pt', conf_threshold=0.25, iou_threshold=0.45):
        """
        Initialize YOLOv11 detector
        
        Args:
            model_path (str): Path to YOLOv11 model weights
            conf_threshold (float): Confidence threshold for detections
            iou_threshold (float): IoU threshold for NMS
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        # COCO class names (80 classes)
        self.class_names = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
            'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
            'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
            'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
            'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
            'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
            'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
            'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
            'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
            'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
            'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
            'toothbrush'
        ]
        
        # Colors for bounding boxes (BGR format)
        self.colors = np.random.uniform(0, 255, size=(len(self.class_names), 3))

    def detect_image(self, image_path, output_path=None, show_result=False):
        """
        Detect objects in a single image
        
        Args:
            image_path (str): Path to input image
            output_path (str): Path to save output image (optional)
            show_result (bool): Whether to display the result
        
        Returns:
            Annotated image as numpy array (always returns an image, never None)
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image from {image_path}")
            # Return a blank image instead of None for API consistency
            return np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Run inference
        results = self.model(image, conf=self.conf_threshold, iou=self.iou_threshold)
        
        # Process results
        annotated_image = self.draw_detections(image, results[0])
        
        # Save result if output path is provided
        if output_path:
            cv2.imwrite(output_path, annotated_image)
            print(f"Result saved to: {output_path}")
        
        # Display result (only if explicitly requested)
        if show_result:
            cv2.imshow('YOLOv11 Detection', annotated_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return annotated_image

    def get_detections_info(self, results):
        """
        Extract detection information as JSON-serializable format
        
        Args:
            results: YOLO detection results
            
        Returns:
            List of detection dictionaries
        """
        detections = []
        
        # Handle both single result and list of results
        if isinstance(results, list):
            boxes = results[0].boxes if results else None
        else:
            boxes = results.boxes
        
        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                try:
                    x1, y1, x2, y2 = map(float, box.xyxy[0])
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    class_name = self.class_names[class_id] if class_id < len(self.class_names) else f"Class {class_id}"
                    
                    detections.append({
                        "class": class_name,
                        "class_id": class_id,
                        "confidence": round(confidence, 3),
                        "bbox": {
                            "x1": round(x1, 2), 
                            "y1": round(y1, 2), 
                            "x2": round(x2, 2), 
                            "y2": round(y2, 2),
                            "width": round(x2 - x1, 2),
                            "height": round(y2 - y1, 2),
                            "center_x": round((x1 + x2) / 2, 2),
                            "center_y": round((y1 + y2) / 2, 2)
                        }
                    })
                except Exception as e:
                    print(f"Error processing detection box: {e}")
                    continue
        
        return detections

    def detect_video(self, video_path, output_path=None, show_result=True):
        """
        Detect objects in video
        
        Args:
            video_path (str): Path to input video
            output_path (str): Path to save output video (optional)
            show_result (bool): Whether to display the result
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Error: Could not open video from {video_path}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Initialize video writer if output path is provided
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        print("Processing video... Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run inference
            results = self.model(frame, conf=self.conf_threshold, iou=self.iou_threshold)
            
            # Draw detections
            annotated_frame = self.draw_detections(frame, results[0])
            
            # Save frame if output path is provided
            if output_path:
                out.write(annotated_frame)
            
            # Display frame
            if show_result:
                cv2.imshow('YOLOv11 Video Detection', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        # Release resources
        cap.release()
        if output_path:
            out.release()
            print(f"Video saved to: {output_path}")
        cv2.destroyAllWindows()

    def detect_webcam(self, webcam_id=0):
        """
        Detect objects from webcam feed
        
        Args:
            webcam_id (int): Webcam device ID
        """
        cap = cv2.VideoCapture(webcam_id)
        
        if not cap.isOpened():
            print(f"Error: Could not open webcam with ID {webcam_id}")
            return
        
        print("Starting webcam detection... Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run inference
            results = self.model(frame, conf=self.conf_threshold, iou=self.iou_threshold)
            
            # Draw detections
            annotated_frame = self.draw_detections(frame, results[0])
            
            # Display frame
            cv2.imshow('YOLOv11 Webcam Detection', annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

    def draw_detections(self, image, results):
        """
        Draw bounding boxes and labels on image
        
        Args:
            image: Input image
            results: YOLO detection results
        
        Returns:
            Annotated image
        """
        annotated_image = image.copy()
        
        # Get detections
        boxes = results.boxes
        
        if boxes is not None:
            for box in boxes:
                try:
                    # Get coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Get class and confidence
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    
                    # Get class name
                    class_name = self.class_names[class_id] if class_id < len(self.class_names) else f"Class {class_id}"
                    
                    # Get color
                    color = self.colors[class_id].tolist()
                    
                    # Draw bounding box
                    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
                    
                    # Create label
                    label = f"{class_name}: {confidence:.2f}"
                    
                    # Get label size
                    (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                    
                    # Draw label background
                    cv2.rectangle(annotated_image, (x1, y1 - label_height - 10), (x1 + label_width, y1), color, -1)
                    
                    # Draw label text
                    cv2.putText(annotated_image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                
                except Exception as e:
                    print(f"Error drawing detection: {e}")
                    continue
        
        return annotated_image

    def print_detections(self, results):
        """
        Print detection results to console
        
        Args:
            results: YOLO detection results
        """
        # Handle both single result and list of results
        if isinstance(results, list):
            boxes = results[0].boxes if results else None
        else:
            boxes = results.boxes
        
        if boxes is not None and len(boxes) > 0:
            print(f"\nDetected {len(boxes)} objects:")
            for i, box in enumerate(boxes):
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = self.class_names[class_id] if class_id < len(self.class_names) else f"Class {class_id}"
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                print(f"{i+1}. {class_name}: {confidence:.2f} at [{x1}, {y1}, {x2}, {y2}]")
        else:
            print("No objects detected")

# Remove the standalone test code when using with FastAPI
# Keep only the class definition for API usage