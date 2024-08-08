# Connect to Arduino over Serial protocol
# Author: Suyash Joshi

import serial

class MotorController:
  def __init__(self, port, baudrate = 115200):
    self.ser = serial.Serial(port, baudrate)
    
  def send_gesture_to_motor_controller(self, gesture):
    if gesture == 'Thumbs_Up':
      self.send_servo_position(90)
    elif gesture == 'Closed_Fist':
      self.send_servo_position(180)

  def send_servo_position(self, position):
    self.ser.write(f'{position}\n'.encode())

  def read_value(self):
    while True:
      value = self.ser.readline()
      value_in_string = value.decode('UTF-8')
      print(value_in_string)
