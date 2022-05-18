from asyncore import read
import math
import re
import consts
from os.path import exists
import consts
from matplotlib.cbook import print_cycles
from plot_wishes_against_num_pulled import plot_wishes_against_num_pulled
from project_future_wishes import project_future_wishes
from datetime import datetime
import helpers
import userinput

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

days_into_update = helpers.days_into_update_count()
banner_end_date = userinput.BANNER_END_DATE
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

iters = 0
iter_bound = 5

while iters < 100:
  reference_stored = input("Use values stored in \"userinput.py\"?(y/n): ")
  if (reference_stored in consts.YES_RESPONSES):
    reference_stored = True
    break
  elif (reference_stored in consts.NO_RESPONSES):
    reference_stored = False
    break
  print("------------------- Invalid response querying again -------------------")
  iters +=1
if reference_stored:
  primogems = userinput.NUM_PRIMOS
  fates = userinput.NUM_WISHES
  starglitter = userinput.NUM_STARGLITTER
  genesis = userinput.NUM_GENESIS
  current_pity = userinput.CURRENT_PITY
  current_guaranteed = userinput.CURRENT_GUARANTEED
  num_rateups_desired =  userinput.NUM_RATEUPS_DESIRED
  banner_end_date  = userinput.BANNER_END_DATE
else:
  #blocks to allow users to input multiple times if the've made an error
  while iters < iter_bound:
    primogems = input("Type your primogem total: ")
    if (helpers.castable_as_int(primogems)):
      break
    print("------------------- Invalid response querying again -------------------")
    iters +=1

  while iters < iter_bound:
    fates = input("Type your intertwined fate total: ")
    if (helpers.castable_as_int(fates)):
      break
    print("------------------- Invalid response querying again -------------------")
    iters +=1

  while iters < iter_bound:
    starglitter = input("Type your starglitter total: ")
    if (helpers.castable_as_int(starglitter)):
      break
    print("------------------- Invalid response querying again -------------------")
    iters +=1

  while iters < iter_bound:
    genesis = input("Type your genesis crystal total: ")
    if (helpers.castable_as_int(genesis)):
      break
    print("------------------- Invalid response querying again -------------------")
    iters +=1

  if(iters > iter_bound):
    raise StopIteration("Too many failed inputs")

total_pulls = math.floor((primogems+genesis)/160)+fates + math.floor(starglitter/5)
total_primos = primogems+genesis+fates*160+math.floor(starglitter/5)*160

# TODO add ability to store this data
# store_data = input("Would you like to store your primogem,etc data for future?")

# while iters < 100:
#   if (store_data in consts.YES_RESPONSES):
      # store_data = True
#     break
#   elif (store_data in consts.NO_RESPONSES):
      # store_data = False
#     break
#   print("------------------- Invalid response querying again -------------------")
#   iters +=1
