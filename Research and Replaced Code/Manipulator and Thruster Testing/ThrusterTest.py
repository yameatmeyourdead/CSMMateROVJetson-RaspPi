from adafruit_platformdetect.board import Board
from adafruit_servokit import ServoKit
import busio
import adafruit_pca9685
from adafruit_motor import motor
import board

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c, address=0x40)
pca.frequency=300

motorChannel = pca.channels[4]

motorChannel.duty_cycle = 0x7fff

while True:
    motorChannel.duty_cycle = int(input("Throttle : "), 16)


# # initialize pca9685
# kit = ServoKit(channels=16)

# # declare motor esc as continuous servo because it expects servo like PWM input
# kit.continuous_servo[0].set_pulse_width_range(1100,1900)

# # allow myself to control it
# while True:
#     kit.continuous_servo[0].throttle = float(input("Throttle?"))