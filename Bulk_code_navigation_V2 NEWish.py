from email import message

import RPi.GPIO as GPIO
import time
import cv2
import socket
import pickle
import struct
import threading
import smbus

#set ups for pins and directions
#four Directions #place holder numbers
direction1=1
direction2=2
direction3=3
direction4=4

BUTTON_PIN= 36 # pin 36 is the button for start

RF1_PIN=11 # pin 11 is for the first RF sensor
RF2_PIN=13 # pin 13 is for the second RF sensor
RF3_PIN=15 # pin 15 is for the third RD sensor

def setup_sensors(): #sensor set up
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RF1_PIN, GPIO.IN)
    GPIO.setup(RF2_PIN, GPIO.IN)
    GPIO.setup(RF3_PIN, GPIO.IN)

def read_sensors(): #sensor read
    sensor1 = GPIO.input(RF1_PIN)
    sensor2 = GPIO.input(RF2_PIN)
    sensor3 = GPIO.input(RF3_PIN)
    return sensor1, sensor2, sensor3

def avoid_line():
    sensor1, sensor2, sensor3 = read_sensors()

    if sensor2 > sensor1:
        # move motor to correct right/left as needed
        forward(20)
    elif sensor2 < sensor1:
        # move motor opposite direction
        backward(20)
    else:
        # sensors equal: keep going straight
        forward(20)

def frontline():
    # code to detect front line and stop if it detects it
    _, _, sensor3 = read_sensors()
    if sensor3 == 1:
        stop()  # stop the motor if the front sensor detects a line

def yellow_plusline():
    # code to detect yellow plus line and stop if it detects it
    # placeholder: checks front sensor and stops; add color-sensor logic here
    _, _, sensor3 = read_sensors()
    if sensor3 == 1:
        stop()  # stop the motor if the front sensor detects a line and yellow condition is met

def red_plusline():
    # code to detect red plus line and stop if it detects it
    # placeholder: checks front sensor and stops; add color-sensor logic here
    _, _, sensor3 = read_sensors()
    if sensor3 == 1:
        stop()  # stop the motor if the front sensor detects a line and red condition is met


IMU_SDA=3 #IMU PIN
IMU_SCL=5 #IMU PIN
def setup_IMU():
    bus = smbus.SMBus(1)  # Use I2C bus 1
    IMU_ADDRESS = 0x68  # I2C address of the IMU (e.g., MPU6050)
    bus.write_byte_data(IMU_ADDRESS, 0x6B, 0)  # Wake up the IMU (clear sleep mode)

def read_IMU():
    bus = smbus.SMBus(1)
    IMU_ADDRESS = 0x68
    # Read accelerometer and gyroscope data (example for MPU6050)
    accel_x = bus.read_i2c_block_data(IMU_ADDRESS, 0x3B, 6)  # Read accelerometer data
    gyro_x = bus.read_i2c_block_data(IMU_ADDRESS, 0x43, 6)   # Read gyroscope data
    return accel_x, gyro_x

Seven_segment= 7,8,10,24,26 #all seven segment pins

MD_PWR1_1 =12 #1st motor driver power switch
MD_IN1_1=16#1st motor driver speed
MD_IN2_1 = 18 #1st motor direction

MD_PWR1_2 =33 #2st motor driver power switch
MD_IN1_2=13#2st motor driver speed
MD_IN2_2 = 15 #2st motor direction

SW_1= 37 #switch pin for signal (low power)
SW_2= 35 #switch pin addtional

#MOTOR SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(MD_PWR1_1, GPIO.OUT)
GPIO.setup(MD_IN1_1, GPIO.OUT)
GPIO.setup(MD_IN2_1, GPIO.OUT)

GPIO.setmode(GPIO.BCM)
GPIO.setup(MD_PWR1_2, GPIO.OUT)
GPIO.setup(MD_IN1_2, GPIO.OUT)
GPIO.setup(MD_IN2_2, GPIO.OUT)

# PWM setup (speed control)
pwm = GPIO.PWM(MD_IN1_1, 1000)  # 1000 Hz
pwm.start(0)

