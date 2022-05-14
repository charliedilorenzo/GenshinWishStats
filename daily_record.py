import record_genshin
from datetime import date, datetime, timedelta
import math
import consts
from project_future_wishes import project_future_wishes
from os.path import exists

num_wishes = consts.NUM_WISHES
num_primos = consts.NUM_PRIMOS
num_starglitter = consts.NUM_STARGLITTER
num_genesis = consts.NUM_GENESIS

primo_record_folder = consts.PRIMO_RECORD_FOLDER
banner_end_date_filename = primo_record_folder+'primogem_projection_over_time.txt'
one_month_filename = primo_record_folder+'primogem_projection_one_month.txt'

print(primo_record_folder+banner_end_date_filename)

total_pulls = math.floor((num_primos+num_genesis)/160)+num_wishes + math.floor(num_starglitter/5)
banner_end_date = consts.BANNER_END_DATE
record_genshin.record_primos(2.5,3, total_pulls*160,banner_end_date_filename, banner_end_date=banner_end_date, welkin_moon=True,battlepass=False)

datetimenow= datetime.now().date()

end_date = datetimenow + timedelta(days=42)

current_effective_primogems= num_wishes*160+num_primos+num_genesis+math.floor(num_starglitter/5)*160
future_primos = project_future_wishes(num_primos+num_genesis, num_wishes, num_starglitter,  42, current_days_into_update = -1, silenced=True)

output_string = ""
output_string+= (str(datetimenow)+ ",").ljust(20)
output_string+= (str(end_date) + ",").ljust(20)
output_string+= (str(current_effective_primogems)+ ",").ljust(20)
output_string+= (str(future_primos) + "\n").ljust(20)

if (not exists(one_month_filename)):
    initial_string = ""
    initial_string += ("Date Recorded"+ ",").ljust(20)
    initial_string += ("Date Projected" + ",").ljust(20)
    initial_string += ("Current Primogems"+ ",").ljust(20)
    initial_string += ("Primogems Projected" + "\n").ljust(20)
    with open(one_month_filename, 'a') as f:
        f.write(initial_string)

with open(one_month_filename, 'a') as f:
    f.write(output_string)