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
import datetime
import helpers
import userinput
import WishSim
import WishStats
import project_future_wishes

# ===========================================================================================================================================================================================
#  MISC INITIALIZATION
# ===========================================================================================================================================================================================
currentDay = datetime.datetime.now().day
currentDate = datetime.datetime.now().date()
currentVersion = 2.6

input_file = 'percentage_breakdown_mostly_correct.csv'
# ===========================================================================================================================================================================================
#  PRIMOGEM INFO
# ===========================================================================================================================================================================================

days_into_update = helpers.days_into_update_count()
banner_end_date = userinput.BANNER_END_DATE
days_till_banner_end_date = (banner_end_date - currentDate)
days_till_banner_end_date = int(divmod(days_till_banner_end_date.total_seconds(), 86400)[0])
# ===========================================================================================================================================================================================
#  BANNER INFO
# ===========================================================================================================================================================================================
standard_five_stars = consts.STANDARD_FIVE_STARS
four_stars = consts.FOUR_STARS
#some default choices can be overwritten later
ru_four_stars = ["Barbara", "Beidou", "Bennett"]
ru_five_stars = ["Baizhu"]
#Cleaning Up Inputs
for i in range(0,len(ru_four_stars)):
  item = ru_four_stars[i]
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

print()
print("------------------------------------------------------------------------------")
print("Continuing for " + options[option] + " --- Press Control+c/Command+c to cancel")
print()

user_data = {}

if options[option] in require_primo_options:
  while iters < 100:
    using_stored = input("Use values stored in \"userinput.py\"?(y/n): ")
    if (using_stored in consts.YES_RESPONSES):
      using_stored = True
      user_data["using_stored"] =using_stored
      break
    elif (using_stored in consts.NO_RESPONSES):
      using_stored = False
      break
    print("------------------- Invalid response querying again -------------------")
    iters +=1
  if using_stored:
    num_primos = userinput.NUM_PRIMOS
    num_fates = userinput.NUM_FATES
    num_starglitter = userinput.NUM_STARGLITTER
    num_genesis = userinput.NUM_GENESIS
    current_pity = userinput.CURRENT_PITY
    current_guaranteed = userinput.CURRENT_GUARANTEED
    desired_ru =  userinput.NUM_RATEUPS_DESIRED
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

user_data.update( {"num_primos": num_primos, "num_fates": num_fates, "num_genesis": num_genesis, "num_starglitter": num_starglitter,
  "current_pity": current_pity, "current_guaranteed": current_guaranteed, "desired_ru": desired_ru, "banner_end_date": banner_end_date})
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

print()
print("------------------------------------------------------------------------------")
print()

# ----------------------------------------------- WISH STATISTICS -----------------------------------------------
if options[option] == "Wish Statistics":
  num_wishes = math.floor(helpers.total_primos(user_data["num_primos"],user_data["num_fates"], user_data["num_genesis"], user_data["num_starglitter"])/160)
  WishStats.main(num_wishes, 0,user_data["desired_ru"], ru_four_stars, four_stars, ru_five_stars, standard_five_stars, current_pity, current_guaranteed)
  pass
# ----------------------------------------------- WISH SIMULATOR -----------------------------------------------
elif options[option] == "Wish Simulator":
  WishSim.main(user_data)
  pass
# ----------------------------------------------- WISH PROJECTION -----------------------------------------------
elif options[option] ==  "Wish Projection":
  iters = 0
  if ("banner_end_date" not in user_data.keys()):
    while iters < 100:
      temp = input("Name the date or a number of days from yoday you want to project for ('n' or 'm/d/y'): ")
      if (helpers.castable_as_int(temp)):
        user_data["days_till_banner_end_date"] = int(temp)
        break
      elif (temp.count(",") == 2):
        temp  = temp.split(",")
        user_data["banner_end_date"] = datetime.date(temp[2],temp[0],temp[1])
      elif (temp.count("-") == 2):
        temp  = temp.split("-")
        user_data["banner_end_date"] = datetime.date(temp[2],temp[0],temp[1])
      elif (temp.count("/") == 2):
        temp  = temp.split("/")
        user_data["banner_end_date"] = datetime.date(temp[2],temp[0],temp[1])
  elif ("banner_end_date" in user_data):
    # we find this here since its easier as an input for project_future_wishes
    days_till_banner_end_date = (user_data["banner_end_date"] - currentDate)
    days_till_banner_end_date = int(divmod(days_till_banner_end_date.total_seconds(), 86400)[0])
    user_data["days_till_banner_end_date"] = days_till_banner_end_date
  project_future_wishes.main(user_data["num_primos"], user_data["num_fates"], user_data["num_starglitter"], user_data["days_till_banner_end_date"])
  pass
