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
four_star_characters = consts.FOUR_STAR_CHARACTERS
four_star_weapons = consts.FOUR_STAR_WEAPONS
four_stars = four_star_characters + four_star_weapons

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

for i in range(1,len(options)+1):
  print(str(i)+ ". --- " + options[i-1])

option = helpers.take_int_as_input("Please give the number corresponding to the option you want to use: ", range= range(1,len(options)+1))-1

# while iters < 100:
#   option  = input("Please give the number corresponding to the option you want to use: ")
#   if (helpers.castable_as_int(option)):
#     if (int(option) in range(1,len(options)+1)):
#       option = int(option)-1
#       break

print()
helpers.print_messaged_banner("Continuing for " + options[option] + " --- Press Control+c/Command+c to cancel", mode="triple_line")

user_data = {}
user_data["desired_five_star"] = None
if (option != str(3)):
  banner_type = helpers.take_phrase_in_list("What banner type are you interested in? (currently supported: character, weapon): ", consts.BANNER_TYPES)
  user_data.update({"banner_type":banner_type})
  if (banner_type == "weapon"):
    iter = 0
    while (iter < iter_bound):
      desired_five_star = input("What is the rate up 5 star that you want on the weapon banner? (with Epitomized Fate): ")
      is_correct = helpers.take_yn_as_input("The recorded five star is " + desired_five_star + " is that correct? ")
      if (is_correct):
        break
      iter+=1
    user_data["desired_five_star"] = desired_five_star

if options[option] in require_primo_options:
  using_stored = helpers.take_yn_as_input("Use values stored in \"userinput.py\"?(y/n): ")
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
    # function rejects responses that cannot be converted to ints
    num_primos = helpers.take_int_as_input("Type your primogem total: ")
    num_fates = helpers.take_int_as_input("Type your intertwined fate total: ")
    num_starglitter = helpers.take_int_as_input("Type your num_starglitter total: ")
    num_genesis = helpers.take_int_as_input("Type your num_genesis crystal total: ")
    current_pity = helpers.take_int_as_input("Type current pity: ")
    current_guaranteed = helpers.take_yn_as_input("Currently have guaranteed? (y/n): ")
    copy_range = range(0,8)
    desired_ru = helpers.take_int_as_input("Type amount of copies desired / number of constellations desired +1): ", range= copy_range)

    if(iters > iter_bound):
      raise StopIteration("Too many failed inputs")

user_data.update( {"num_primos": num_primos, "num_fates": num_fates, "num_genesis": num_genesis, "num_starglitter": num_starglitter,
  "current_pity": current_pity, "current_guaranteed": current_guaranteed, "desired_ru": desired_ru, "banner_end_date": banner_end_date, "banner_type": banner_type})
# TODO add ability to store this data
# store_data = input("Would you like to store your primogem,etc data for future?")

# while iters < 100:
#   if (store_data in consts.YES_RESPONSES):
      # store_data = True
#     break
#   elif (store_data in consts.NO_RESPONSES):
      # store_data = False
#     break
#   helpers.print_messaged_banner("Invalid response querying again")
#   iters +=1

print()
print("-"*consts.UNIVERSAL_FORMAT_LENGTH)
print()

# ----------------------------------------------- WISH STATISTICS -----------------------------------------------
if options[option] == "Wish Statistics":
  WishStats.main(user_data)
# ----------------------------------------------- WISH SIMULATOR -----------------------------------------------
elif options[option] == "Wish Simulator":
  WishSim.main(user_data)
# ----------------------------------------------- WISH PROJECTION -----------------------------------------------
elif options[option] ==  "Wish Projection":
  iters = 0
  if ("banner_end_date" not in user_data.keys()):
    while iters < 100:
      temp = input("Name the date or a number of days from yoday you want to project for ('n' or 'm/d/y'): ")
      if (helpers.castable_as_int(temp)):
        user_data["days_till_banner_end_date"] = int(temp)
        break
      split_characters = [",","-","/"]
      for split in split_characters:
        if (temp.count(split) == 2):
          temp  = temp.split(split)
          user_data["banner_end_date"] = datetime.date(temp[2],temp[0],temp[1])
  elif ("banner_end_date" in user_data):
    # we find this here since its easier as an input for project_future_wishes
    days_till_banner_end_date = (user_data["banner_end_date"] - currentDate)
    days_till_banner_end_date = int(divmod(days_till_banner_end_date.total_seconds(), 86400)[0])
    user_data["days_till_banner_end_date"] = days_till_banner_end_date
  project_future_wishes.main(user_data)
