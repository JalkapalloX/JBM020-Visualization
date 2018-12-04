import pandas as pd
import numpy as np
import os
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import time
plt.rcParams['figure.figsize'] = 15, 8
from PIL import Image as PImage
from scipy.misc import imread


os.getcwd()
os.chdir("/Users/blazejmanczak/Desktop/School/Year2/Q2/Visualization/Project_code/")
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

### BLAZEJ'S PART BEGIN
#dd = create_div_cols(pitch_devisions, wholeDataset).copy()

def create_pivot(data, start_time = -1, end_time = -1):
    if start_time == -1 and end_time == -1:
        start_time = min(data['secs'])
        end_time = max(data['secs'])
    start = min(data['secs'])*start_time
    end = max(data['secs'])*end_time
    data = data[(start<data['secs']) & (data['secs']<end)].copy()
    part_to_part_count = data.groupby(['part_of_origin', 'part_of_dest']).aggregate(['count'])['action_type']
    part_to_part_count = part_to_part_count.reset_index()
    pivot_table = part_to_part_count.pivot('part_of_origin', 'part_of_dest','count')
    return pivot_table

def create_heat(pivot_table):
    ax = sns.heatmap(pivot_table, annot = True, cmap = "RdYlGn")
    ax.set_xlabel("Destination of the ball")
    ax.set_ylabel("Origin of the ball")
    ax.set_title("Heatmap of passes", weight = "bold")
    #plt.show()
    return ax

pivot_table = create_pivot(data, 0, 100)
create_heat(pivot_table)

def generate_images(data, minutes, path):
    if (minutes > max(data['mins'])) or (minutes < min(data['mins'])):
        return "Invalid step. Please give step between {0} and {1}"
    if not os.path.exists(path):
        os.makedirs(path)
    num_steps = max(data['mins'])//minutes
    for i in range (1, num_steps+1):
        if i != num_steps:
            data_subset = data.loc[data['mins']<i*minutes].copy()
        else: data_subset = data.copy()
        table = create_pivot(data_subset)
        plt.clf()
        plot = create_heat(table)
        plot.get_figure().savefig(path + str(i)  + ".png")

dir = "/Users/blazejmanczak/Desktop/testPhotos/"
generate_images(data, 30, dir)

files = sorted([dir + f for f in os.listdir(dir) if f[-3:] == 'png'])

def loadImages(files):
    # return array of images
    loadedImages = []
    for image in files:
        img = PImage.open(image)
        loadedImages.append(img)
    return loadedImages

imgs = loadImages(files)
#import pylab as pl

plt.ion() # turn on interactive mode, non-blocking `show`
for i in range(0,len(files)):
    plt.figure() # create a new figure
    plt.axis('off')
    plt.imshow(imgs[i],interpolation="nearest")   # plot the figure
    plt.show()     # show the figure, non-blocking
    plt.close()
    time.sleep(2)



### BLAZEJ'S PART END
print("testing {0}".format(max(data['mins'])))

### KACPER'S PART BEGIN
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