def forward(speed):
    GPIO.output(MD_IN1_1, GPIO.HIGH)
    GPIO.output(MD_IN2_1, GPIO.LOW)
    GPIO.output(MD_IN1_2, GPIO.HIGH)
    GPIO.output(MD_IN2_2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def backward(speed):
    GPIO.output(MD_IN1_1, GPIO.LOW)
    GPIO.output(MD_IN2_1, GPIO.HIGH)
    GPIO.output(MD_IN1_2, GPIO.LOW)
    GPIO.output(MD_IN2_2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def stop():
    GPIO.output(MD_IN1_1, GPIO.LOW)
    GPIO.output(MD_IN2_1, GPIO.LOW)
    GPIO.output(MD_IN1_2, GPIO.LOW)
    GPIO.output(MD_IN2_2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

def left():#needs to be reworked
    GPIO.output(MD_IN1_1, GPIO.LOW)
    GPIO.output(MD_IN2_1, GPIO.LOW)
    GPIO.output(MD_IN1_2, GPIO.LOW)
    GPIO.output(MD_IN2_2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

def right():#needs to be reworked
    GPIO.output(MD_IN1_1, GPIO.LOW)
    GPIO.output(MD_IN2_1, GPIO.LOW)
    GPIO.output(MD_IN1_2, GPIO.LOW)
    GPIO.output(MD_IN2_2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)


def turn():#needs to be reworked
    if  read_IMU()[1][0] > 0: #example condition for turning right based on gyroscope data
        right() #turn right
    elif read_IMU()[1][0] < 0: #example condition for turning left based on gyroscope data
        left() #turn left                   
        elif read_IMU()[1][0] == 0: #example condition for going straight based on gyroscope data
            forward(20) #go straight at speed 20
            turned==(True) #set turned to true to indicate a turn has been made
        
        
    


#code to send camera feed on wifi to the receiving pc
def Send():
     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     client_socket.connect(('192.168.1.32', 5000)) #ip for the sending pc

     cap = cv2.VideoCapture(0)

     while True:

        ret, frame = cap.read()
    
        data = pickle.dumps(frame)
        message = struct.pack("Q" , len(data)) + data
    
        client_socket.sendall(message)
#code to receive data on wifi from the sending pc
def Receive(client_socket):  # receive data from the sending pc (called to the current pc connection(IP))
    while True:
        try:
            data = client_socket.recv(1024)  # receive data at up to 1024 bytes
            if not data:
                break
            message = data.decode().strip()  # decode and strip whitespace
            if message == "yellow": 
                yellow_plusline()
            elif message == "red":
                red_plusline()
            elif message == "green":
                forward(20)
        except Exception as e:
            print(f"Error receiving data: {e}")

            break

def out_put_seven_segment(): #code to output to seven segment display
    GPIO.output(Seven_segment, GPIO.HIGH) #placeholder: set all segments high; add logic to control specific segments based on conditions
    
            
    

#start button
Start=0 #always of unless it's told to start

GPIO.setmode(GPIO.BCM)
BUTTON_PIN= 36 # pin 36 is the button for start

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #setting pin 36 to setup
try:
    while True:
        if GPIO.input(BUTTON_PIN) == False:
            Start = 1
            time.sleep(1)
            turned = False #variable to track if a turn has been made
    

                    # establish connection to the sending PC for receiving commands
        try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect(('192.168.1.32', 5000))
                except Exception as e:
                    print(f"Could not connect to command server: {e}")
                    client_socket = None
        if Start == 1:
            starttimer = time.time() #code to start the timer
            #start navigation code: Start motor
            for d in directions:
                forward(20) # moving forward at 20 speed

                # Check the lines of the RF sensors
                setup_sensors()
                
                setup_IMU()  # Initialize the IMU

                while True:
                    avoid_line() # code to avoid line
                    if client_socket:
                        Receive(client_socket) # code to receive data from the sending pc (called to the current pc connection(IP))
                    elif Receive(client_socket) == "green":
                        forward(20)
                    elif Receive(client_socket) == "yellow":
                        yellow_plusline()
                    elif Receive(client_socket) == "red":
                        red_plusline()

                        if red_plusline() == False and turned == True or yellow_plusline() == True and turned == True:
                            d = d + 1
                            forward(20)
                            turned = False #see if turn has been made, if so, move to the next direction and reset turned to false for the next turn

            if d == 4 and frontline() == True and Receive(client_socket) == "Stop Sign":
                        stop()
                        break #stop the motor and end the program if the front line is detected and the stop sign command is received from the sending pc
        stop_timer = time.time() #code to stop the timer and calculate elapsed time
        time_elapsed = stop_timer - start_timer
        out_put_seven_segment(time_elapsed) #code to output elapsed time to seven segment display
                        
                    

            # Send image on delay ran on thread (call Send() or start a thread here)
except KeyboardInterrupt:
    print("exit")
    GPIO.cleanup()

                








     

     


     
    





















































































