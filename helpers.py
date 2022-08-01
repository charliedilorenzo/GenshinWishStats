from cProfile import label
from pydoc import Helper
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
from project_future_wishes import project_future_wishes
import helpers

def days_till_primo_count(primocount, welkin_moon = True, battlepass = False, current_days_into_update = -1,silenced=False):
  current_primos = 0
  current_fates = 0
  current_starglitter = 0
  #genshin probably wont last 7000 days ~ 20 years
  for i in range(0,7000):
    days_till_banner_end_date = i
    if (project_future_wishes(current_primos, current_fates, current_starglitter, days_till_banner_end_date, welkin_moon, battlepass ,current_days_into_update, silenced) >= primocount):
      return i
  return i

def combined_weapon_to_breakdown(character_successes,weapon_sucesses, character_rateup_count, weapon_rateup_count,trials):
  percentage_character_breakdown = { i :character_rateup_count[i]/trials  for i in range(0, len(character_rateup_count))}
  percentage_character_breakdown = [percentage_character_breakdown[i]*100 for i in range(0,len(percentage_character_breakdown))]
  percentage_character_breakdown = ["%.4f" % r for r in percentage_character_breakdown]
  output_string = "X: " + (str(percentage_character_breakdown[0]) + "%").ljust(10)
  for k in range(1,len(percentage_character_breakdown)):
      output_string +="C" + str(k-1) + ": " + (percentage_character_breakdown[k]+"%").ljust(10)
  helpers.print_messaged_banner("Character Banner")
  print(output_string)

  percentage_weapon_breakdown = { i :weapon_rateup_count[i]/trials  for i in range(0, len(weapon_rateup_count))}
  percentage_weapon_breakdown = [percentage_weapon_breakdown[i]*100 for i in range(0,len(percentage_weapon_breakdown))]
  percentage_weapon_breakdown = ["%.4f" % r for r in percentage_weapon_breakdown]
  output_string = "X: " + (str(percentage_weapon_breakdown[0]) + "%").ljust(10)
  for k in range(1,len(percentage_weapon_breakdown)):
      output_string +="C" + str(k-1) + ": " + (percentage_weapon_breakdown[k]+"%").ljust(10)
  helpers.print_messaged_banner("Weapon Banner")
  print(output_string)


def generate_abbreviations(word_list):
  word_list = [word_list[i].lower() for i in range(0,len(word_list))]
  length_list = [0 for i in range(0,len(word_list))]
  done_list = [False for i in range(0,len(word_list))]
  true_done_list = [True for i in range(0,len(word_list))]
  extension_list = []
  while not done_list == true_done_list:
      for i in range(0,len(word_list)):
          if(done_list[i] == True):
              continue
          length_list[i] = length_list[i]+1
          length = length_list[i]
          shared_letters = word_list[i][0:length]
          unique = True
          for compare in word_list:
              if compare[0:length] == shared_letters and compare != word_list[i]:
                  unique = False
                  break
          if unique:
              extension_list.append(shared_letters)
              done_list[i] = True
  extension_list = word_list+extension_list
  return extension_list

def generate_cases(word):
  case_list = {word}
  case_list.add(word.upper())
  case_list.add(word.lower())
  case_list.add(word.capitalize())
  return case_list

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

def take_phrase_in_list(message,phrase_dict,failure_response = None, iter_bound = 100):
  iters = 0
  response = "Error"
  while iters < iter_bound:
    temp = input(message)
    for phrase in phrase_dict.keys():
      if (temp in phrase_dict[phrase]):
        response = phrase
        break
    if response != "Error":
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

def justify_csv_double_layered_list(matrix, labels, intial_setup = False, extra_spaces=4):
  #labels are assumed to be a list
  #matrix is assumed to be a list with any amount of lists of strings of equal length in it
  #justify based on the maximum length string found per column

  if intial_setup:
    #start by stripping everything:
    for i in range(0,len(labels)):
      labels[i] = labels[i].strip()
    labels[-1] += "\n"
    for i in range(0,len(matrix)):
      for j in range(0,len(matrix[0])):
        matrix[i][j] =  matrix[i][j].strip()
    for i in range(0,len(matrix)):
      matrix[i][-1]+= "\n"
    
    max_length_list = []
    for i in range(0,len(labels)):
      max_length_list.append(len(labels[i]))
    length = len(max_length_list)
    for list in matrix:
      for i in range(0,length):
        if max_length_list[i] < len(str(list[i])):
          max_length_list[i] = len(str(list[i]))
    
    for i in range(0,len(max_length_list)):
      max_length_list[i]+=extra_spaces

    for i in range(0,length):
      if (labels[i][-1] == "\n"):
        temp = (str(labels[i][0:len(labels[i])-1])).rjust(max_length_list[i]-1)
        temp = temp + "\n"
        labels[i] = temp
      else:
        labels[i] = (str(labels[i])).rjust(max_length_list[i])

    for i in range(0,len(matrix)):
      for j in range(0,length):
        if (matrix[i][j][-1] == "\n"):
          temp = (str(matrix[i][j][0:len(matrix[i][j])-1])).rjust(max_length_list[j]-1)
          temp = temp + "\n"
          matrix[i][j] = temp
        else:
          matrix[i][j] = (str(matrix[i][j])).rjust(max_length_list[j])
  #case where we already have the labels
  else:
    #look at the labels to find out justification
    max_length_list = []
    for i in range(0,len(labels)):
      max_length_list.append(len(labels[i]))
    length = len(max_length_list)
    #then use those to justify properly
    for i in range(0,len(matrix)):
      for j in range(0,length):
        if (matrix[i][j][-1] == "\n"):
          temp = (str(matrix[i][j][0:len(matrix[i][j])-1])).rjust(max_length_list[j]-1)
          temp = temp + "\n"
          matrix[i][j] = temp
        else:
          matrix[i][j] = (str(matrix[i][j])).rjust(max_length_list[j])

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