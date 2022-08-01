from re import I
from numpy import full
import WishSim
import WishStats
import helpers
import userinput
import consts
import math

def main(user_data, action_list):
    full_action_list = []
    action_list = helpers.generate_abbreviations(action_list)
    for item in action_list:
        full_action_list.extend(helpers.generate_cases(item))
    
    
    order = []
    while order != []:
        action = order.pop(-1)
        # the outputs should be formated as a user_data dictionary
        output = action()

    return 0

def character_then_weapon_stats(total_pulls = 0, character_copies = 7, weapon_copies = 1, character_pity = 0, character_guaranteed = 0, weapon_pity = 0, weapon_guaranteed = 0, epitomized_path = 0, silenced = True, trials = 10000):
    character_successes = {True: 0, False:0}
    weapon_sucesses = {True:0,False:0}
    character_rateup_count = { i : 0 for i in range(0,character_copies+1) }
    weapon_rateup_count = { i : 0 for i in range(0,weapon_copies+1) }
    pulls_remaining = {}
    for i in range(0,trials):
        output = character_then_weapon_sim(total_pulls = total_pulls, character_copies = character_copies, weapon_copies = weapon_copies, character_pity = character_pity, character_guaranteed = character_guaranteed, 
                                    weapon_pity = weapon_pity, weapon_guaranteed = weapon_guaranteed, epitomized_path = epitomized_path, silenced = silenced)
        #output -> {"character_goal_achieved": character_goal_achieved, "weapon_goal_achieved": weapon_goal_achieved, "character_rateup_count": character_wish_sim.rateup_count,
        #                                         "weapon_rateup_count": weapon_wish_sim.rateup_count, "wishes_remaining": total_pulls}
        character_successes[output["character_goal_achieved"]]+=1
        weapon_sucesses[output["weapon_goal_achieved"]]+=1
        character_rateup_count[output["character_rateup_count"]]+=1
        if ("weapon_rateup_count" in output.keys()):
            weapon_rateup_count[output["weapon_rateup_count"]]+=1
        if output["wishes_remaining"] in pulls_remaining.keys():
            pulls_remaining[output["wishes_remaining"]]+=1
        else:
            pulls_remaining[output["wishes_remaining"]]=1
    helpers.combined_weapon_to_breakdown(character_successes,weapon_sucesses, character_rateup_count, weapon_rateup_count,trials)
    return character_successes,weapon_sucesses, character_rateup_count, weapon_rateup_count

def character_then_weapon_sim(total_pulls = 0, character_copies = 7, weapon_copies = 1, character_pity = 0, character_guaranteed = 0, weapon_pity = 0, weapon_guaranteed = 0, epitomized_path = 0, silenced = True ):
    # this is good for putting on return I think
    character_goal_achieved = False
    weapon_goal_achieved = False

    # grabbing consts
    four_stars = consts.FOUR_STAR_CHARACTERS+consts.FOUR_STAR_WEAPONS
    banner_end_date  = userinput.BANNER_END_DATE

    # initialize values
    if total_pulls == 0:
        num_primos = userinput.NUM_PRIMOS
        num_fates = userinput.NUM_FATES
        num_starglitter = userinput.NUM_STARGLITTER
        num_genesis = userinput.NUM_GENESIS
        total_pulls = math.floor((num_primos+num_genesis)/160)+num_fates + math.floor(num_starglitter/5)
    else:
        total_pulls = total_pulls
    current_pity = character_pity
    current_guaranteed = character_guaranteed
    
    if not silenced:
        print()
        helpers.print_messaged_banner("CHARACTER BANNER", mode="triple_line")
        print()
    # --------------------------- CHARACTER BANNER PART ---------------------------
    ru_five_stars = ["Baizhu"]
    ru_four_stars = ["Partner for Baizhu"]
    desired_five_star = "Baizhu"
    desired_ru =  character_copies
    five_stars = consts.STANDARD_FIVE_STAR_CHARACTERS

    banner_type = "character"
    character_wish_sim = WishSim.WishSim(ru_four_stars, four_stars, ru_five_stars, five_stars, desired_five_star = desired_five_star,  banner_type = banner_type)
    character_wish_sim.roll(total_pulls, 0, desired_ru, silenced = silenced, set_pity = current_pity,set_guaranteed=current_guaranteed)
    # we calculate how many pulls we have left from the other one
    character_guaranteed= character_wish_sim.guaranteed
    character_pity = character_wish_sim.pity
    wishes_used = character_wish_sim.number_pulled
    total_pulls = total_pulls-wishes_used
    if not silenced:
        print()
        helpers.print_messaged_banner("WEAPON BANNER", mode="triple_line")
        print()

    if character_wish_sim.rateup_count >= desired_ru:
        character_goal_achieved = True

    return_package = {}
    if total_pulls > 0:
        # the rest is already known
        current_pity = weapon_pity
        current_guaranteed = weapon_guaranteed
        ru_five_stars = ["Baizhu Weapon", "Other Crappy Weapon"]
        ru_four_stars = []
        desired_five_star = "Baizhu Weapon"
        desired_ru =  weapon_copies
        five_stars = consts.STANDARD_FIVE_STAR_WEAPONS
        banner_type = "weapon"
        weapon_wish_sim = WishSim.WishSim(ru_four_stars, four_stars, ru_five_stars, five_stars, desired_five_star = desired_five_star,  banner_type = banner_type)
        weapon_wish_sim.roll(total_pulls, 0, desired_ru, silenced = silenced, set_pity = current_pity,set_guaranteed=current_guaranteed)
        weapon_guaranteed = weapon_wish_sim.guaranteed
        weapon_pity = weapon_wish_sim.pity
        wishes_used = weapon_wish_sim.number_pulled
        total_pulls = total_pulls - wishes_used
        if weapon_wish_sim.rateup_count >= desired_ru:
            weapon_goal_achieved = True
        return_package.update({"weapon_rateup_count": weapon_wish_sim.rateup_count,})

    return_package.update({"character_goal_achieved": character_goal_achieved, "weapon_goal_achieved": weapon_goal_achieved, "character_rateup_count": character_wish_sim.rateup_count,
                         "wishes_remaining": total_pulls })
    return return_package


def script(silenced = True):
    current_pity = userinput.CURRENT_PITY
    current_guaranteed = userinput.CURRENT_GUARANTEED
    character_then_weapon_sim(character_copies=7,weapon_copies=1, character_pity=current_pity,character_guaranteed= current_guaranteed,silenced=silenced)

if __name__ == "__main__":
    script()