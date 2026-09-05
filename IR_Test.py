import RPi.GPIO as GPIO
import time

# Use BOARD numbering
GPIO.setmode(GPIO.BOARD)

# PIN NUMBER FOR IR SENSOR
IR_LEFT_FRONT = 37
IR_LEFT_BACK = 38
IR_RIGHT_FRONT = 40
IR_RIGHT_BACK = 24

# Set sensors as inputs
GPIO.setup(IR_LEFT_FRONT, GPIO.IN)
GPIO.setup(IR_LEFT_BACK, GPIO.IN)
GPIO.setup(IR_RIGHT_FRONT, GPIO.IN)
GPIO.setup(IR_RIGHT_BACK, GPIO.IN)

print("IR Sensor Test")#shows working code
print("Press CTRL+C to stop")#shows how to cancel code
print("--------------------------------")

try:
    while True:

        left_front = GPIO.input(IR_LEFT_FRONT)
        left_back = GPIO.input(IR_LEFT_BACK)
        right_front = GPIO.input(IR_RIGHT_FRONT)
        right_back = GPIO.input(IR_RIGHT_BACK)

        print(
            f"Left Front: {left_front} | "
            f"Left Back: {left_back} | "
            f"RIGHT Front: {right_front} | "
            f"Right Back: {right_back}"
        )

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    GPIO.cleanup()
