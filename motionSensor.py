import board
import time
import digitalio
import RPi.GPIO as GPIO

class MotionSensor:
  def __init__(self, pin):
    GPIO.setmode(GPIO.BCM)
    self.pin = pin
    GPIO.setup(self.pin, GPIO.IN)
    self.lastDetectedValue = GPIO.input(self.pin)
  def currentValue:
    self.lastDetectedValue = GPIO.input(self.pin)
    return self.lastDetectedValue
  # Consistent motion is considered that which lasts at least 3 seconds
  def consistentMotionSensed:
    i = 0
    while i < 3:
      if not currentValue():
        return false
      i = i + 1
      time.sleep(1)
    return true