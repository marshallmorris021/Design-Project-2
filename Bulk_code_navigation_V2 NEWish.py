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
directions= [ "forward", "right", "left", "backward" ] #placeholder for the directions to be taken by the robot, will be replaced by the actual directions from the sending pc


#Pin layout

#motor driver 1(front two motors)
M1_Ain1= 11 #this is the pin for motordriver 1(first motor)
M1_Ain2= 13 #this is the pin for motordriver 1(first motor)
M1_Bin1= 15 #this is the pin for motordriver 1(second motor)
M1_Bin2= 16 #this is the pin for motordriver 1(second motor)
#MOTOR DRIVER 1 Power pins
M1_PWMA = 12 #this is the pin for motordriver 1(first motor) power
M1_PWMB = 22 #this is the pin for motordriver 1(second motor) power

#motor driver 2(back two motors)
M2_Ain1= 29 #this is the pin for motordriver 2(third motor)
M2_Ain2= 31 #this is the pin for motordriver 2(third motor)
M2_Bin1= 36 #this is the pin for motordriver 2  (fourth motor)
M2_Bin2= 35 #this is the pin for motordriver 2 (fourth motor)
#MOTOR DRIVER 2 Power pins
M2_PWMA = 32 #this is the pin for motordriver 2(third motor) power
M2_PWMB = 33 #this is the pin for motordriver 2(fourth motor) power

#Start Button
Start_Btn = 19 #this is the pin for the start button

#led pin
Status_led = 7 #this is the pin for the led

#reset button (Unsure why we are using this
Reset_Btn = 21 #this is the pin for the reset button)

#IMU setup
IMU_SDA = 3  #this is the pin for the IMU SDA
IMU_SCL = 5  #this is the pin for the IMU SCL

#IR sensor setup
IR_right = 37
IR_left = 40
IR_front = 38


#end of pin layout

#setup for all compoents

#Sensor Setup

def setup_sensors(): #sensor set up
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IR_right, GPIO.IN)
    GPIO.setup(IR_left, GPIO.IN)
    GPIO.setup(IR_front, GPIO.IN)

def read_sensors(): #sensor read
    sensor_Right = GPIO.input(IR_right)
    sensor_Left = GPIO.input(IR_left)
    sensor_Front = GPIO.input(IR_front)
    return sensor_Right, sensor_Left, sensor_Front

# IMU set-up

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

#motor driver setup

#MOTOR SETUP for front left
GPIO.setmode(GPIO.BCM)
GPIO.setup(M1_PWMA, GPIO.OUT)
GPIO.setup(M1_Ain1, GPIO.OUT)
GPIO.setup(M1_Ain2, GPIO.OUT)

#MOTOR SETUP for front right
GPIO.setmode(GPIO.BCM)
GPIO.setup(M1_PWMB, GPIO.OUT)
GPIO.setup(M1_Bin1, GPIO.OUT)
GPIO.setup(M1_Bin2, GPIO.OUT)

#MOTOR SETUP for back left
GPIO.setmode(GPIO.BCM)
GPIO.setup(M2_PWMA, GPIO.OUT)
GPIO.setup(M2_Ain1, GPIO.OUT)
GPIO.setup(M2_Ain2, GPIO.OUT)

#MOTOR SETUP for back right
GPIO.setmode(GPIO.BCM)
GPIO.setup(M2_PWMB, GPIO.OUT)
GPIO.setup(M2_Bin1, GPIO.OUT)
GPIO.setup(M2_Bin2, GPIO.OUT)


# PWM setup (speed control)
pwm_FL = GPIO.PWM(M1_PWMA, 1000)  # 1000 Hz
pwm_FR = GPIO.PWM(M1_PWMB, 1000)  # 1000 Hz
pwm_BL = GPIO.PWM(M2_PWMA, 1000)  # 1000 Hz
pwm_BR = GPIO.PWM(M2_PWMB, 1000)  # 1000 Hz
pwm_FL.start(0)
pwm_FR.start(0)
pwm_BL.start(0)
pwm_BR.start(0)



#stop movement
def stop(speed):
    GPIO.output(M1_Ain1, GPIO.LOW) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.LOW) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.LOW)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.LOW) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.LOW) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed

#forward movement
def forward(speed):
    GPIO.output(M1_Ain1, GPIO.HIGH) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.HIGH) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.LOW)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.HIGH) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.HIGH) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed

#backward movement
def Backward(speed):
    GPIO.output(M1_Ain1, GPIO.LOW)
    GPIO.output(M1_Ain2, GPIO.HIGH)
    GPIO.output(M1_Bin1, GPIO.LOW)
    GPIO.output(M1_Bin2, GPIO.HIGH)
    GPIO.output(M2_Ain1, GPIO.LOW)
    GPIO.output(M2_Ain2, GPIO.HIGH)
    GPIO.output(M2_Bin1, GPIO.LOW)
    GPIO.output(M2_Bin2, GPIO.HIGH)
    pwm_FL.ChangeDutyCycle(speed)
    pwm_FR.ChangeDutyCycle(speed)
    pwm_BL.ChangeDutyCycle(speed)
    pwm_BR.ChangeDutyCycle(speed)

