import read_files
import analytical_solutions 

read_files.wish_breakdown_lookup(300,filename='percentage_breakdown_after_fix')

stats = analytical_solutions.Five_Star_Analytical_Stats(False, 0)
stats.less_than_soft_pity_odds()

read_files.read_timer_file('percentage_breakdown_pity_53_timer.csv')
