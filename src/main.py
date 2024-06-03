import torch
from ultralytics import YOLO
import cv2
import os
import time
import serial

model_n = YOLO("runs/detect/train6/weights/best.pt")
model_s = YOLO("runs/detect/train7/weights/best.pt")

colors ={
        'Cardboard': (38, 67, 109),
        'Glass': (28, 255, 0),
        'Metal': (128, 128, 128),
        'Paper':  (230, 216, 173),
        'Plastic': (0, 255, 255)
    }

def detect(model, frame , conf ):
    results = model(frame, conf = conf)
    
    detections = results[0].boxes.data
    
    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        label = model.names[int(cls)]
        #print (label)
        color = colors.get(label, (0, 0, 0))
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        text = f'{label}: {conf:.2f}'
        cv2.putText(frame, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
     


class CameraViewer:
    def __init__(self, camera,show_fps=True):
        self.cap = cv2.VideoCapture(camera)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 576)
        self.show_fps = show_fps
        self.frames = 0 
        self.start_time = time.time() 
        
    def resize_frame(self, frame):
        return cv2.resize(frame, (960, 540))
    
    def show_fps_on_frame(self, frame):
        # Calcular los FPS
        elapsed_time = time.time() - self.start_time
        fps = self.frames / elapsed_time

        # Mostrar los FPS en el frame
        cv2.putText(frame, f"FPS: {fps:.2f}", (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error en la cámara.")
                break
            
            frame = self.resize_frame(frame)
            
            if self.show_fps:
                self.frames += 1
                self.show_fps_on_frame(frame)
                
            detect(model_s , frame , conf= 0.65)
            
            cv2.imshow("CAMERA", frame)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'):
                break
            
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    viewer = CameraViewer(camera = 1, show_fps=True)
    viewer.run()