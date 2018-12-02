import pandas as pd
import numpy as np
import os
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
os.getcwd()

wholeDataset = pd.read_csv('C:/Users/Hermii/Desktop/Vizualizations/all_passes.csv')
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
            return i

### example
pitch_devisions = make_division(68,105,3,4)
pitch_devisions
start_x = wholeDataset['start_x'][0]
start_y = wholeDataset['start_y'][0]
start_x
start_y
compare_to_part(start_x,start_y, pitch_devisions)

def create_div_cols(pitch_devisions, data):
    """ Adds columns saying what part of the pitch the pass originated from and to which part of the pitch the pass went"""

    data['part_of_origin'] = data.apply(lambda row: compare_to_part(row['start_x'], row['start_y'], pitch_devisions), axis = 1)
    data['part_of_dest'] = data.apply(lambda row: compare_to_part(row['end_x'], row['end_y'], pitch_devisions), axis = 1)

    return data.copy()

data_no_pitch_part = wholeDataset[wholeDataset['match_id'] == 30695]
data = create_div_cols(pitch_devisions, data_no_pitch_part).copy()
data.isnull().sum()

dd = create_div_cols(pitch_devisions, wholeDataset).copy()

#run this for making heatmap with 30 sec intervals on x axis and parts of field on y axis and color variable counts of passes
#from the origin of these parts of field
bins = np.arange(data_no_pitch_part["minsec"].min(), data_no_pitch_part["minsec"].max(), 30)
q = dd.groupby(["part_of_origin",pd.cut(dd["minsec"], bins=bins, labels=bins[1:])]).describe()
plt.subplots(figsize=(40, 12))
fig_heatmap = sns.heatmap(q.unstack()["part_of_dest"]["count"], annot=False, cmap = "RdYlGn")
fig_heatmap.set_title("Heat map of count of passes(origin) by intervals plotted against field parts", size = 16, weight = "bold");
fig_heatmap.set_xlabel("30sec Intervals", size = 14);                                                                           plt.show()
fig_heatmap.set_ylabel("Part in field", size = 14);
#plt.show()

#same but this time for destination
q2 = dd.groupby(["part_of_dest",pd.cut(dd["minsec"], bins=bins, labels=bins[1:])]).describe()
plt.subplots(figsize=(40, 12))
fig_heatmap2 = sns.heatmap(q2.unstack()["part_of_origin"]["count"], annot=False, cmap = "RdYlGn")
fig_heatmap2.set_title("Heat map of count of passes(dest) by intervals plotted against field parts", size = 16, weight = "bold");
fig_heatmap2.set_xlabel("30sec Intervals", size = 14);
fig_heatmap2.set_ylabel("Part in field", size = 14);
plt.show()