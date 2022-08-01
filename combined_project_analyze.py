import combined_weapon_banner
import userinput
from datetime import date, datetime
import math
import helpers
import consts
from WishStats import WishStats
from project_future_wishes import project_future_wishes
import read_files

def main():
    
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
    current_pity = userinput.CURRENT_PITY
    current_guaranteed = userinput.CURRENT_GUARANTEED

    num_wishes = userinput.NUM_FATES
    num_primos = userinput.NUM_PRIMOS
    num_starglitter = userinput.NUM_STARGLITTER
    num_genesis = userinput.NUM_GENESIS

    desired_five_stars = 0
    desired_ru = 0
    dict = {}

    total_pulls = math.floor((num_primos+num_genesis)/160)+num_wishes + math.floor(num_starglitter/5)
    total_primos = num_primos+num_genesis+num_wishes*160+math.floor(num_starglitter/5)*160
    print()
    print("Total Current Pulls: " + str(total_pulls))
    print()

    days_into_update = helpers.days_into_update_count()
    banner_end_date = userinput.BANNER_END_DATE
    days_until_end_date = (banner_end_date - currentDate)
    days_until_end_date = int(divmod(days_until_end_date.total_seconds(), 86400)[0])
    # ===========================================================================================================================================================================================
    #  BANNER INFO
    # ===========================================================================================================================================================================================
    # WE ASSUME BANNER TYPE IS CHARACTER SO NO 5 STAR WEAPONS
    banner_type = "character"
    standard_five_stars = helpers.get_banner_of_type(banner_type)
    four_star_characters = consts.FOUR_STAR_CHARACTERS
    four_star_weapons = consts.FOUR_STAR_WEAPONS
    four_stars = four_star_characters + four_star_weapons

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
    trials = 10000

    #ADD THIS IF YOU WANT MORE SPECIFIC PREDICTION
    weapon_pity = 9
    weapon_guaranteed = True
    epitomized_path = 1


    #No projections for the future
    print("Current Statistics:")
    print("No Pity + No Starglitter+Proj: {0}".format(total_pulls))
    combined_weapon_banner.character_then_weapon_stats(total_pulls=total_pulls, character_pity = 0, character_guaranteed = 0, weapon_pity=0,weapon_guaranteed=0,epitomized_path=0,silenced=True,trials=trials)

    if (current_pity != 0 or current_guaranteed == True or weapon_pity != 0 or weapon_guaranteed == True):
        print()
        print("Pity + Starglitter+Proj: Pulls= {0}, Pity={1}, Guaranteed={2}".format(total_pulls,current_pity,current_guaranteed))
        combined_weapon_banner.character_then_weapon_stats(total_pulls=total_pulls,character_pity = current_pity, character_guaranteed = current_guaranteed, weapon_pity=weapon_pity,weapon_guaranteed=weapon_guaranteed,epitomized_path=epitomized_path,silenced=True,trials=trials)


    #projecting primos for an banner date in the future
    print()
    proj_wishes = project_future_wishes(total_primos,0,0,days_until_end_date,True,False,silenced=True)
    total_pulls = math.floor(proj_wishes/160)
    print("Days Until Banner: {0}, Version Number: {1}".format(days_until_end_date,"3.0"))
    print("No Pity + No Starglitter+Proj: {0}".format(total_pulls))
    combined_weapon_banner.character_then_weapon_stats(total_pulls=total_pulls,character_pity = 0, character_guaranteed = 0, weapon_pity=0,weapon_guaranteed=0,epitomized_path=0,silenced=True,trials=trials)


    starglitter_from_wishes = helpers.starglitter_back(total_pulls)
    with_starglitter = math.floor(starglitter_from_wishes/5) + total_pulls

    print()
    print("No Pity + Starglitter+Proj: {0}".format(with_starglitter))
    combined_weapon_banner.character_then_weapon_stats(total_pulls=with_starglitter,character_pity = 0, character_guaranteed = 0, weapon_pity=0,weapon_guaranteed=0,epitomized_path=0,silenced=True,trials=trials)
    
    if (current_pity != 0 or current_guaranteed == True or weapon_pity != 0 or weapon_guaranteed == True):
        print()
        print("Pity + Starglitter+Proj: Pulls= {0}, Pity={1}, Guaranteed={2}".format(with_starglitter,current_pity,current_guaranteed))
        combined_weapon_banner.character_then_weapon_stats(total_pulls=with_starglitter,character_pity = current_pity, character_guaranteed = current_guaranteed, weapon_pity=weapon_pity,weapon_guaranteed=weapon_guaranteed,epitomized_path=epitomized_path,silenced=True,trials=trials)

    #projecting primos for an extra update in the future
    days_until_end_date = days_until_end_date+(42)*4
    proj_wishes =project_future_wishes(total_primos,0,0,days_until_end_date,True,False,silenced=True)
    total_pulls = math.floor(proj_wishes/160)
    starglitter_from_wishes = helpers.starglitter_back(total_pulls)
    with_starglitter = math.floor(starglitter_from_wishes/5) + total_pulls
    print()
    print("Days Until Banner: {0}, Version Number: {1}".format(days_until_end_date,"3.4"))

    print()
    print("No Pity + Starglitter+Proj: {0}".format(with_starglitter))
    combined_weapon_banner.character_then_weapon_stats(total_pulls=with_starglitter,character_pity = 0, character_guaranteed = 0, weapon_pity=0,weapon_guaranteed=0,epitomized_path=0,silenced=True,trials=trials)

    print()
    print("Pity + Starglitter+Proj: Pulls= {0}, Pity={1}, Guaranteed={2}".format(with_starglitter,current_pity,current_guaranteed))
    combined_weapon_banner.character_then_weapon_stats(total_pulls=with_starglitter,character_pity = current_pity, character_guaranteed = current_guaranteed, weapon_pity=weapon_pity,weapon_guaranteed=weapon_guaranteed,epitomized_path=epitomized_path,silenced=True,trials=trials)


if __name__ == "__main__":
    main()