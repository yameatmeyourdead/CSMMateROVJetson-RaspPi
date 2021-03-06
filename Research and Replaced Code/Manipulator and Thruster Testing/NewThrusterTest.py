from adafruit_servokit import ServoKit
from adafruit_motor import servo

# initialize pca9685
kit = ServoKit(channels=16)


# declare motor esc as continuous servo because it expects servo like PWM input
kit._items[4] = servo.ContinuousServo(kit._pca.channels[0])
ESC = kit._items[4]

# experimentally found pulse width range shifted -> 100
ESC.set_pulse_width_range(1200,2000)

# allow myself to control it
while True:
    ESC.throttle = float(input("OUT> "))