import record_genshin
from datetime import date, datetime, timedelta
import math
import consts
from project_future_wishes import project_future_wishes
from os.path import exists
import userinput

num_wishes = userinput.NUM_FATES
num_primos = userinput.NUM_PRIMOS
num_starglitter = userinput.NUM_STARGLITTER
num_genesis = userinput.NUM_GENESIS

primo_record_folder = consts.PRIMO_RECORD_FOLDER
banner_end_date_filename = primo_record_folder+'primogem_projection_over_time.csv'
one_month_filename = primo_record_folder+'primogem_projection_one_month.csv'

print(primo_record_folder+banner_end_date_filename)

total_pulls = math.floor((num_primos+num_genesis)/160)+num_wishes + math.floor(num_starglitter/5)
banner_end_date = userinput.BANNER_END_DATE
record_genshin.record_primos(2.5,3, total_pulls*160,banner_end_date_filename, banner_end_date=banner_end_date, welkin_moon=True,battlepass=False)

datetimenow= datetime.now().date()

end_date = datetimenow + timedelta(days=42)

current_effective_primogems= num_wishes*160+num_primos+num_genesis+math.floor(num_starglitter/5)*160
future_primos = project_future_wishes(num_primos+num_genesis, num_wishes, num_starglitter,  42, current_days_into_update = -1, silenced=True)

output_string = ""
output_string+= (str(datetimenow)+ ",")
output_string+= (str(end_date) + ",")
output_string+= (str(current_effective_primogems)+ ",")
output_string+= (str(future_primos) + "\n")

if (not exists(one_month_filename)):
    initial_string = ""
    initial_string += ("Date Recorded"+ ",")
    initial_string += ("Date Projected" + ",")
    initial_string += ("Current Primogems"+ ",")
    initial_string += ("Primogems Projected" + "\n")
    with open(one_month_filename, 'a') as f:
        f.write(initial_string)

with open(one_month_filename, 'a') as f:
    f.write(output_string)