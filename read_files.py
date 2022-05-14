from posixpath import split
from os.path import exists
from matplotlib.cbook import print_cycles
import consts
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from helpers import Gauss, cos_func, objective

BREAKDOWN_FILENAME = 'percentage_breakdown_pity_0.csv'
SPACING = "     "

def lookup_or_run_stats(wish_num, wish_stats, filename=BREAKDOWN_FILENAME, trials=10000,pity=0):
    (lookup,deadone,deadtwo) = wish_breakdown_lookup(wish_num,filename=filename)
    if (lookup != []):
        # TODO lookup = [ lookup[i] for i in range(0,len(lookup))]
        print(format_wish_breakdown(lookup))
    else:
        temp_stats = wish_stats
        temp_stats.run_stats(trials)
        counts = list(temp_stats.tally_per_ru.values())
        counts = [ counts[i]/100 for i in range(0,len(counts))]
        counts = ["%.4f" % r for r in counts]
        output_string = ""
        output_string += "X: " + (str(counts[0]) + "%").ljust(10)
        for k in range(1,8):
            #make sure things are spaced evenly
            output_string += "C" + str(k-1) + ": " + (str(counts[k])+"%").ljust(10)
        print(output_string)
        pass

def format_wish_breakdown(breakdownlist):
    ratio_list = breakdownlist[1:len(breakdownlist)]
    output_string = ""
    output_string += "X: " + (str(ratio_list[0]) + "%").ljust(10)
    for k in range(1,8):
        #make sure things are spaced evenly
        output_string +="C" + str(k-1) + ": " + (ratio_list[k]+"%").ljust(10)
    return output_string

def wish_breakdown_lookup(wish_num, filename=BREAKDOWN_FILENAME):
    saved_line = ""
    if (not exists(filename)):
       print("Input File not found, filename: \"{0}\"".format(filename))
       return [], [], []
    else:
        i = 0
        j = 0
        columns = ["Wishes Available", "X","C0","C1","C2","C3","C4","C5","C6"]
        with open(filename, 'r') as f:
            for line in f:
                j+=1
                if(j == 2):
                    columns = line.split(',')
                if line[-5:-1] == "SKIP":
                    continue
                i+=1
                if(i == wish_num):
                    saved_line = line
                    break 
    splitting = saved_line.split(',')
    if (splitting == ['']):
        print("Stat for Wish number not recorded, num =  {0}".format(wish_num))
        return [], [], []

    #cleaning space
    for i in range(0,len(splitting)):
        splitting[i] = splitting[i].strip()
        if ('.' in splitting[i]):
            splitting[i] = float(splitting[i])
        else:
            splitting[i] = int(splitting[i])
    temp = splitting[0]
    splitting = ["%.4f" % r for r in splitting]
    splitting[0] = temp

    #cleaning space for columns
    for i in range(0,len(splitting)):
        columns[i] = columns[i].strip()
        if (i == len(columns)-1):
            columns[i] = columns[i][0:-4].strip()
    dictionary = { columns[i] : splitting[i] for i in range(0,len(splitting)) }
    return splitting, columns, dictionary

def read_full_breakdown_file(filename):
    if consts.PERCENTAGE_BREAKDOWN_FOLDER not in filename:
        percentage_breakdown_folder = consts.PERCENTAGE_BREAKDOWN_FOLDER
        filename = percentage_breakdown_folder+filename
    data_splitting = []
    data_labels = []
    with open(filename, 'r') as f:
        for line in f:
            if ("SKIP" in line):
                if (',' in line):
                    data_labels = line.split(',')
                    data_labels[-1] = data_labels[-1].replace("SKIP","")
                    data_labels[-1] = data_labels[-1].replace("\n","")
                    data_labels = [(data_labels[i]).strip() for i in range(0,len(data_labels))]
                    continue
            temp = line.split(',')
            temp[-1] = temp[-1].replace("\n","")
            temp = [temp[i].replace(" ","") for i in range(0,len(temp))]
            temp = [temp[i].strip() for i in range(0,len(temp))]

    print(data_labels)

def read_timer_file(timer_filename):
    if consts.TIMER_FOLDER not in timer_filename:
        percentage_breakdown_folder = consts.TIMER_FOLDER
        timer_filename = percentage_breakdown_folder+timer_filename
    values = []
    times = []
    data_labels = ["Values", "Time(s)"]
    with open(timer_filename, 'r') as f:
        for line in f:
            if ("SKIP" in line):
                continue
            temp = line.split(',')
            temp[-1] = temp[-1].replace("\n","")
            temp = [temp[i].replace(" ","") for i in range(0,len(temp))]
            temp = [temp[i].strip() for i in range(0,len(temp))]
            values.append(int(temp[0]))
            times.append(float(temp[1]))
    parameters, covariance = curve_fit(objective, values, times)
    fit_A = parameters[0]
    fit_B = parameters[1]
    fit_y = [objective(values[i], fit_A, fit_B) for i in range(0,len(values))]
    plt.plot(values, times, 'o', label='data')
    plt.plot(values, fit_y, '-', label='fit')
    plt.legend()
    plt.show()
    
    