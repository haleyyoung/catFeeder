import RPi.GPIO as GPIO
import board
import time
from datetime import datetime
from utilities import Log
from catFeeder import CatFeeder

GPIO.setmode(GPIO.BCM)
dispenseFoodButtonPin = 27
GPIO.setup(dispenseFoodButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
onepawFeeder = CatFeeder()

def dispenseFoodButtonPushed():
  isButtonPushed = GPIO.input(dispenseFoodButtonPin)
  if isButtonPushed:
    time.sleep(0.25)
    if GPIO.input(dispenseFoodButtonPin):
      onepawFeeder.dispenseFood(3)
      Log.info("Dispense Food putton pushed")
      time.sleep(2)

try:
  while True:
    dispenseFoodButtonPushed()
except KeyboardInterrupt:
  onepawFeeder.killAllMotors()
  Log.info("Dispense Food button dead")

