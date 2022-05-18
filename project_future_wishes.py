import random
import matplotlib.pyplot as plt
import numpy as np
import math
from os.path import exists
from consts import PROB_FIVE_STAR_AT_WISH_NUM
import helpers
from datetime import date, datetime


def project_future_wishes(current_primos, current_fates, current_starglitter, days_till_end_of_banner, welkin_moon = True, battlepass = False, current_days_into_update = -1, silenced=False):
    current_total_primos = current_primos+160*math.floor(current_starglitter/5) + 160*current_fates

    if (current_days_into_update == -1):
        current_days_into_update = helpers.days_into_update_count()
    day_in_month = datetime.now().day

    #primogems for daily commisions
    future_primos = days_till_end_of_banner*60
    #primogems for 33 stars on abyss
    future_primos += 450*math.floor((day_in_month+days_till_end_of_banner)/15)
    #primogems from stardust exchange
    future_primos += 800*math.floor((day_in_month+days_till_end_of_banner)/30)
    #primogems from announcing next update:
    future_primos += 300*math.floor((current_days_into_update+days_till_end_of_banner)/42)
    #primogems from game update compensation:
    future_primos += 300*math.floor((current_days_into_update+days_till_end_of_banner)/42)
    #primogems from bug fixing:
    future_primos += 300*math.floor((current_days_into_update+days_till_end_of_banner)/42)
    #primogems from testing characters (assumes 2 banners)
    future_primos += 80*math.floor(((current_days_into_update % 21)+days_till_end_of_banner)/21)

    # TODO reevaluate amount from event wishes https://twitter.com/SaveYourPrimos/status/1500327010354094083/photo/1 https://gamerant.com/genshin-impact-13000-primogems-calculation-in-version-24/#:~:text=Every%20six%20weeks%2C%20Genshin%20Impact,translates%20to%20around%2060%20Wishes.
    #primogems from events
    future_primos += 1500*math.floor((current_days_into_update+days_till_end_of_banner)/42)

    if(battlepass == True):
        future_primos += 1320*math.floor((current_days_into_update+days_till_end_of_banner)/42)
    if(welkin_moon == True):
        future_primos += days_till_end_of_banner*90
    if (not silenced):
        print("Wishes: " + str(math.floor((future_primos+current_total_primos)/160)))
        print("Primos: " + str(future_primos+current_total_primos))
    return future_primos+current_total_primos