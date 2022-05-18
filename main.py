from asyncore import read
import random
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import io
import os
import consts
from os.path import exists
from NoStreamObj import NoStdStreams
import consts
from WishSim import WishSim
from matplotlib.cbook import print_cycles
from WishStats import WishStats
from plot_wishes_against_num_pulled import plot_wishes_against_num_pulled
from project_future_wishes import project_future_wishes
import re
from datetime import date, datetime
import helpers
import record_genshin
import read_files

# ===========================================================================================================================================================================================
#  MISC INITIALIZATION
# ===========================================================================================================================================================================================
currentDay = datetime.now().day
currentDate = datetime.now().date()
currentVersion = 2.6

input_file = 'percentage_breakdown_mostly_correct.csv'
# ===========================================================================================================================================================================================
#  PRIMOGEM INFO
# ===========================================================================================================================================================================================
current_pity = consts.CURRENT_PITY
current_guaranteed = consts.CURRENT_GUARANTEED

num_wishes = consts.NUM_WISHES
num_primos = consts.NUM_PRIMOS
num_starglitter = consts.NUM_STARGLITTER
num_genesis = consts.NUM_GENESIS

desired_five_stars = 15
desired_ru = consts.NUM_RATEUPS_DESIRED
dict = {}

total_pulls = math.floor((num_primos+num_genesis)/160)+num_wishes + math.floor(num_starglitter/5)
total_primos = num_primos+num_genesis+num_wishes*160+math.floor(num_starglitter/5)*160
print()
print("Total Current Pulls: " + str(total_pulls))
print()

days_into_update = helpers.days_into_update_count()
banner_end_date = consts.BANNER_END_DATE
days_until_end_date = (banner_end_date - currentDate)
days_until_end_date = int(divmod(days_until_end_date.total_seconds(), 86400)[0])
# ===========================================================================================================================================================================================
#  BANNER INFO
# ===========================================================================================================================================================================================
standard_five_stars = consts.STANDARD_FIVE_STARS
four_stars = consts.FOUR_STARS
four_rateups = ["Barbara", "Gorou", "Xiangling"]
rateups = ["Baizhu"]
#Cleaning Up Inputs
for i in range(0,len(four_rateups)):
  item = four_rateups[i]
  four_stars.remove(item)

# ===========================================================================================================================================================================================
#  ACTION INFO
# ===========================================================================================================================================================================================

#full updates into the future
days_till_end_of_banner = 3*42 
# first banner
days_till_end_of_banner += 21 
#days left in current update
days_till_end_of_banner += (42-(days_into_update))
trials = 100000

print("Current Statistics:")
simulator = WishSim(four_rateups,four_stars,rateups,standard_five_stars)
simulator.roll(total_pulls,desired_five_stars,desired_ru,False, current_pity,current_guaranteed)

