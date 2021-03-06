from adafruit_servokit import ServoKit
from adafruit_motor import servo
from .Vector import Vector
from . import Controller

SQRT2 = 1.4142136


def start():
    print("AZIMUTH ROTATION SCRIPT")
    kit = ServoKit(channels=16)

    VELOCITY_MOD = .5

    TURN = False
    
    THRUSTER_FRONT_LEFT = kit._items[0] = servo.ContinuousServo(kit._pca.channels[0])
    THRUSTER_FRONT_LEFT_THRUST_VECTOR = Vector(SQRT2/2, SQRT2/2, 0)
    THRUSTER_FRONT_RIGHT = kit._items[1] = servo.ContinuousServo(kit._pca.channels[1])
    THRUSTER_FRONT_RIGHT_THRUST_VECTOR = Vector(-SQRT2/2, SQRT2/2, 0)
    THRUSTER_BACK_LEFT = kit._items[2] = servo.ContinuousServo(kit._pca.channels[2])
    THRUSTER_BACK_LEFT_THRUST_VECTOR = Vector(SQRT2/2, -SQRT2/2, 0)
    THRUSTER_BACK_RIGHT = kit._items[3] = servo.ContinuousServo(kit._pca.channels[3])
    THRUSTER_BACK_RIGHT_THRUST_VECTOR = Vector(-SQRT2/2, -SQRT2/2, 0)
    THRUSTER_FRONT_LEFT.set_pulse_width_range(1200,2000)
    THRUSTER_FRONT_RIGHT.set_pulse_width_range(1200,2000)
    THRUSTER_BACK_LEFT.set_pulse_width_range(1200,2000)
    THRUSTER_BACK_RIGHT.set_pulse_width_range(1200,2000)

    while True:
        rightStick = Controller.getRightStick()
        target = Vector()
        if(Controller.getButtonPresses == 1):
            target = Vector(0,0,1)
        elif(rightStick[2] == 1):
            target = Vector(0,0,0)

        if(TURN):
            print(target.toString())
            THRUSTER_FRONT_LEFT.throttle = -(THRUSTER_FRONT_LEFT_THRUST_VECTOR.crossProduct(target).getMagnitude() * VELOCITY_MOD)
            THRUSTER_FRONT_RIGHT.throttle = (THRUSTER_FRONT_RIGHT_THRUST_VECTOR.crossProduct(target).getMagnitude() * VELOCITY_MOD)
            THRUSTER_BACK_LEFT.throttle = (THRUSTER_BACK_LEFT_THRUST_VECTOR.crossProduct(target).getMagnitude() * VELOCITY_MOD)
            THRUSTER_BACK_RIGHT.throttle = -(THRUSTER_BACK_RIGHT_THRUST_VECTOR.crossProduct(target).getMagnitude() * VELOCITY_MOD)

        if(Controller.getButtonPresses().rs):
            if(TURN):
                TURN = False
            else:
                TURN = True