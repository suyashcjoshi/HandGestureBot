# HandGestureBot (Work in Progress Project)
Application to detect hand gesture and landmark locations in order to interact with Arduino robots.

## Setup & Run

### Pre-requisites
1. Download/clone this repository locally.
2. Make sure you have Python 3.x and pip installed on your machine. It's advisable to use a virtual enviornment for the same.
3. Make sure you have InfluxDB installed locally or cloud account (free one is good) as you will need to provide the credentials for the same. It's best to create a .env file and store the credentials there.
4. Connect an Arduino device (I used Arduino Uno) to your computer over USB and make sure it has a servo motor attached to it. Take note of the pin number for the servo motor, in my example I've attached to pin 8. To find out the port address for Arduino device you can use this command `
5. Alternatively you can also connect to arduino over 'WebSerial' using a browser, test code for the same is [here](https://editor.p5js.org/suyashjoshi/sketches/Ii6cmfKro)
6. Install the following python modules using pip: `pip install influxdb3-python mediapipe pyserial python-dotenv opencv-python`

### Running the app

This app is mianly a python project which can be started by typing `python GestureRecognizer.py` and you should be able to see your webcam. Now make a few hand gestures and notice it controlling the arduino motors or robot if you have one connected.

### Testing Serial connection

Run the program `python test-serial.py`
