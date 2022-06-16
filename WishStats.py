import consts
from os.path import exists
from NoStreamObj import NoStdStreams
import consts
from WishSim import WishSim
from matplotlib.cbook import print_cycles
from NoStreamObj import NoStdStreams
import helpers
import math
import userinput

def main(user_data):
  four_stars = consts.FOUR_STAR_CHARACTERS + consts.FOUR_STAR_WEAPONS
  five_stars = helpers.get_banner_of_type(user_data["banner_type"])
  num_wishes = math.floor(helpers.total_primos(user_data["num_primos"],user_data["num_fates"], user_data["num_genesis"], user_data["num_starglitter"])/160)

  wishstat = WishStats(num_wishes, 0, user_data["desired_ru"], userinput.RU_FOUR_STARS, four_stars, userinput.RU_FIVE_STARS, five_stars, user_data["current_pity"],user_data["current_guaranteed"],banner_type=user_data["banner_type"])
  print()
  print()
  print("How many trials should be done?")
  trials = helpers.take_int_as_input("(more takes longer and gives more accurate averages and medians, but less accurate mins/maxs):   ")
  print()
  print()
  print("Press Control+C or Command+C to cancel. It may take a minute or two")
  print()
  print()
  wishstat.run_stats(trials)
  wishstat.print_stats()
  #silence it
  with NoStdStreams():
    ratio_list = wishstat.breakdown_percent_rateups()
  ratio_list = ["%.4f" % r for r in ratio_list]
  ratio_list = [[r+"%" for r in ratio_list]]
  labels = [ "X","C0","C1","C2","C3","C4","C5","C6"]
  string,labels = helpers.justify_csv_double_layered_list(ratio_list, labels)
  print("X = Didn't get the rateup")
  print(" ".join(labels))
  for line in string:
    print(" ".join(line))
class WishStats:
  def __init__(self,num_wishes, five_stars_desired, guaranteed_desired, ru_four_stars, four_stars, ru_five_star, five_stars,  set_pity = 0,set_guaranteed=False,banner_type = "character"):
    self.total_pulls = 0
    self.tally_per_ru = { i : 0 for i in range(0,8) }
    self.tally_per_five_star = { i : 0 for i in range(0,15) }
    self.tally_wishes_used = {}
    self.trial_num = 0
    self.init_pity = set_pity
    self.init_guaranteed = set_guaranteed
    self.wish_sim = WishSim(ru_four_stars, four_stars, ru_five_star, five_stars,banner_type=banner_type)

    self.wishes_per_trial = num_wishes
    self.five_stars_desired = five_stars_desired
    if (five_stars_desired > 14):
      self.five_stars_desired = 14
    else:
      self.five_stars_desired = five_stars_desired
    if (guaranteed_desired > 7):
      self.guaranteed_desired = 7
    else:
      self.guaranteed_desired = guaranteed_desired
    self.ru_four_stars = ru_four_stars
    self.four_stars = four_stars
    self.ru_five_star = ru_five_star
    self.five_stars = five_stars

  def get_wish_sim(self):
    return self.wish_sim

  def update_wishes_used(self, num_wished):
    if (num_wished in self.tally_wishes_used.keys()):
      self.tally_wishes_used[num_wished] += 1
    else:
      self.tally_wishes_used[num_wished] = 1

  def run_stats(self, num_trials):
    five_stars_acquired  = 0
    for i in range(0,num_trials):
      with NoStdStreams():
        self.wish_sim.reset_pulls()
        [wishes_used, five_stars_acquired, ru_acquired] = self.wish_sim.roll(self.wishes_per_trial, self.five_stars_desired, self.guaranteed_desired, silenced= True, set_pity=self.init_pity,set_guaranteed=self.init_guaranteed)
        self.update_wishes_used(wishes_used)
        self.total_pulls += wishes_used
        self.tally_per_ru[ru_acquired] +=1
        self.tally_per_five_star[five_stars_acquired] +=1
    self.trial_num +=num_trials

  def average_wishes_used(self):
    sum = 0
    for i in self.tally_wishes_used.keys():
      sum += self.tally_wishes_used[i]*i
    return sum/self.trial_num

  def average_five_stars(self):
    sum = 0
    for i in self.tally_per_five_star.keys():
      sum += self.tally_per_five_star[i]*i
    return sum/self.trial_num
  
  def average_ru(self):
    sum = 0
    for i in self.tally_per_ru.keys():
      sum += self.tally_per_ru[i]*(i)
    return sum/self.trial_num

  def breakdown_percent_rateups(self):
    ratio_list = []
    print("No RU: " + str(100*self.tally_per_ru[0]/self.trial_num))
    ratio_list = [100*self.tally_per_ru[0]/self.trial_num]
    for i in range(1,8):
      ratio = 100*self.tally_per_ru[i]/self.trial_num
      print("C" + str(i-1) + ": "+ str(ratio)+ "%")
      ratio_list.append(ratio)
    return ratio_list
    
  def median_wishes_used(self):
      stop_mark = self.total_pulls/2
      running_total = 0
      for j in self.tally_wishes_used.keys():
        running_total += self.tally_wishes_used[j]*j
        if (running_total > stop_mark):
          break
        elif(running_total == stop_mark-.5):
          #this is usually incorrect for small sample size
          j = (2j+1)/2
          break
      return j


  def print_stats(self):
    
    print("PARAMETERS ----------------------------")
    print("Wishes per Trial:" + str(self.wishes_per_trial))
    print("Number of Trials:" + str(self.trial_num))
    print()

    print("WISHES USED ------------------------------")
    print("Average: "+ str(self.average_wishes_used()))
    print("Median: "+ str(self.median_wishes_used()))
    print("Min: "+ str(min(self.tally_wishes_used.keys())))
    print("Max: "+ str(max(self.tally_wishes_used.keys())))
    print()
    print("NUMBER OF 5⭐ ------------------------------")
    print("Average: "+ str(self.average_five_stars()))
    minimum = -1
    maximum = 14
    for i in range(0,15):
      if (self.tally_per_five_star[i] != 0 ):
        if minimum <= -1:
          minimum = i
        maximum = i
    print("Min: "+ str(minimum))
    print("Max: "+ str(maximum))
    print()
    print("NUMBER OF RATE UPS ------------------------------")
    print("Average: "+ str(self.average_ru()))
    minimum = -1
    maximum = 7
    for i in range(0,8):
      if (self.tally_per_ru[i] != 0 ):
        if minimum <= -1:
          minimum = i
        maximum = i
    print("Min: "+ str(minimum))
    print("Max: "+ str(maximum))
    print()