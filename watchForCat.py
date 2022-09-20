import time
import datetime
from './motionSensor.py' import MotionSensor
def main:
  motionSensorPin = 5
  motionSensor = MotionSensor(motionSensorPin)
  try:
    while True:
      if motionSensor.consistentMotionSensed()
        print("MOTION SENSED", datetime.datetime.now())
      else:
        print("motion not sensed")
      time.sleep(1)
  except KeyboardInterrupt:
    print("\nQuitting")
main()