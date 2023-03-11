import RPi.GPIO as GPIO
import board
import time
from datetime import datetime
from utilities import Log
from catFeeder import CatFeeder

GPIO.setmode(GPIO.BCM)
openDoorButtonPin = 25
GPIO.setup(openDoorButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
onepawFeeder = CatFeeder()

def openDoorButtonPushed():
  isButtonPushed = GPIO.input(openDoorButtonPin)
  if isButtonPushed:
    time.sleep(0.25)
    isButtonPushed = GPIO.input(openDoorButtonPin)
    if isButtonPushed:
      Log.info("Button pushed, toggling trap door")
  return isButtonPushed

try:
  while True:
    if not onepawFeeder.isDoorInMotion():
      if openDoorButtonPushed() and onepawFeeder.isDoorClosed():
        onepawFeeder.openTrapDoor()
      if openDoorButtonPushed() and onepawFeeder.isDoorOpen():
        onepawFeeder.closeTrapDoor()
except KeyboardInterrupt:
  onepawFeeder.killAllMotors()
  Log.info("Trap door button dead")

