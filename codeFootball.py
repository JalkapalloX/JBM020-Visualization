import pandas as pd
import numpy as np
import os
import time

%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns  # also improves the look of plots
sns.set()  # set Seaborn defaults
plt.rcParams['figure.figsize'] = 10, 5  # default hor./vert. size of plots, in inches
plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn

os.getcwd()

wholeDataset = pd.read_csv('/Users/blazejmanczak/Desktop/School/Year2/Q2/Visualization/Project_code/all_passes.csv')
wholeDataset[['start_x','end_x']] = wholeDataset[['start_x','end_x']]/100 * 68 # transofrming x coordinates to width in m
wholeDataset[['start_y','end_y']] = wholeDataset[['start_y','end_y']]/100 * 105 # transofrming x coordinates to width in m
wholeDataset.drop(['a','injurytime_play', 'through_ball', 'throw_ins'], axis = 1, inplace = True)

def make_division(pitch_width, pitch_length, divideByX, divideByY):
    """Creates a list of divideByX*divideByY nested lists that set up the bounaries of the different parts of the pitch"""
    div = []
    step_width = pitch_width/3
    step_height = pitch_length/4
    for i in range (0,divideByY):
        for k in range(0,divideByX):
            div.append([k*step_width,(k+1)*step_width, i*step_height, (i+1)*step_height ]) #format [start_x, end_x, start_y, end_y]
    return div


def compare_to_part(x,y, pitch_devisions):
    #print("going_in",x,y)
    for i in range (len(pitch_devisions)):
        if ((pitch_devisions[i][0] <= x <= pitch_devisions[i][1]) & (pitch_devisions[i][2] <= y <= pitch_devisions[i][3])):
            return i+1

### example
data = wholeDataset[wholeDataset['match_id'] == 30695]
pitch_devisions = make_division(68,105,3,4)
pitch_devisions
start_x = data['start_x'][0]
start_y = data['start_y'][0]
start_x
start_y
compare_to_part(start_x,start_y, pitch_devisions)

def create_div_cols(pitch_devisions, data):
    """ Adds columns saying what part of the pitch the pass originated from and to which part of the pitch the pass went"""
    data1 = data.copy()

    data1['part_of_origin'] = data1.apply(lambda row: compare_to_part(row['start_x'], row['start_y'], pitch_devisions), axis = 1)
    data1['part_of_dest'] = data1.apply(lambda row: compare_to_part(row['end_x'], row['end_y'], pitch_devisions), axis = 1)

    return data1



data_no_pitch_part = wholeDataset[wholeDataset['match_id'] == 30695]
data = create_div_cols(pitch_devisions, data_no_pitch_part).copy()


def create_pivot(data, start_time, end_time):
    start = min(data['secs'])*start_time
    end = max(data['secs'])*end_time
    data = data[(start<data['secs']) & (data['secs']<end)].copy()
    part_to_part_count = data.groupby(['part_of_origin', 'part_of_dest']).aggregate(['count'])['action_type']
    part_to_part_count = part_to_part_count.reset_index()
    pivot_table = part_to_part_count.pivot('part_of_origin', 'part_of_dest','count')
    return pivot_table

def create_heat(pivot_table):
    ax = sns.heatmap(pivot_table, annot = True)
    ax.set_xlabel("Destination of the ball")
    ax.set_ylabel("Origin of the ball")
    ax.set_title("Heatmap of passes", weight = "bold")

pivot_table = create_pivot(data, 0, 100)
create_heat(pivot_table)





for i in range(1,10):
    time.sleep(5)
    sns.heatmap(pivot_table, annot = True)
    plt.show()
    fig.canvas.draw()
    plt.clf()



    #create_heat(create_pivot(data,10*(i-1), 10*i) )
    #plt.clf()
    #plt.show(block = False)