#Right movement
def Right(speed):
    GPIO.output(M1_Ain1, GPIO.LOW)
    GPIO.output(M1_Ain2, GPIO.HIGH)
    GPIO.output(M1_Bin1, GPIO.LOW)
    GPIO.output(M1_Bin2, GPIO.LOW)
    GPIO.output(M2_Ain1, GPIO.HIGH)
    GPIO.output(M2_Ain2, GPIO.LOW)
    GPIO.output(M2_Bin1, GPIO.LOW)
    GPIO.output(M2_Bin2, GPIO.LOW)
    pwm_FL.ChangeDutyCycle(speed)
    pwm_FR.ChangeDutyCycle(speed)
    pwm_BL.ChangeDutyCycle(speed)
    pwm_BR.ChangeDutyCycle(speed)
#Left movement
def Left(speed):
    GPIO.output(M1_Ain1, GPIO.HIGH) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.LOW) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.HIGH)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.LOW) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.HIGH) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.HIGH) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed

#forward Right movement
def Forward_Right(speed):
    GPIO.output(M1_Ain1, GPIO.LOW)
    GPIO.output(M1_Ain2, GPIO.HIGH)
    GPIO.output(M1_Bin1, GPIO.LOW)
    GPIO.output(M1_Bin2, GPIO.HIGH)
    GPIO.output(M2_Ain1, GPIO.LOW)
    GPIO.output(M2_Ain2, GPIO.HIGH)
    GPIO.output(M2_Bin1, GPIO.LOW)
    GPIO.output(M2_Bin2, GPIO.HIGH)
    pwm_FL.ChangeDutyCycle(speed)
    pwm_FR.ChangeDutyCycle(speed)
    pwm_BL.ChangeDutyCycle(speed)
    pwm_BR.ChangeDutyCycle(speed)

#forward Left movement
def Forward_Left(speed):
    GPIO.output(M1_Ain1, GPIO.HIGH) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.LOW) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.LOW)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.LOW) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.HIGH) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed

#Backward Right movement
def Backward_Right(speed):
    GPIO.output(M1_Ain1, GPIO.LOW) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.HIGH)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.LOW) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.LOW)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.LOW) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.LOW) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.HIGH) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed

#Backward Left movement
def Backward_Left(speed):
    GPIO.output(M1_Ain1, GPIO.LOW) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.LOW) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.HIGH)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.LOW) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.LOW) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.HIGH) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed

#Turn right movement
def Turn_Right(speed):
    GPIO.output(M1_Ain1, GPIO.HIGH) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.LOW) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.HIGH)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.HIGH) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.LOW) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.HIGH) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed

    #Turn left movement
def Turning_Left(speed):
    GPIO.output(M1_Ain1, GPIO.LOW) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.HIGH)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.HIGH) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.LOW)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.LOW) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.HIGH) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.HIGH) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed

    #Curved Left movement
def Curverd_left(speed):
    GPIO.output(M1_Ain1, GPIO.HIGH) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.HIGH) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.LOW)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.HIGH) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.HIGH) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed/2) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed/2) #back right motor speed

        #Curved Right movement
def Curverd_right(speed):
    GPIO.output(M1_Ain1, GPIO.HIGH) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.HIGH) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.LOW)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.HIGH) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.HIGH) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed/2) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed/2) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed

        # lateral left movement
def Lateral_left(speed):
    GPIO.output(M1_Ain1, GPIO.HIGH) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.LOW) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.HIGH)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.LOW) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.LOW) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed
# lateral right movement
def Lateral_right(speed):
    GPIO.output(M1_Ain1, GPIO.LOW) #Front left motor forward
    GPIO.output(M1_Ain2, GPIO.HIGH)  #front left motor backward
    GPIO.output(M1_Bin1, GPIO.HIGH) #front right motor forward
    GPIO.output(M1_Bin2, GPIO.LOW)  #front right motor backward
    GPIO.output(M2_Ain1, GPIO.LOW) #back left motor forward
    GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
    GPIO.output(M2_Bin1, GPIO.LOW) #back right motor forward
    GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
    pwm_FL.ChangeDutyCycle(speed) #front left motor speed
    pwm_FR.ChangeDutyCycle(speed) #front right motor speed
    pwm_BL.ChangeDutyCycle(speed) #back left motor speed
    pwm_BR.ChangeDutyCycle(speed) #back right motor speed


 #   def turn():#needs to be reworked
 #  if  read_IMU()[1][0] > 0: #example condition for turning right based on gyroscope data
  #      right() #turn right
  #  elif read_IMU()[1][0] < 0: #example condition for turning left based on gyroscope data
  #      left() #turn left                   
  #  elif read_IMU()[1][0] == 0: #example condition for going straight based on gyroscope data
   #     forward(20) #go straight at speed 20
    #    turned==(True) #set turned to true to indicate a turn has been made







