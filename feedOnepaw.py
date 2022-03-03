import time
from catFeeder import CatFeeder

def main():
  onepawFeeder = CatFeeder()
  print("FEEDING CAT NOW!!")
  onepawFeeder.clearDirtyBowl()
  onepawFeeder.dropNewBowl()
  onepawFeeder.stirFood()
  onepawFeeder.dispenseFood(4)
  print("MISSION ACCOMPLISHED!!")

main()
