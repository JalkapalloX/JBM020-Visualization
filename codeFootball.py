import pandas as pd
import numpy as np
import os
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import time
plt.rcParams['figure.figsize'] = 12, 10
from PIL import Image as PImage
from scipy.misc import imread


os.getcwd()
os.chdir("/Users/blazejmanczak/Desktop/School/Year2/Q2/Visualization/Project_code/")
wholeDataset = pd.read_csv('/Users/blazejmanczak/Desktop/School/Year2/Q2/Visualization/Project_code/all_passes.csv')

def convert_to_meters(data, width, length):
    """Converts the cooridnates to meters"""
    data = data.copy()
    data[['start_x','end_x']] = data[['start_x','end_x']]/100 * width # transofrming x coordinates to width in m
    data[['start_y','end_y']] = data[['start_y','end_y']]/100 * length # transofrming x coordinates to width in m
    return data


wholeDataset = convert_to_meters(wholeDataset,68,105)
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
    data = data.copy()
    data['part_of_origin'] = data.apply(lambda row: compare_to_part(row['start_x'], row['start_y'], pitch_devisions), axis = 1)
    data['part_of_dest'] = data.apply(lambda row: compare_to_part(row['end_x'], row['end_y'], pitch_devisions), axis = 1)

    return data

data_no_pitch_part = wholeDataset[wholeDataset['match_id'] == 30695]
data = create_div_cols(pitch_devisions, data_no_pitch_part).copy()

### BLAZEJ'S PART  ASS 3 BEGIN
#dd = create_div_cols(pitch_devisions, wholeDataset).copy()


def create_pivot(data):
    part_to_part_count = data.groupby(['part_of_origin', 'part_of_dest']).aggregate(['count'])['action_type']
    part_to_part_count = part_to_part_count.reset_index()
    pivot_table = part_to_part_count.pivot('part_of_origin', 'part_of_dest','count')
    return pivot_table

def create_heat(pivot_table):
    ax = sns.heatmap(pivot_table, annot = True, cmap = "Blues", fmt='g')
    ax.set_xlabel("Destination of the ball")
    ax.set_ylabel("Origin of the ball")
    ax.set_title("Heatmap of passes", weight = "bold")
    #plt.show()
    return ax

pivot_table = create_pivot(data)
create_heat(pivot_table)
plt.show()

def generate_images(data, minutes, path):  # I guess we will not be using it but just in case
    """
    A function that generates heatmaps given
    """
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
#generate_images(data, 30, dir)

### BLAZEJ'S PART ASS 3END


### KACPER'S PART ASS 3 BEGIN

#dd = create_div_cols(pitch_devisions, wholeDataset).copy()

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

### KACPER'S PART ASS 3 END

### BLAZEJ'S PART ASS 4 BEGIN

def filter_time_dimension_min(data, start_interval, end_interval):
    """"
    Takes data as a data frame, start_interval and end_interval in minutes.
    Return a data frame with data only withinh specified time interval
    """
    return data[data['mins'].between(start_interval,end_interval)]

def filter_time_dimension_sec(data, start_interval, end_interval):
    """"
    Takes data as a data frame, start_interval and end_interval in seconds.
    Return a data frame with data only withinh specified time interval
    """
    return data[data['minsec'].between(start_interval,end_interval)]


def vertex_filter_dimennsion(data, vertices):
    """
    Input: data and the list of vertices to included
    Output: subset of a data frame with only those passes that have both part_of_origin and part_of_dest within the given list of vertices
    """
    return data.loc[ (data['part_of_origin'].isin(vertices)) & (data['part_of_dest'].isin(vertices)) ]

def edge_filter_dimension(pivot_table, weight_thresh):
    """
    Returns a copy of the input pivot table later used to create heatmaps with weights strictly smaller
    than given weight_thresh subsitued to NaN values
    """
    pivot_no_weights = pivot_table.copy()
    x_shape = pivot_table.shape[0]
    y_shape = pivot_table.shape[0]
    for a in range (1, x_shape +1):
        for b in range (1, y_shape+1):
            if (pivot_no_weights[a][b] < weight_thresh):
                pivot_no_weights[a][b] = np.nan
    return pivot_no_weights