def avoid_line():
    sensor_Right, sensor_Left, sensor_Front = read_sensors()

    if sensor_Left > sensor_Right:
        # move motor to correct right/left as needed
        Lateral_right(20)  # example speed value
    elif sensor_Left < sensor_Right:
        # move motor opposite direction
        Lateral_left(20)  # example speed value
    elif sensor_Left == sensor_Right:
        # sensors equal: keep going straight
        forward(20)
    else:
        # sensors equal: keep going straight
        forward(20)

def Front_line():
    sensor_Right, sensor_Left, sensor_Front = read_sensors()
    if sensor_Front == 1:
        return (1)  # stop the motor if the front sensor detects a line
    return (0)  # continue moving if no line is detected

     
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


def Send_time():
     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     client_socket.connect(('192.168.1.32', 5000)) #ip for the sending pc
     while True:
      client_socket.sendall(str(time_elapsed).encode())  # send the elapsed time as a string


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


#check for front line detection and stop if it detects it
def frontline():
    # code to detect front line and stop if it detects it
    _, _, sensor_Front = read_sensors()
    if sensor_Front == 1:
        stop()  # stop the motor if the front sensor detects a line


#yellow signal + front line detection
def yellow_plusline():
    # code to detect yellow plus line and stop if it detects it
    # placeholder: checks front sensor and stops; add color-sensor logic here
    _, _, sensor_Front = read_sensors()
    if sensor_Front == 1 and Receive(client_socket) == "yellow":
        stop()  # stop the motor if the front sensor detects a line and yellow condition is met

#red signal + front line detection
def red_plusline():
    # code to detect red plus line and stop if it detects it
    # placeholder: checks front sensor and stops; add color-sensor logic here
    _, _, sensor_Front = read_sensors()
    if sensor_Front == 1 and Receive(client_socket) == "red":
        stop()  # stop the motor if the front sensor detects a line and red condition is met

#stop sign + front line detection
def Stopsign_plusline():
    # code to detect stop sign plus line and stop if it detects it
    # placeholder: checks front sensor and stops; add color-sensor logic here
    _, _, sensor_Front = read_sensors()
    if sensor_Front == 1 and Receive(client_socket) == "Stop Sign":
        stop()  # stop the motor if the front sensor detects a line and stop sign condition is met

#function used for threading the camera capture and sending/receiving data
def Threading_Camera_Capture():
    try: 
        Send() #code to send camera feed on wifi to the receiving pc
        Receive(client_socket) #code to receive data on wifi from the sending pc
    except Exception as e:
        print(f"Error in camera capture: {e}")


#start button
Start=0 #always of unless it's told to start
GPIO.setup(Start_Btn, GPIO.IN, pull_up_down=GPIO.PUD_UP) #setting pin 36 to setup
try:
    while True:
        if GPIO.input(Start_Btn) == False:
            Start = 1 #tell to start
            Turn_counter=0 #how many turns have been made, used to track the direction of the robot
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
            start_timer = time.time() #code to start the timer
            #start navigation code: Start motor
            for d in directions:
                forward(20) # moving forward at 20 speed
                start_timer = time.time()  # Start the timer for elapsed time calculation
                # Set up Sensor and Imu
                setup_sensors()
                
                setup_IMU()  # Initialize the IMU
                Threading_Camera_Capture()  # Start camera capture and data sending/receiving in a separate thread

                #start the threading for the camera capture and sending/receiving data
                Camera_thread = threading.Thread(target=Threading_Camera_Capture)
                Camera_thread.daemon = True  # Daemonize thread to exit when main program exits
                Camera_thread.start()  # Start the camera capture thread

                while True:
                    avoid_line() # code to avoid line
                    yellow_plusline() #code to detect yellow plus line and stop if it detects it
                    red_plusline() #code to detect red plus line and stop if it detects it
                    Stopsign_plusline() #code to detect stop sign plus line and stop if it detects it
            if Front_line() == True:
                    forward(20) # move forward if front line is detected
                    if directions == "right":
                        Turn_Right(20) #turn right if the direction is right
                    elif directions == "left":
                        Turning_Left(20) #turn left if the direction is left
                    elif directions == "straight":
                        forward(20) #move forward if the direction is forward

                    time.sleep(1)#wait to continue straight after turning
                    forward(20) #move forward after turning
                    Turn_counter = Turn_counter + 1 #increment the turn counter by 1
            if Turn_counter == 4 and Front_line() == True and Receive(client_socket) == "Stop Sign":
                        stop()
                        break #stop the motor and end the program if the front line is detected and the stop sign command is received from the sending pc
        stop_timer = time.time() #code to stop the timer and calculate elapsed time
        time_elapsed = stop_timer - start_timer 

        # Send image on delay ran on thread (call Send() or start a thread here)
        Send_time(time_elapsed)  # Send the elapsed time to the sending PC
except KeyboardInterrupt:
    print("exit")
    GPIO.cleanup()
