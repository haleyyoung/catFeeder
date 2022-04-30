import RPi.GPIO as GPIO
from utilities import Log
from catFeeder import CatFeeder

GPIO.setmode(GPIO.BCM)
openDoorButtonPin = 25
GPIO.setup(openDoorButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
onepawFeeder = CatFeeder()
try:
  Log.info("Opening door via script")
  onepawFeeder.openTrapDoor()
except KeyboardInterrupt:
  onepawFeeder.killAllMotors()
  Log.info("Trap door button dead")

