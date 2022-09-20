import RPi.GPIO as GPIO
import board
import time
from datetime import datetime, timedelta
import asyncio

from utilities import Log
from catFeeder import CatFeeder

class MotionSensor:
  def __init__(self, pin):
    GPIO.setmode(GPIO.BCM)
    self.pin = pin
    GPIO.setup(self.pin, GPIO.IN)

  def currentValue(self):
    return GPIO.input(self.pin)

  # Consistent motion is considered that which lasts at least 3 seconds
  @asyncio.coroutine
  def consistentMotionSensed(self, sensorName):
    i = 0
    while i < 3:
      if not self.currentValue():
        return False
      i = i + 1
      yield from asyncio.sleep(1)
    return True

class MotionSensorFeeder:
  def __init__(self):
    self.feeder = CatFeeder()

  def isCatEligibleToEat(self):
    # If the cat was fed in the last 6 hours, she doesn't need more
    sixHoursAgo = datetime.now() - timedelta(hours=6)
    if self.feeder.catLastFed == None:
     Log.info("last fed? last fed: {x} 6 hours ago: {y} comparison: n/a".format(x=self.feeder.catLastFed,y=sixHoursAgo))
    else:
     Log.info("last fed? last fed: {x} 6 hours ago: {y} comparison: {z}".format(x=self.feeder.catLastFed,y=sixHoursAgo, z=self.feeder.catLastFed >= sixHoursAgo))
    return self.feeder.catLastFed == None or self.feeder.catLastFed < sixHoursAgo

  def runTheSystem(self):
    if self.isCatEligibleToEat():
      Log.info("FEEDING CAT NOW!!")
      self.feeder.stirFood()
      self.feeder.dispenseFood(4)
      Log.info("MISSION ACCOMPLISHED!!")

async def checkAllSensors(motionSensorA, motionSensorB):
  return motionSensorA.consistentMotionSensed("a") and motionSensorB.consistentMotionSensed("b")

def main():
  motionSensorA = MotionSensor(5)
  motionSensorB = MotionSensor(6)
  motionSensorFeeder = MotionSensorFeeder()
  Log.info("Motion sensors live!")

  try:
    while True:
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      tasks = motionSensorA.consistentMotionSensed("a"), motionSensorB.consistentMotionSensed("b")
      a, b = loop.run_until_complete(asyncio.gather(*tasks))
      loop.close()
      if a and b:
        Log.info("MOTION SENSED by both sensors")
        motionSensorFeeder.runTheSystem()
  except KeyboardInterrupt:
    motionSensorFeeder.feeder.killAllMotors()
    Log.info("Motion sensors dead")


main()
