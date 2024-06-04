import torch
from ultralytics import YOLO
import cv2
import os
import time
import serial
from collections import deque

# Initialize serial communication with Arduino
arduino = serial.Serial('COM3', 9600, timeout=1)

# Load YOLO models for detection
model_n = YOLO("models\Final_model_n.pt")
model_s = YOLO("models\Final_model_s.pt")

# Define colors for each trash category
colors = {
    'Cardboard': (38, 67, 109),
    'Glass': (28, 255, 0),
    'Metal': (128, 128, 128),
    'Paper':  (230, 216, 173),
    'Plastic': (0, 255, 255)
}

# Initialize a queue to manage detections
detections_queue = deque()

# Function to detect objects in the frame using the YOLO model
def detect(model, frame, conf):
    
    results = model(frame, conf=conf)
    detections = results[0].boxes.data
    detected_labels = []
    
    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        label = model.names[int(cls)]
        color = colors.get(label, (0, 0, 0))
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        text = f'{label}: {conf:.2f}'
        cv2.putText(frame, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        detected_labels.append(label)
        
    return detected_labels

# Function to send the detected label to the Arduino
def send_label(label):
    commands = {
        "Plastic": "open_plastic",
        "Paper": "open_paper",
        "Glass": "open_glass",
        "Metal": "open_metal",
        "Cardboard": "open_cardboard"
    }
    command = commands.get(label, "")
    if command:
        arduino.write(f"{command}\n".encode())
        print(f"Sending command to Arduino: {command}")

# Class to handle the camera feed and display
class CameraViewer:
    def __init__(self, camera, show_fps=True):
        self.cap = cv2.VideoCapture(camera)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 576)
        self.show_fps = show_fps
        self.frames = 0
        self.start_time = time.time()
        
    def resize_frame(self, frame):
        return cv2.resize(frame, (960, 540))
    
    def show_fps_on_frame(self, frame):
        # Calculate and display FPS
        elapsed_time = time.time() - self.start_time
        fps = self.frames / elapsed_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Camera error.")
                break
            
            frame = self.resize_frame(frame)
            
            if self.show_fps:
                self.frames += 1
                self.show_fps_on_frame(frame)
                
            detected_labels = detect(model_s, frame, conf=0.65)
            
            # Add detections to the queue
            for label in detected_labels:
                detections_queue.append(label)

            # Process detections from the queue
            if detections_queue:
                current_label = detections_queue.popleft()
                send_label(current_label)
                
            # Show inference
            cv2.imshow("CAMERA", frame)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'):
                break
            
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    viewer = CameraViewer(camera=1, show_fps=True)
    viewer.run()
