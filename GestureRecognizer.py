# Sample application to demonstrate hand recognition using Mediapipe to control a robot and save data in InfluxDB
# Author: Suyash Joshi
# License : MIT
# Copyright: InfluxData

import cv2

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import numpy as np
import time

from dotenv import load_dotenv
import os

from MotorController import MotorController  # Ensure this matches the filename
from InfluxDBWriter import InfluxDBWriter  # Import the InfluxDBWriter class

class GestureRecognizerApp:
  def __init__(self, model_path, motor_controller, influxdb_writer):
    self.model_path = model_path
    self.recognized_gesture = None
    self.confidence_score = None
    self.gesture_timestamp = 0
    self.gesture_display_duration = 2  # Display gesture for 2 seconds
    self.recognizer = self.create_recognizer()
    self.motor_controller = motor_controller
    self.influxdb_writer = influxdb_writer
    self.last_sent_gesture = None

  def create_recognizer(self):
    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = GestureRecognizerOptions(
      base_options=BaseOptions(model_asset_path=self.model_path),
      running_mode=VisionRunningMode.LIVE_STREAM,
      result_callback=self.print_result
    )
    return GestureRecognizer.create_from_options(options)

  def print_result(self, result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print(f"Result received at timestamp: {timestamp_ms}")
    print(f"Result type: {type(result)}")
    print(f"Gestures: {result.gestures}")

    self.recognized_gesture = None  # Reset recognized gesture for each new frame
    self.confidence_score = None  # Reset confidence score for each new frame
    self.gesture_timestamp = timestamp_ms  # Update timestamp of the recognized gesture

    if result.gestures:
      for gesture_group in result.gestures:
        if isinstance(gesture_group, list):
          for gesture in gesture_group:
            print(f"Individual gesture: {gesture}")
            if hasattr(gesture, 'category_name'):
              print(f'Category name: {gesture.category_name}, Score: {gesture.score}')
              self.recognized_gesture = gesture.category_name
              self.confidence_score = gesture.score
            elif hasattr(gesture, 'name'):
              print(f'Gesture: {gesture.name}, Confidence: {gesture.score}')
              self.recognized_gesture = gesture.name
              self.confidence_score = gesture.score

      if self.recognized_gesture != self.last_sent_gesture:
        self.influxdb_writer.write_gesture(self.recognized_gesture, timestamp_ms)
        self.last_sent_gesture = self.recognized_gesture
        self.motor_controller.send_gesture_to_motor_controller(self.recognized_gesture)
    else:
      print("No gestures detected in this frame")

  def run(self):
    cap = cv2.VideoCapture(0)  # Open the default camera
    while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
        print("Failed to capture frame")
        break

      current_time = time.time()
      frame_timestamp_ms = int(current_time * 1000)

      rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

      print(f"Processing frame at timestamp: {frame_timestamp_ms}")
      self.recognizer.recognize_async(mp_image, frame_timestamp_ms)

      # Always display the current recognized gesture (if any)
      if self.recognized_gesture:
        cv2.putText(frame, f'Current Gesture: {self.recognized_gesture}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

      # Display the last recognized gesture for a duration
      if self.recognized_gesture and (current_time * 1000 - self.gesture_timestamp) < self.gesture_display_duration * 1000:
        cv2.putText(frame, f'Confidence: {self.confidence_score * 100:.2f}%', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Timestamp: {self.gesture_timestamp}', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

      cv2.imshow('Gesture Recognition', frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cap.release()
    cv2.destroyAllWindows()

def main():
  
  load_dotenv()

  influxDB_url = os.getenv("influxDB_url")
  influxDB_token = os.getenv("influxDB_token")
  influxDB_org = os.getenv("influxDB_org")
  influxDB_bucket = os.getenv("influxDB_bucket")
  
  model_path = 'ai-model/gesture_recognizer.task'
  
  motor_controller = MotorController(port='/dev/cu.usbmodem70041DD465902')
  influxdb_writer = InfluxDBWriter(influxDB_url, influxDB_token, influxDB_org, influxDB_bucket)
  app = GestureRecognizerApp(model_path, motor_controller, influxdb_writer)
  app.run()

if __name__ == "__main__":
  main()
