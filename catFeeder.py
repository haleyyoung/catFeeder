import RPi.GPIO as GPIO
import board

from adafruit_motorkit import MotorKit

from utilities import Log

class CatFeeder:
  def __init__(self):
    self.kit = MotorKit()
    self.kit2 = MotorKit(address=0x61)
    GPIO.setmode(GPIO.BCM)
    self.doorOpenLimitSwitchPin = 16
    self.doorClosedLimitSwitchPin = 21
    GPIO.setup(self.doorOpenLimitSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(self.doorClosedLimitSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  def doorMotor(self):
    return self.kit.motor1

  def bowlsMotor(self):
    return self.kit.motor2

  def stirrerMotor(self):
    return self.kit.motor3

  def dispenseFoodMotor(self):
    return self.kit.motor4

  def isDoorOpen(self):
    return GPIO.input(self.doorOpenLimitSwitchPin)

  def isDoorClosed(self):
    return GPIO.input(self.doorClosedLimitSwitchPin)

  def isDoorInMotion(self):
    if self.kit.motor1.throttle == None or self.kit.motor1.throttle == 0:
      return False
    return True

  def openTrapDoor(self):
    while not self.isDoorOpen():
      if self.kit.motor1.throttle != 1:
        Log.info("Trap door opening!!")
        self.kit.motor1.throttle = 1
    self.kit.motor1.throttle = 0
    Log.info("TRAP DOOR OPEN - complete!")

  def closeTrapDoor(self):
    while not self.isDoorClosed():
      if self.kit.motor1.throttle != -1:
        Log.info("Trap door closing!!")
        self.kit.motor1.throttle = -1
    self.kit.motor1.throttle = 0
    Log.info("TRAP DOOR CLOSED - complete!")

  # Open and close the trap door
  def clearDirtyBowl(self):
    self.openTrapDoor()
    Log.info("Trap door will close soon...")
    time.sleep(1)
    self.closeTrapDoor()
    Log.info("Dirty bowl handled!!")

    Log.info("Dispensing clean bowl!!")
    self.kit.motor2.throttle = 1.0
    time.sleep(1.7)
    self.kit.motor2.throttle = 0
    Log.info("Clean bowl dispensed!!")

  def clearDirtyBowlAndDropNewBowl(self):
    Log.info("Clearing old bowl")
    self.clearDirtyBowl()
    self.dropNewBowl()
    Log.info("Old bowl cleared!")

  def stirFood(self):
    Log.info("Stirring food!!")
    self.kit.motor3.throttle = 1
    time.sleep(30)
    self.kit.motor3.throttle = 0
    Log.info("Food is sufficiently mixed!!")

  def dispenseFood(self, duration):
    Log.info("Dispensing food!!")
    self.kit.motor4.throttle = -1
    time.sleep(duration)
    self.kit.motor4.throttle = 1
    time.sleep(duration)
    self.kit.motor4.throttle = 0
    Log.info("Food is dispensed!!")



