import RPi.GPIO as GPIO
import board
import time
from datetime import datetime
from adafruit_motorkit import MotorKit

from utilities import Log
from texts import Texts

class CatFeeder:
  def __init__(self):
    self.kit = MotorKit()
    self.kit2 = MotorKit(address=0x61)
    GPIO.setmode(GPIO.BCM)
    self.doorOpenLimitSwitchPin = 16
    self.doorClosedLimitSwitchPin = 21
    GPIO.setup(self.doorOpenLimitSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(self.doorClosedLimitSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    self.catLastFed = None
    self.texts = Texts()

  def doorMotor(self):
    return self.kit.motor1

  def bowlsMotor(self):
    return self.kit.motor2

  def stirrerMotor(self):
    return self.kit.motor3

  def dispenseFoodMotor(self):
    return self.kit.motor4

  def isEnabled(self):
    filename = "/home/pi/catFeeder/enabled.setting"
    file = open(filename, 'r')
    currentValue = file.read()
    file.close()
    return currentValue == 'True'

  def toggleEnabled(self):
    currentValue = self.isEnabled()
    filename = "/home/pi/catFeeder/enabled.setting"
    file = open(filename, 'w')
    file.write(str(not currentValue))
    file.close()

  def isCatEligibleToEat(self):
    if not self.isEnabled():
      Log.info("WARNING SYSTEM OFF")
      return
    MORNING_START_TIME = "05:30:00"
    MORNING_END_TIME = "11:30:00"
    EVENING_START_TIME = "18:00:20"
    EVENING_END_TIME = "23:59:59"
    morningEarlyBound = datetime.strptime(MORNING_START_TIME, '%H:%M:%S').time()
    morningLateBound = datetime.strptime(MORNING_END_TIME, '%H:%M:%S').time()
    eveningEarlyBound = datetime.strptime(EVENING_START_TIME, '%H:%M:%S').time()
    eveningLateBound = datetime.strptime(EVENING_END_TIME, '%H:%M:%S').time()

    now = datetime.now().time()

    # If the cat was fed in the last 6 hours, she doesn't need more
    sixHoursAgo = now - timedelta(hours=6)
    if self.catLastFed != None and self.catLastFed >= sixHoursAgo:
      return False

    Log.info("morning window? {value}".format(value=morningEarlyBound <= now and now <= morningLateBound))
    Log.info("evening window? {value}".format(value=eveningEarlyBound <= now and now <= eveningLateBound))

    if morningEarlyBound <= now and now <= morningLateBound:
      return True
    if eveningEarlyBound <= now and now <= eveningLateBound:
      return True
    return False

  def isDoorOpen(self):
    return GPIO.input(self.doorOpenLimitSwitchPin)

  def isDoorClosed(self):
    return GPIO.input(self.doorClosedLimitSwitchPin)

  def isDoorInMotion(self):
    if self.kit.motor1.throttle == None or self.kit.motor1.throttle == 0:
      return False
    return True

  def openTrapDoor(self):
    if not self.isEnabled():
      Log.info("WARNING SYSTEM OFF")
      return
    timeToOpenStart = time.time()
    while not self.isDoorOpen():
      if self.kit.motor1.throttle != 1:
        Log.info("Trap door opening!!")
        timeToOpenStart = time.time()
        self.kit.motor1.throttle = 1
      if self.checkForTrapDoorIssues(timeToOpenStart, "opening"):
        return
    self.kit.motor1.throttle = 0
    print(f"door took {time.time() - timeToOpenStart} seconds to open")
    Log.info("TRAP DOOR OPEN - complete!")

  def closeTrapDoor(self):
    if not self.isEnabled():
      Log.info("WARNING SYSTEM OFF")
      return
    timeToCloseStart = time.time()
    while not self.isDoorClosed():
      if self.kit.motor1.throttle != -1:
        Log.info("Trap door closing!!")
        timeToCloseStart = time.time()
        self.kit.motor1.throttle = -1
      if self.checkForTrapDoorIssues(timeToCloseStart, "closing"):
        return
    self.kit.motor1.throttle = 0
    print(f"door took {time.time() - timeToCloseStart} seconds to close")
    Log.info("TRAP DOOR CLOSED - complete!")

  # Door mechanical issues catch
  def checkForTrapDoorIssues(self, doorMovementStartTime, doorDirection):
    if (doorMovementStartTime is not None) and ((time.time() - doorMovementStartTime) > 10):
      print(f"trap door broken? {time.time() - doorMovementStartTime}")
      Log.info(f"Trap door is stuck while {doorDirection}. The motor has been turned off")
      # Text something went wrong
      self.texts.sendText(f"❌ The trap door is stuck while {doorDirection}. The motor has been turned off\n\nTime: {datetime.now().strftime('%H:%M:%S')}")
      self.kit.motor1.throttle = 0
      return True
    return False

  # Open and close the trap door
  def clearDirtyBowl(self):
    if not self.isEnabled():
      Log.info("WARNING SYSTEM OFF")
      return
    self.openTrapDoor()
    Log.info("Trap door will close soon...")
    time.sleep(1)
    self.closeTrapDoor()
    Log.info("Dirty bowl handled!!")

  def dropNewBowl(self):
    if not self.isEnabled():
      Log.info("WARNING SYSTEM OFF")
      return
    Log.info("Dispensing clean bowl!!")
    self.kit.motor2.throttle = 1.0
    time.sleep(1.7)
    self.kit.motor2.throttle = 0
    Log.info("Clean bowl dispensed!!")

  def clearDirtyBowlAndDropNewBowl(self):
    Log.info("Clearing old bowl")
    modifiedEnabledState = False
    # We don't want the motion sensors to go off while clearing the bowl
    if onepawFeeder.isEnabled():
      onepawFeeder.toggleEnabled()
      modifiedEnabledState = True
    self.clearDirtyBowl()
    self.dropNewBowl()
    if modifiedEnabledState:
      onepawFeeder.toggleEnabled()
    Log.info("Old bowl cleared!")

  def pushBowls(self):
    if not self.isEnabled():
      Log.info("WARNING SYSTEM OFF")
      return
    Log.info("Pushing bowls!!")
    self.kit2.motor1.throttle = 1
    time.sleep(1.6)
    self.kit2.motor1.throttle = 0
    time.sleep(1)
    self.kit2.motor1.throttle = -1
    time.sleep(1.6)
    self.kit2.motor1.throttle = 0
    Log.info("Bowls pushed!!")

  def stirFood(self):
    if not self.isEnabled():
      Log.info("WARNING SYSTEM OFF")
      return
    Log.info("Stirring food!!")
    self.kit.motor3.throttle = 1
    time.sleep(30)
    self.kit.motor3.throttle = 0
    Log.info("Food is sufficiently mixed!!")

  def dispenseFood(self, duration):
    if not self.isEnabled():
      Log.info("WARNING SYSTEM OFF")
      return
    Log.info("Dispensing food!!")
    self.kit.motor4.throttle = -1
    time.sleep(duration)
    self.kit.motor4.throttle = 1
    time.sleep(duration)
    self.kit.motor4.throttle = 0
    Log.info("Food is dispensed!!")

    self.texts.sendText(f"✅ Onepaw has been fed, check to see if enough food was dispensed.\n\nTime: {datetime.now().strftime('%H:%M:%S')}")
    # Save the last time the cat was fed
    self.catLastFed = datetime.now()

  def killAllMotors(self):
    Log.info("Killing all motors")
    self.kit.motor1.throttle = 0
    self.kit.motor2.throttle = 0
    self.kit.motor3.throttle = 0
    self.kit.motor4.throttle = 0
    Log.info("ALL MOTORS OFF")
