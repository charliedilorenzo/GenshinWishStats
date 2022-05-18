from cProfile import label
import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import io
import os
import re
from os.path import exists
from consts import PROB_FIVE_STAR_AT_WISH_NUM
from datetime import date, datetime
import math

def justify_csv_double_layered_list(matrix, labels, extra_spaces=4):
  #initialize list with indices
  # max_length_list = [0 for i in range(0,100)]
  max_length_list = []
  for i in range(0,len(labels)):
    max_length_list.append(len(labels[i]))
  length = len(max_length_list)
  for list in matrix:
    for i in range(0,length):
      if max_length_list[i] < len(str(list[i])):
        max_length_list[i] = len(str(list[i]))
  test = ""
  for i in range(0,length):
    labels[i] = (str(labels[i])+",").rjust(max_length_list[i]+extra_spaces)
    test += labels[i]
  print(test)

  for i in range(0,len(matrix)):
    test = ""
    for j in range(0,length):
      matrix[i][j] = (str(matrix[i][j])+",").rjust(max_length_list[j]+extra_spaces)
      test += str(matrix[i][j])
    print(test)
  return matrix,labels

def objective(x, a, b):
	return a * x + b

def cos_func(x, D, E):
    y = D*np.cos(E*x)
    return y

def Gauss(x, A, B):
  y = A*np.exp(-1*B*x**2)
  return y

def y__random_under_one(y):
  x = random.uniform(0,1)
  return x <= y

def days_into_update_count():
  currentDay = datetime.today().date()
  update_marker = date(2022,2,16)
  in_between = currentDay - update_marker

  days_between = int(divmod(in_between.total_seconds(), 86400)[0])
  days_into_update = days_between % 42
  return days_into_update

def starglitter_back(num_wishes):
  #this function takes worst case scenario and assumes you have at least one copy of every 4 star and 5 star (on standard banner)

  #divide into amount of ten pulls
  ten_pulls = math.floor(num_wishes/10)

  #divide into small amount of pulls and large amount
  four_star_ten_pulls = ten_pulls - math.floor(ten_pulls/9)
  five_star_ten_pulls = math.floor(ten_pulls/9)
  
  #calculate starglitter
  starglitter = four_star_ten_pulls*2 + max(0,(five_star_ten_pulls-1)*10)
  return starglitter