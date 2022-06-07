from cProfile import label
import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import io
import os
import re
from os.path import exists
from datetime import date, datetime
import math
import consts

def get_banner_of_type(banner_type):
  # this we can do since we store that in a const file, however in the future might be better to store it in file
  if (banner_type == "character"):
    return consts.STANDARD_FIVE_STAR_CHARACTERS
  elif(banner_type == "weapon"):
    return consts.STANDARD_FIVE_STAR_WEAPONS
  else:
    return consts.STANDARD_FIVE_STAR_CHARACTERS

def print_messaged_banner(message, length = -1, mode = "single_line"):
  if length == -1:
    length = consts.UNIVERSAL_FORMAT_LENGTH
  remaining_length = length - len(message)
  divided = math.floor(remaining_length/2)
  # so that we always have length the same for all lines (not fully symmetrical for message line though)
  extra = ""
  if len(message)+2*divided != length:
    extra = "-"
  #for padding
  divided = divided-1
  if mode == "triple_line":
    print("-"*length)
    print("-"*divided,"{:^1}".format(message),"-"*divided+extra)
    print("-"*length)
  #single line for default
  else:
    print("-"*divided,"{:^1}".format(message),"-"*divided+extra)

def take_phrase_in_list(message,list,failure_response = None, iter_bound = 100):
  iters = 0
  response = "Error"
  while iters < iter_bound:
    temp = input(message)
    if (temp in list):
      response = temp
      break
    elif failure_response is not None:
      print_messaged_banner(failure_response)
  return response

def take_yn_as_input(message, failure_response = None, iter_bound = 100):
  response = False
  iters = 0
  while iters < iter_bound:
    response = input(message)
    if (response in consts.YES_RESPONSES):
      response = True
      break
    elif (response in consts.NO_RESPONSES):
      response = False
      break
    elif failure_response is not None:
      print_messaged_banner(failure_response)
  return response

def take_int_as_input(message, failure_response = None, iter_bound = 100, range = None):
  iters = 0
  response = "Error"
  while iters < iter_bound:
    temp = input(message)
    if (castable_as_int(temp)):
      if (range is None or int(temp) in range):
        response = int(temp)
        break
    if failure_response is not None:
      print_messaged_banner(failure_response)
  if(iters > iter_bound or temp == "Error"):
      raise StopIteration("Too many failed inputs")
  return response

def total_primos(raw_primos, raw_fates, num_genesis, raw_starglitter):
  total_primos = raw_primos+num_genesis+raw_fates*160+math.floor(raw_starglitter/5)*160
  return total_primos

def castable_as_int(string):
  try:
    int(string)
    return True
  except ValueError:
    return False

def justify_csv_double_layered_list(matrix, labels, extra_spaces=4):
  #justify based on the maximum length string found per column
  max_length_list = []
  for i in range(0,len(labels)):
    max_length_list.append(len(labels[i]))
  length = len(max_length_list)
  for list in matrix:
    for i in range(0,length):
      if max_length_list[i] < len(str(list[i])):
        max_length_list[i] = len(str(list[i]))
  for i in range(0,length):
    labels[i] = (str(labels[i])).ljust(max_length_list[i]+extra_spaces)

  for i in range(0,len(matrix)):
    for j in range(0,length):
      matrix[i][j] = (str(matrix[i][j])).ljust(max_length_list[j]+extra_spaces)
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