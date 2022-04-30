import RPi.GPIO as GPIO
import board
from utilities import Log
from catFeeder import CatFeeder

def main():
  onepawFeeder = CatFeeder()
  onepawFeeder.clearDirtyBowlAndDropNewBowl()

main()
