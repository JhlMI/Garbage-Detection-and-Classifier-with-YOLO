import torch
from ultralytics import YOLO
import cv2
import os


model_n = YOLO("runs/detect/train6/weights/best.pt")
model_s = YOLO("runs/detect/train7/weights/best.pt")
