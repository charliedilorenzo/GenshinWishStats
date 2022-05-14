from asyncio import constants
import record_genshin
from datetime import date, datetime
import math
import record_genshin
import consts


# record_genshin.record_percentage_breakdown(1000000, filename='percentage_breakdown_stop_1',timer=True,guaranteed_desired=1)

base_filename = 'percentage_breakdown_pity_'
file_extension = '.txt'
record_genshin.record_percentage_breakdown(100000, filename='percentage_breakdown_pity_53.txt',timer=True, pity=53)
for i in range(0,20):
    j = i*5
    if j >= 90:
        break
    filename = base_filename + str(j) + file_extension
    print(filename)
    record_genshin.record_percentage_breakdown(100000, filename=filename,timer=True, pity=j)