from .Drive import Drive
from .Manip import Manip
from .MicroROV import MicroROV
from . import ROVMap
from . import ControllerServer
import queue
import sys
import os
import time
import traceback
from multiprocessing import Process, set_start_method

parts = [] # Component list for ease of looping in autoOp/teleOp function
operatingMode = True # Operate in Autonomous or TeleOp? True = TeleOp, False = Auto

# Creation of parts
# Drive thrusters
parts.append(Drive())
# Manipulator(s)
parts.append(Manip())
# MicroROV
parts.append(MicroROV())

ROVMap.log("All parts constructed")

# Defining stop method (Includes E Stop functionality through FATAL bool)
def stop(FATAL = False):
    """
    Stop the robot. Contains Capability for auto-shutdown of computer\n
    WARNING: IF TESTING THIS FATAL FUNCTIONALITY, IT WILL SHUTDOWN YOUR COMPUTER... YOU HAVE BEEN WARNED\n
    usage: stop(FATAL) Fatal=False by default
    """
    try:
        ROVMap.log(f"Received Stop Command.....Fatal? = {FATAL}")
        # Calmly deactivate all components
        ROVMap.JOYSTICK.__exit__()
        ROVMap.NetworkingProcess.kill()
        ControllerServer.ControllerProcess.kill()
        
        for Comp in parts:
            Comp.kill()
        # If EStop Fatal was triggered, shutdown Jetson immediately
        if(FATAL):
            ROVMap.log("Triggering system shutdown due to EStop", endO="")
            os.system('shutdown /s /t 1')
        ROVMap.log("ROV Successfully Shutdown", endO="")
    except:
        os.system('shutdown /s /t 1')

def start():
    """
    Start the Robot\n
    
    """
    # starts network handler
    # send stuff by putting to ROVMap.sendQueue
    # recv stuff by looking in ROVMap.dataQueue
    ROVMap.JetsonNetworking.start()

    # starts controller server
    ControllerServer.ControllerProcess.start()

    while True:
        # Update each component of the robot depending on the operating mode
        ROVMap.updateController()
        try:
            raise ROVMap.errQueue.get(block=False) # raise appropriate errors as they are received
        except queue.Empty:
            pass
        if(operatingMode):
            # Teleop
            for Comp in parts:
                Comp.Update()
        else:
            # Autonomous
            for Comp in parts:
                Comp.autoUpdate()


# Creates two processes, one for keyboard stop/estop and one for actually doing robo
try:
    if __name__ == "__main__":
        # start robot (blocking) and all child processes
        start()
# If interrupted for any reason, shut down every single part
except Exception as e:
    ROVMap.log("Received Interrupt.....Stopping")
    stop(isinstance(e, ROVMap.EStopInterruptFatal))
    