import time

# Use this class for all logging needs. Instance of Logger has already been created -> main -> logger variable
class Logger:
    # Constructor creates global file object named f
    def __init__(self):
        global f
        time = Logger.getTimeFormatted('_')
        f = open("ROV/Logs/" + f"{time}" + ".txt", "w")

    # Call this method to log something compatible with all data types capable of conversion to str through str()
    def log(self, strin, endO="\n"):
        strin = '[' + Logger.getTimeFormatted(':') + '] ' + str(strin) + endO
        f.write(strin)

    def getTimeFormatted(delim):
        SYSTIME = time.localtime(time.time())
        return (str(SYSTIME.tm_hour) + delim + str(SYSTIME.tm_min) + delim + str(SYSTIME.tm_sec))
    
    def closeLog():
        f.close()