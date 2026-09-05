import RPi.GPIO as GPIO
import time

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

# Standby pin
STBY = 18

#code to set standby high for the motor drivers to work XD
GPIO.setup(STBY, GPIO.OUT)
GPIO.output(STBY, GPIO.HIGH)


#MOTOR SETUP for front left
GPIO.setmode(GPIO.BOARD)
GPIO.setup(M1_PWMA, GPIO.OUT)
GPIO.setup(M1_Ain1, GPIO.OUT)
GPIO.setup(M1_Ain2, GPIO.OUT)

#MOTOR SETUP for front right
GPIO.setmode(GPIO.BOARD)
GPIO.setup(M1_PWMB, GPIO.OUT)
GPIO.setup(M1_Bin1, GPIO.OUT)
GPIO.setup(M1_Bin2, GPIO.OUT)

#MOTOR SETUP for back left
GPIO.setmode(GPIO.BOARD)
GPIO.setup(M2_PWMA, GPIO.OUT)
GPIO.setup(M2_Ain1, GPIO.OUT)
GPIO.setup(M2_Ain2, GPIO.OUT)

#MOTOR SETUP for back right
GPIO.setmode(GPIO.BOARD)
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

#defition for the speed of the motors
def set_motor_speed(speed):
    pwm_FL.ChangeDutyCycle(speed)
    pwm_FR.ChangeDutyCycle(speed)
    pwm_BL.ChangeDutyCycle(speed)
    pwm_BR.ChangeDutyCycle(speed)


Start=0 #always of unless it's told to start
GPIO.setup(Start_Btn, GPIO.IN, pull_up_down=GPIO.PUD_UP) #setting pin 19 to setup
try:
    while True:
        if GPIO.input(Start_Btn) == True:

            GPIO.output(M1_Ain1, GPIO.HIGH) #Front left motor forward
            GPIO.output(M1_Ain2, GPIO.LOW)  #front left motor backward
            GPIO.output(M1_Bin1, GPIO.HIGH) #front right motor forward
            GPIO.output(M1_Bin2, GPIO.LOW)  #front right motor backward
            GPIO.output(M2_Ain1, GPIO.HIGH) #back left motor forward
            GPIO.output(M2_Ain2, GPIO.LOW) #back left motor backward
            GPIO.output(M2_Bin1, GPIO.HIGH) #back right motor forward
            GPIO.output(M2_Bin2, GPIO.LOW) #back right motor backward
            set_motor_speed(500) #set all motors to 1000 speed
            time.sleep(10)
            break 


except KeyboardInterrupt:
    print("exit")
    GPIO.cleanup()
