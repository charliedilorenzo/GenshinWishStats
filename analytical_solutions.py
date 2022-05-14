import random
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
from helpers import y__random_under_one
from consts import PROB_FIVE_STAR_AT_WISH_NUM

class Five_Star_Analytical_Stats:

    def __init__(self, guaranteed,pity):
        self.five = "5⭐"
        self.four = "4⭐"
        self.prob_at_value = PROB_FIVE_STAR_AT_WISH_NUM
        self.guaranteed = guaranteed
        self.pity = 0
        self.number_pulled = 0
        self.soft_pity = min(PROB_FIVE_STAR_AT_WISH_NUM.keys())

    def below_soft_pity(self):
        if self.pity < self.soft_pity:
            return True
        return False

    def less_than_soft_pity_odds(self):
        x = range(0,7)
        binomial = scipy.stats.binom.pmf(x, self.soft_pity-1, 0.006)
        no_five_stars = binomial[0]
        single_five_star = binomial[1]
        sum_both = no_five_stars+single_five_star
        ratio_corrected_no_five_stars =no_five_stars/sum_both
        ratio_corrected_single_five_star = single_five_star/sum_both
        print(no_five_stars)
        print(ratio_corrected_no_five_stars)


        print(single_five_star)
        print(ratio_corrected_single_five_star)



    # y__random_under_one()