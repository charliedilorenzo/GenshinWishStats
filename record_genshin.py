from turtle import update
import matplotlib.pyplot as plt
import numpy as np
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
from datetime import datetime
import time

DEFAULT_COLUMN_LABELS = ["Wishes Available", "X","C0","C1","C2","C3","C4","C5","C6"]

def record_primos(current_update_version, updates_into_future, currrent_primo_num, filename, banner_end_date=datetime.today().date(), welkin_moon=True, battlepass=False):
    currentDate = datetime.today().date()
    update_version = float(current_update_version) + updates_into_future*0.1
    current_txt = "Record of primos on {date}, Version {update_version}\n".format(date=currentDate,update_version = current_update_version)
    future_txt = "Projection of primos on {date} for Baizhu in end of {update_version}\n".format(date=currentDate,update_version = update_version)
    with open(filename, 'a') as f:
        f.write(current_txt)
        f.write(str(currrent_primo_num))
        f.write("\n")
    if (banner_end_date != currentDate):
        day_difference = banner_end_date- currentDate
        day_difference = int(divmod(day_difference.total_seconds(), 86400)[0])
        future_primo_num = project_future_wishes(currrent_primo_num,0,0,days_till_end_of_banner=day_difference, welkin_moon=welkin_moon, battlepass= battlepass,silenced=True)
    elif(updates_into_future >0):
        days_till_end_of_banner =  42*updates_into_future
        future_primo_num = project_future_wishes(currrent_primo_num,0,0,days_till_end_of_banner=days_till_end_of_banner, welkin_moon=welkin_moon, battlepass= battlepass)
    with open(filename, 'a') as f:
        f.write(future_txt)
        f.write(str(future_primo_num ))
        f.write("\n")
        f.write("\n")
    print(current_txt)
    print(currrent_primo_num)
    print(future_txt)
    print(future_primo_num)

def record_percentage_breakdown(trials, filename='percentage_breakdown.csv',column_description_list=DEFAULT_COLUMN_LABELS,timer=True, five_stars_desired=0, guaranteed_desired=0,pity=0):
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # WRITE TO EXTERNAL FILE BREAKDOWN OF PERCENTAGE AT EACH CONSTELLATION PER AMOUNT OF WISHES
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    percentage_breakdown_folder = 'percentage_breakdown_files/'
    timer_filename = consts.TIMER_FOLDER+filename.replace(".csv","_timer.csv")
    filename = percentage_breakdown_folder+filename
    string_column_description = ""
    for column in column_description_list:
        string_column_description+=column+","
    string_column_description = string_column_description[0:len(string_column_description)-1]
    string_column_description = string_column_description + "   SKIP\n"
    current_wishes = 1
    # check if we have previous data
    if(timer and not exists(timer_filename)):
        with open(timer_filename, 'w') as f:
            f.write("Pity,Time(s)   SKIP\n")
    if (not exists(filename)):
        print("--------------------------- CREATING NEW FILE --------------------------- ")
        with open(filename, 'w') as f:
            f.write("Trials = " + str(trials)+ "   SKIP" + "\n")
            f.write(string_column_description)
    else:
        print("------------------------------ CONTINUING ------------------------------ ")
        with open(filename, 'r') as f:
            for line in f:
                if line == "":
                    last_line = line
                    break
                pass
                last_line = line
        if (',' in last_line):
            #split the line by colons and target the one that will give us the current wishes
            splitting = last_line.split(',')
            current_wishes = int(re.sub("[^0-9]", "", splitting[0]))+1
    print("-------------- Starting with Wish Num: {0} --------------".format(current_wishes))
    j = current_wishes
    for j in range(current_wishes,1000):
        if(timer):
            starttime = time.perf_counter()
        output_string = str(j)
        total_pulls = j
        stats = WishStats(total_pulls, five_stars_desired, guaranteed_desired, ["Barbara", "Beidou", "Bennett"], consts.FOUR_STARS, ["Generic"], consts.STANDARD_FIVE_STARS,set_pity=pity)
        stats.run_stats(trials)
        with NoStdStreams():
            ratio_list = stats.breakdown_percent_rateups()
            #show proper amount of digits in float (probably too many)
            ratio_list = ["%.4f" % r for r in ratio_list]
            #make sure things are spaced evenly
            for k in range(0,8):
                #make sure things are spaced evenly
                output_string +=  "," + str(ratio_list[k])
        output_string += "\n"
        with open(filename, 'a') as f:
            f.write(output_string)
        if(timer):
            endtime = time.perf_counter()
            time_diff = endtime-starttime
            with open(timer_filename, 'a') as f:
                timer_string = str(j)+","+str(time_diff)+"\n"
                f.write(timer_string)
            print("----- Recorded Wish Num: {0} ---------- Time Taken: {1}s -----".format(j,time_diff))
        else:
            print("----- Recorded Wish Num: {0} -----".format(j))
    print()
    print("----------------------- COMPLETE - STOPPED AT WISH NUM {0} -----------------------".format(j))