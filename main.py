from ast import Pass
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
import WishSim
import WishStats
import project_future_wishes

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

#this is just to make sure that somehow an infinite loop occurs
iters = 0
iter_bound = 100

require_primo_options = ["Wish Statistics", "Wish Simulator", "Wish Projection"]
options = ["Wish Statistics", "Wish Simulator", "Wish Projection"]

for i in range(0,len(options)):
  print(str(i+1)+ ". --- " + options[i])

while iters < 100:
  option  = input("Please give the number corresponding to the option you want to use: ")
  if (helpers.castable_as_int(option)):
    if (int(option) in range(1,len(options)+1)):
      option = int(option)-1
      break

print("Continuing for " + options[option] + " --- Press Control+c/Command+c to cancel")

if options[option] in require_primo_options:
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
    num_primos = userinput.NUM_PRIMOS
    num_fates = userinput.NUM_FATES
    num_starglitter = userinput.NUM_STARGLITTER
    num_genesis = userinput.NUM_GENESIS
    current_pity = userinput.CURRENT_PITY
    current_guaranteed = userinput.CURRENT_GUARANTEED
    num_rateups_desired =  userinput.NUM_RATEUPS_DESIRED
    banner_end_date  = userinput.BANNER_END_DATE
  else:
    #blocks to allow users to input multiple times if the've made an error
    while iters < iter_bound:
      num_primos = input("Type your primogem total: ")
      if (helpers.castable_as_int(num_primos)):
        break
      print("------------------- Invalid response querying again -------------------")
      iters +=1

    while iters < iter_bound:
      num_fates = input("Type your intertwined fate total: ")
      if (helpers.castable_as_int(num_fates)):
        break
      print("------------------- Invalid response querying again -------------------")
      iters +=1

    while iters < iter_bound:
      num_starglitter = input("Type your num_starglitter total: ")
      if (helpers.castable_as_int(num_starglitter)):
        break
      print("------------------- Invalid response querying again -------------------")
      iters +=1

    while iters < iter_bound:
      num_genesis = input("Type your num_genesis crystal total: ")
      if (helpers.castable_as_int(num_genesis)):
        break
      print("------------------- Invalid response querying again -------------------")
      iters +=1

    if(iters > iter_bound):
      raise StopIteration("Too many failed inputs")
  total_pulls = math.floor((num_primos+num_genesis)/160)+num_fates + math.floor(num_starglitter/5)
  total_primos = num_primos+num_genesis+num_fates*160+math.floor(num_starglitter/5)*160

kwargs = {"num_primos": num_primos, "num_fates": num_fates, "num_genesis": num_genesis, "num_starglitter": num_starglitter, 
  "current_pity": current_pity, "current_guaranteed": current_guaranteed, "num_rateups_desired": num_rateups_desired, "banner_end_date": banner_end_date}
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


if options[option] == "Wish Statistics":
  WishStats.main(kwargs)
  pass
elif options[option] == "Wish Simulator":
  WishSim.main(kwargs)
  pass
elif options[option] ==  "Wish Projection":
  project_future_wishes.main(kwargs)
  pass
