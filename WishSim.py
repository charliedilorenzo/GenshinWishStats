import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import io
import os
import re
from os.path import exists
from NoStreamObj import NoStdStreams
from consts import PROB_FIVE_STAR_AT_WISH_NUM
from helpers import y__random_under_one

class WishSim:

  def __init__(self, ru_four_stars, four_stars, ru_five_stars, five_stars):
    self.five = "5⭐⭐⭐⭐⭐"
    self.four = "4⭐"
    self.prob_at_value = PROB_FIVE_STAR_AT_WISH_NUM
    
    self.ru_four_stars = ru_four_stars
    self.four_stars = four_stars
    self.ru_five_stars = ru_five_stars
    self.five_stars = five_stars

    self.guaranteed = False
    self.four_guaranteed = False
    self.pity = 0
    self.four_pity = 0
    self.number_pulled = 0
    self.five_tally = { i : 0 for i in (list(set(self.ru_five_stars + self.five_stars))) }
    self.four_tally = { i : 0 for i in (list(set(self.ru_four_stars + self.four_stars))) }

  def print_for_char(self, char):
    if (char in self.five_tally.keys()):
      print(char + " #: " + str(self.five_tally[char]))
    elif (char in self.four_tally.keys()):
      print(char + " #: " + str(self.four_tally[char]))
    else:
      print("Character not found.")

  def num_five_stars_pulled(self):
    sum = 0
    for i in self.five_tally.keys():
      sum += self.five_tally[i]
    return sum

  def num_four_stars_pulled(self):
    sum = 0
    for i in self.four_tally.keys():
      sum += self.four_tally[i]
    return sum
  
  def ru_count(self, name_of_rateup = None):
    if name_of_rateup is not None:
      return self.five_tally[name_of_rateup]
    else:
      sum = 0
      for i in self.ru_five_stars:
        sum+= self.five_tally[i]
      return sum

  def reset_pulls(self):
    self.guaranteed = False
    self.four_guaranteed = False
    self.pity = 0
    self.four_pity = 0
    self.total_pulls = 0
    self.number_pulled = 0
    self.five_tally = { i : 0 for i in (list(set(self.ru_five_stars + self.five_stars))) }
    self.four_tally = { i : 0 for i in (list(set(self.ru_four_stars + self.four_stars))) }

  def generate_five_star(self, silenced = False):
    # this is to check if we win 50/50, it will still run if we have guaranteed but it will not overwrite
    if (y__random_under_one(.5)):
      self.guaranteed = True
    if (self.guaranteed):
      choice = random.choice(self.ru_five_stars)
      if not silenced:
        print(self.five+choice+" - Rolls Left: "+str(self.number_pulled)+" - Pity: "+str(self.pity))
      self.five_tally[choice] +=1
      self.guaranteed = False
    else:
      choice = random.choice(self.five_stars)
      if not silenced:
        print(self.five+choice+" - Rolls Left: "+str(self.number_pulled)+" - Pity: "+str(self.pity))
      self.five_tally[choice] +=1
      self.guaranteed = True
    self.pity = 0
    self.four_pity = 0

  def generate_four_star(self, silenced = False):
    if (y__random_under_one(.5)):
      self.four_guaranteed = True
    if (self.four_guaranteed):
      choice = random.choice(self.ru_four_stars)
      if not silenced:
        print(self.four+choice+" - Rolls Left: "+str(self.number_pulled)+" - Pity: "+str(self.pity))
      self.four_tally[choice] +=1
      self.four_guaranteed = False
    else:
      choice = random.choice(self.four_stars)
      if not silenced:
        print(self.four+choice+" - Rolls Left: "+str(self.number_pulled)+" - Pity: "+str(self.pity))
      self.four_tally[choice] +=1
      self.four_guaranteed = True
    self.four_pity = 0

  def roll(self, num_wishes, five_stars_desired, guaranteed_desired, silenced = False, set_pity = 0,set_guaranteed=False):
    #cap them out, this is meaningless since if any of these numbers are about 15 they will break out of loop anyways
    self.guaranteed=set_guaranteed
    self.pity = set_pity
    if (five_stars_desired == 0):
      five_stars_desired = 100000
    if (guaranteed_desired == 0):
      guaranteed_desired = 100000
    begin_wishes = num_wishes
    five_stars_acquired = 0
    while (five_stars_desired > five_stars_acquired and guaranteed_desired > self.ru_count() and self.number_pulled < begin_wishes and self.ru_count() < 7 and five_stars_acquired < 14):
      num_wishes -= 1
      self.pity+=1
      self.four_pity +=1
      self.number_pulled+=1
      # 5 star block
      if (y__random_under_one(0.006) and self.pity < 74):
        self.generate_five_star(silenced=silenced)
        five_stars_acquired+=1
        continue
      if (self.pity >= 74):
        if (y__random_under_one(self.prob_at_value[self.pity])):
          self.generate_five_star(silenced=silenced)
          five_stars_acquired+=1
          continue
      #this shouldnt ever be run but just in case
      if (self.pity >= 90):
        self.generate_five_star(silenced=silenced)
        five_stars_acquired+=1
        continue

      # 4 star block - not too sure about the values here
      if (self.four_pity >= 10):
        self.generate_four_star(silenced=silenced)
        continue
      elif (self.four_pity == 9):
        if (y__random_under_one(.3688)):
          self.generate_four_star(silenced=silenced)
          continue
      else:
        if (y__random_under_one(.051)):
          self.generate_four_star(silenced=silenced)
          continue

    wishes_used = begin_wishes - num_wishes
    four_stars_acquired = self.num_four_stars_pulled()
    if not silenced:
        print()
        print("Wishes Left: " + str(num_wishes))
        print("Wishes Used: " + str(wishes_used))
        print("5⭐ total: " +str(five_stars_acquired))
        print("Rate_up 5⭐s: " +str(self.ru_count()))
        print("4⭐ total: " +str(four_stars_acquired))
    return [wishes_used, five_stars_acquired, self.ru_count()]
