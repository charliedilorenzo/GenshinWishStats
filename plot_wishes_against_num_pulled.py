import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import io
import os
import re
from WishStats import WishStats
import consts
from os.path import exists
from NoStreamObj import NoStdStreams
from consts import PROB_FIVE_STAR_AT_WISH_NUM
from WishSim import WishSim
from helpers import y__random_under_one

def plot_wishes_against_num_pulled(trials):
  prob_at_value = PROB_FIVE_STAR_AT_WISH_NUM
  value = []
  count = []
  for i in range(1,91):
    value.append(i)
    count.append(0)

  for i in range(0,trials):
    pity = 0
    no_reset = True
    while (no_reset):
      pity+=1
      if (y__random_under_one(0.006)):
        no_reset = False
      if (pity > 73):
        if (y__random_under_one(prob_at_value[pity])):
          no_reset = False
    pity-=1
    count[pity]+=1

  total = trials

  print("Amount of 5 Stars: " + "{:,}".format(total))

  pulls = 0
  for i  in range(0,90):
    pulls = pulls + count[i]*(i+1)
  print("Amount of Pulls: " + "{:,}".format(pulls))

  largest = 0
  smallest = total+1
  for i in range(0,90):
    if (count[i] > largest):
      largest = count[i]
      maxtrack = i+1
    if (count[i] < smallest):
      smallest = count[i]
      mintrack = i+1
  print("Max: " + str(maxtrack))
  print("Min: " + str(mintrack))

  average = pulls/total
  print("Average: " + '{0:.5g}'.format(average))

  median = 0
  halfway = total/2
  current = 0
  i = 0
  while current <= halfway and i < 90:
    current = current + count[i]
    i+=1
  if current == halfway:
    median = (2*i+1)/2
  else:
    median = i+1
  print("Median: " + str(median))

  print(value)
  print(count)

  fig = plt.figure()
  v= count
  plt.plot(v, linestyle='-',linewidth=5.0, c='c')
  # ax = fig.add_axes([0,0,1,1])
  # ax.bar(value,count)
  plt.xticks(np.arange(0, 91, 10))
  plt.show() 

  fig = plt.figure()
  # ax = fig.add_axes([0,0,1,1])
  # ax.bar(value[70:91],count[70:91])
  plt.xticks(range(20), value[70:91])
  plt.show() 