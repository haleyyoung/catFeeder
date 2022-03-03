import RPi.GPIO as GPIO
import board
import asyncio
from utilities import Log
from catFeeder import CatFeeder

class TestConnections:
  def __init__(self, pin):
    self.feeder = CatFeeder()

  def test(self):
    print("motor 1 #{self.feeder.motor1.throttle}")
    print("motor 2 #{self.feeder.motor2.throttle}")
    print("motor 3 #{self.feeder.motor3.throttle}")
    print("motor 4 #{self.feeder.motor4.throttle}")

TestConnections().test()