### BLAZEJ'S PART ASS 4 END

# match to experiment on 30695


def get_match(match_id, data):
    return data[data["match_id"] == match_id]


direc = "C:/Users/Hermii/Desktop/Vizualizations/heats/"
direc = "/Users/blazejmanczak/Desktop/testPhotos"

def create_heat_modified(pivot_table, c, b, round_minut_param):
    ax = sns.heatmap(pivot_table, annot=True, cmap="Blues")
    ax.set_xlabel("Destination of the ball")
    ax.set_ylabel("Origin of the ball")
    ax.set_title("Heatmap of passes " + str(round(b / 60, round_minut_param)) + "min - " + str(
        round(c / 60, round_minut_param)) + "min", weight="bold")
    # plt.show()
    return ax



def generate_images(data_full, parts_to_divide, path, match_id, round_minut_param):
    if not os.path.exists(path):
        os.makedirs(path)
    match_data = get_match(match_id, data)
    step = match_data["minsec"].max() / parts_to_divide
    c = step
    b = 0
    for i in range(1, parts_to_divide + 1):
        subset_data = filter_time_dimension_sec(data, b, c)
        table = create_pivot(subset_data)
        plot = create_heat_modified(table, c, b, round_minut_param)
        plot.get_figure().savefig(path + str(i) + ".png")
        plt.clf()
        c += step
        b += step


generate_images(wholeDataset, 20, direc, 30695, 1)


### Blazej's Ass 5 BEGIN

data_no_pitch_part = wholeDataset[wholeDataset['team_id'] == 521] ## getting all the matches of team 521
data = create_div_cols(pitch_devisions, data_no_pitch_part).copy()

def generate_matrix_reorderd(pivot_table):
    """
    Function to genereate clustergrid object. If followed by plt.show(),
    it will display a hierarchically clustered heatmap with a dendogram
    """
    pivot_table = pivot_table.fillna(0)
    ax = sns.clustermap(pivot_table, cmap="Blues", fmt='g')
    #plt.clf()
    #ax.ax_heatmap.set_title('Hierachically clustered heatmap of passes', weight = "bold")
    return ax

#Example generate_matrix_reorderd(pivot_table) which generates heatmap with dendogram
ax2 = generate_matrix_reorderd(pivot_table)
plt.show()

def get_hierachical_order(pivot_table):
    """Uses the clustergrid object generated by generate_matrix_reorderd to get the order of columns and rows"""
    ax = generate_matrix_reorderd(pivot_table)
    rows_reorderd = [x+1 for x in ax.dendrogram_row.reordered_ind] # such construct because indexing starts at 0 and our naming from 1
    coulmns_reordered = ax.dendrogram_col.reordered_ind
    return rows_reorderd, coulmns_reordered

def reorder_pivot_table(row_order, column_order, pivot_table):
    pivot_table_reorderd = pivot_table.copy()
    pivot_table_reorderd = pivot_table.reindex(row_order) # reordering rows
    pivot_table_reorderd = pivot_table_reorderd[[pivot_table.columns[i] for i in column_order]] #reordering columns
    return pivot_table_reorderd

#Example of obtaining ordered adjacency matrix visualization without a dendogram
row_order, column_order = get_hierachical_order(pivot_table)
plt.clf() ## must be there not to fuck up the graph
pivot_table_reorderd = reorder_pivot_table(row_order,column_order, pivot_table)
ax1 = create_heat(pivot_table_reorderd)
plt.show()

#In comparasion to original unordered version
ax3 = create_heat(pivot_table)
plt.show()


#Saving for assignment
os.chdir('/Users/blazejmanczak/Desktop/School/Year2/Q2/Visualization')
ax1.get_figure().savefig("orderdHeat.png")
ax2.savefig("orderedWithDendogram.png")
ax3.get_figure().savefig("nonOrderedHeat.png")
