# HandGestureBot (Work in Progress Project)

Application to detect hand gesture in order to interact with simple Arduino based wooden robots.

**Presentation**: https://www.slideshare.net/slideshow/arduino-controlled-robot-using-hand-gestures-using-python/270870080

![alt text](https://github.com/suyashcjoshi/HandGestureBot/blob/main/misc/pic.png?raw=true)


## Setup & Run

### Pre-requisites
1. Download/clone this repository locally.
2. Make sure you have Python 3.x and pip installed on your machine. It's advisable to use a virtual enviornment for the same. Also you need Arduino IDE on your machine and corresponding board installed for your hardware.
3. Make sure you have [InfluxDB](https://www.influxdata.com) installed locally or cloud account (preferred) as you will need to provide the credentials for the same. It's best to create a .env file and store the credentials there.
4. Connect an Arduino device (I used Arduino Uno) to your computer over USB and make sure it has a servo motor attached to it. Take note of the pin number for the servo motor, in my example I've attached to pin 8. To find out the port address for Arduino device you can use this command `python -m serial.tools.list_ports`. Open the "arduino" directory and run the "arduino" sketches.
5. Alternatively you can also connect to arduino over 'WebSerial' using a browser, test code for the same is [here](https://editor.p5js.org/suyashjoshi/sketches/Ii6cmfKro)
6. Install the following python modules using pip: `pip install influxdb3-python mediapipe pyserial python-dotenv opencv-python`

### Running the app

- Firstly, open "GestureRecognizer.py" and update the main function with the correspending enviornment variables and value for "MotorController port address".
- Start the app by typing `python GestureRecognizer.py` and you should be able to see your webcam.
- Now make a few hand gestures and notice it controlling the arduino motors or robot if you have one connected.

### Testing Serial connection

Run the program `python test-serial.py`

### Contact

Please tag me on social media for any questions or if you build upon this, love to see [@suyashcjoshi](https://x.com/suyashcjoshi)
