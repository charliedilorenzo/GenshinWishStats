import sys
sys.path.append("..")
from asyncore import read
import math
import consts
from os.path import exists
from matplotlib.cbook import print_cycles
from WishStats import WishStats
from project_future_wishes import project_future_wishes
from datetime import date, datetime
import helpers
import read_files

# ===========================================================================================================================================================================================
#  MISC INITIALIZATION
# ===========================================================================================================================================================================================
currentDay = datetime.now().day
currentDate = datetime.now().date()
currentVersion = 2.6
percentage_breakdown_folder = 'percentage_breakdown_files/'

# ===========================================================================================================================================================================================
#  PRIMOGEM INFO
# ===========================================================================================================================================================================================
current_pity = consts.CURRENT_PITY
current_guaranteed = consts.CURRENT_GUARANTEED

num_wishes = consts.NUM_WISHES
num_primos = consts.NUM_PRIMOS
num_starglitter = consts.NUM_STARGLITTER
num_genesis = consts.NUM_GENESIS

desired_five_stars = 0
desired_ru = 0
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

zero_pity_filename = percentage_breakdown_folder + 'percentage_breakdown_pity_0.csv'
current_pity_filename=  percentage_breakdown_folder + 'percentage_breakdown_pity_' + str(current_pity) + '.csv' 

print("Current Statistics:")
temp_stats = WishStats(total_pulls, desired_five_stars, desired_ru, four_rateups, four_stars, rateups, standard_five_stars,set_pity=0, set_guaranteed=False)
read_files.lookup_or_run_stats(total_pulls,temp_stats,filename=zero_pity_filename,pity=0)

#projecting primos for an banner date in the future
print()
proj_wishes =project_future_wishes(total_primos,0,0,days_until_end_date,True,False,silenced=True)
total_pulls = math.floor(proj_wishes/160)
print("Days Until Banner: {0}, Version Number: {1}".format(days_until_end_date,"2.9"))
print("No Pity + No Starglitter+Proj: {0}".format(total_pulls))
temp_stats = WishStats(total_pulls, desired_five_stars, desired_ru, four_rateups, four_stars, rateups, standard_five_stars,set_pity=0, set_guaranteed=False)
read_files.lookup_or_run_stats(total_pulls,temp_stats,filename=zero_pity_filename,pity=0)


starglitter_from_wishes = helpers.starglitter_back(total_pulls)
with_starglitter = math.floor(starglitter_from_wishes/5) + total_pulls

print()
print("No Pity + Starglitter+Proj: {0}".format(with_starglitter))
temp_stats = WishStats(with_starglitter, desired_five_stars, desired_ru, four_rateups, four_stars, rateups, standard_five_stars,set_pity=0, set_guaranteed=False)
read_files.lookup_or_run_stats(with_starglitter,temp_stats,filename=zero_pity_filename,pity=0)

# print()
# print("Pity + Starglitter+Proj: Pulls= {0}, Pity={1}, Guaranteed={2}".format(with_starglitter,current_pity,current_guaranteed))
# stats = WishStats(with_starglitter, desired_five_stars, desired_ru, four_rateups, four_stars, rateups, standard_five_stars,set_pity=current_pity, set_guaranteed=current_guaranteed)
# stats.run_stats(trials)
# stats.print_stats()
# print()
# stats.breakdown_percent_rateups()
# print()
# print(stats.tally_per_ru)

print()
print("Pity + Starglitter+Proj: Pulls= {0}, Pity={1}, Guaranteed={2}".format(with_starglitter,current_pity,current_guaranteed))
temp_stats = WishStats(with_starglitter, desired_five_stars, desired_ru, four_rateups, four_stars, rateups, standard_five_stars,set_pity=current_pity, set_guaranteed=current_guaranteed)
read_files.lookup_or_run_stats(with_starglitter,temp_stats,filename=current_pity_filename,pity=current_pity)

#projecting primos for an extra update in the future
days_until_end_date = days_until_end_date+42
proj_wishes =project_future_wishes(total_primos,0,0,days_until_end_date,True,False,silenced=True)
total_pulls = math.floor(proj_wishes/160)
starglitter_from_wishes = helpers.starglitter_back(total_pulls)
with_starglitter = math.floor(starglitter_from_wishes/5) + total_pulls
print()
print("Days Until Banner: {0}, Version Number: {1}".format(days_until_end_date,"2.10"))

print()
print("No Pity + Starglitter+Proj: {0}".format(with_starglitter))
temp_stats = WishStats(with_starglitter, desired_five_stars, desired_ru, four_rateups, four_stars, rateups, standard_five_stars,set_pity=0, set_guaranteed=False)
read_files.lookup_or_run_stats(with_starglitter,temp_stats,filename=zero_pity_filename,pity=0)

# print()
# print("Pity + Starglitter+Proj: Pulls= {0}, Pity={1}, Guaranteed={2}".format(with_starglitter,current_pity,current_guaranteed))
# stats = WishStats(with_starglitter, desired_five_stars, desired_ru, four_rateups, four_stars, rateups, standard_five_stars,set_pity=current_pity, set_guaranteed=current_guaranteed)
# stats.run_stats(trials)
# stats.print_stats()
# print()
# stats.breakdown_percent_rateups()
# print()
# print(stats.tally_per_ru)

print()
print("Pity + Starglitter+Proj: Pulls= {0}, Pity={1}, Guaranteed={2}".format(with_starglitter,current_pity,current_guaranteed))
temp_stats = WishStats(with_starglitter, desired_five_stars, desired_ru, four_rateups, four_stars, rateups, standard_five_stars,set_pity=current_pity, set_guaranteed=current_guaranteed)
read_files.lookup_or_run_stats(with_starglitter,temp_stats,filename=current_pity_filename,pity=current_pity)