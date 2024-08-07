import serial

ser = serial.Serial(port = "/dev/cu.usbmodem70041DD465902", baudrate = 115200)

while True:
  value = ser.readline()
  valueInString = str(value, "UTF-8")
  print(valueInString)
