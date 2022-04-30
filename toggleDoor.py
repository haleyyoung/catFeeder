import RPi.GPIO as GPIO
from utilities import Log
from catFeeder import CatFeeder

GPIO.setmode(GPIO.BCM)
openDoorButtonPin = 25
GPIO.setup(openDoorButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
onepawFeeder = CatFeeder()
try:
  if onepawFeeder.isDoorClosed():
    Log.info("Opening door via script")
    onepawFeeder.openTrapDoor()
  elif onepawFeeder.isDoorOpen():
    Log.info("Closing door via script")
    onepawFeeder.closeTrapDoor()
except KeyboardInterrupt:
  onepawFeeder.killAllMotors()
  Log.info("Trap door button dead")
