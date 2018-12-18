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


#os.getcwd()
#os.chdir("/Users/blazejmanczak/Desktop/School/Year2/Q2/Visualization/Project_code/")
wholeDataset = pd.read_csv('C:/Users/Hermii/Desktop/Vizualizations/all_passes.csv')

def convert_to_meters(data, width, length, start_xcol = "start_x", ##data parameter should be whole dataset
                                           start_ycol = "start_y",
                                           end_xcol = "end_x",
                                           end_ycol = "end_y"):

    """Converts the cooridnates of a field to meters, in our data: default column names are subject to change for another dataset"""
    data = data.copy()
    data[[start_xcol, end_xcol]] = data[[start_xcol, end_xcol]]/100 * width # transofrming x coordinates to width in m
    data[[start_ycol, end_ycol]] = data[[start_ycol, end_ycol]]/100 * length # transofrming x coordinates to width in m
    return data


def make_division(pitch_width, pitch_length, divideByX, divideByY):
    """Creates a list of divideByX*divideByY nested lists that set up the bounaries of the different parts of the pitch"""
    div = []
    step_width = pitch_width/divideByX
    step_height = pitch_length/divideByY
    for i in range (0,divideByY):
        for k in range(0,divideByX):
            div.append([k*step_width,(k+1)*step_width, i*step_height, (i+1)*step_height ]) #format [start_x, end_x, start_y, end_y]
    return div


def compare_to_part(x,y, pitch_devisions):
    for i in range (len(pitch_devisions)):
        if ((pitch_devisions[i][0] <= x <= pitch_devisions[i][1]) & (pitch_devisions[i][2] <= y <= pitch_devisions[i][3])):
            return i+1



def create_div_cols(pitch_devisions, data, start_xcol = "start_x",
                                           start_ycol = "start_y",
                                           end_xcol = "end_x",
                                           end_ycol = "end_y"):
    """ Adds columns saying what part of the pitch the pass originated from and to which part of the pitch the pass went"""
    data = data.copy()
    data['part_of_origin'] = data.apply(lambda row: compare_to_part(row[start_xcol], row[start_ycol], pitch_devisions), axis = 1)
    data['part_of_dest'] = data.apply(lambda row: compare_to_part(row[end_xcol], row[end_ycol], pitch_devisions), axis = 1)

    return data

#data_no_pitch_part = wholeDataset[wholeDataset['match_id'] == 30695]
#data = create_div_cols(pitch_devisions, data_no_pitch_part).copy()

### BLAZEJ'S PART  ASS 3 BEGIN
#dd = create_div_cols(pitch_devisions, wholeDataset).copy()


def create_pivot(data, to_aggr1 = 'part_of_origin' , to_aggr2 = 'part_of_dest'):
    part_to_part_count = data.groupby([to_aggr1, to_aggr2]).aggregate(['count'])['action_type']
    part_to_part_count = part_to_part_count.reset_index()
    pivot_table = part_to_part_count.pivot(to_aggr1, to_aggr2,'count')
    return pivot_table

def create_heat(pivot_table):
    ax = sns.heatmap(pivot_table, annot = True, cmap = "RdYlGn")
    ax.set_xlabel("Destination of the ball")
    ax.set_ylabel("Origin of the ball")
    ax.set_title("Heatmap of passes", weight = "bold")
    #plt.show()
    return ax

#pivot_table = create_pivot(data)
#create_heat(pivot_table)
#plt.show()

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

dir = "C:/Users/Hermii/Desktop/Vizualizations/testPhotosi"
#generate_images(data, 30, dir)

### BLAZEJ'S PART ASS 3END


### KACPER'S PART ASS 3 BEGIN
#dd = create_div_cols(pitch_devisions, wholeDataset).copy()

#run this for making heatmap with 30 sec intervals on x axis and parts of field on y axis and color variable counts of passes
#from the origin of these parts of field


def intervalheat(data): #data parameter is the divided by columns dataset
    bins = np.arange(data["minsec"].min(), data["minsec"].max(), 30)
    q = data.groupby(["part_of_origin",pd.cut(data["minsec"], bins=bins, labels=bins[1:])]).describe()
    plt.subplots(figsize=(40, 12))
    fig_heatmap = sns.heatmap(q.unstack()["part_of_dest"]["count"], annot=False, cmap = "RdYlGn")
    fig_heatmap.set_title("Heat map of count of passes(origin) by intervals plotted against field parts", size = 16, weight = "bold");
    fig_heatmap.set_xlabel("30sec Intervals", size = 14);                                                                           plt.show()
    fig_heatmap.set_ylabel("Part in field", size = 14);
    #plt.show()

#same but this time for destination
def intervalheat2(data):
    bins = np.arange(data["minsec"].min(), data["minsec"].max(), 30)
    q2 = data.groupby(["part_of_dest",pd.cut(data["minsec"], bins=bins, labels=bins[1:])]).describe()
    plt.subplots(figsize=(40, 12))
    fig_heatmap2 = sns.heatmap(q2.unstack()["part_of_origin"]["count"], annot=False, cmap = "RdYlGn")
    fig_heatmap2.set_title("Heat map of count of passes(dest) by intervals plotted against field parts", size = 16, weight = "bold");
    fig_heatmap2.set_xlabel("30sec Intervals", size = 14);
    fig_heatmap2.set_ylabel("Part in field", size = 14);
    #plt.show()

### KACPER'S PART ASS 3 END

### BLAZEJ'S PART ASS 4 BEGIN

def filter_time_dimension(data, start_interval, end_interval, column_seconds = "minsec"):
    """" Takes data as a data frame, start_interval and end_interval in percentages of total match time """
    return data.loc[(data[column_seconds]>=max(data[column_seconds]* start_interval/100)) & (data[column_seconds]<=max(data[column_seconds]* end_interval/100))]

def vertex_filter_dimension(data, vertices, col1 = 'part_of_origin', col2 = "part_of_dest"):
    """
    Input: data and the list of vertices to be included
    Output: subset of a data frame with only those passes that have both part_of_origin and part_of_dest within the given list of vertices
    """
    return data.loc[ (data[col1].isin(vertices)) & (data[col2].isin(vertices)) ]

def edge_filter_dimension(pivot_table, weight_thresh):
    """
    Returns a copy if input pivot table later used to create heatmaps with weights strictly smaller
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


def create_heat_modified(pivot_table, c, b, round_minut_param):
    ax = sns.heatmap(pivot_table, annot=True, cmap="Blues")
    ax.set_xlabel("Destination of the ball")
    ax.set_ylabel("Origin of the ball")
    ax.set_title("Heatmap of passes " + str(round(b / 60, round_minut_param)) + "min - " + str(
        round(c / 60, round_minut_param)) + "min", weight="bold")
    # plt.show()
    return ax


def generate_images(data_full, parts_to_divide, path, match_id, round_minut_param, column_seconds="minsec"):
    if not os.path.exists(path):
        os.makedirs(path)
    match_data = get_match(match_id, data_full)
    step = match_data[column_seconds].max() / parts_to_divide
    c = step
    b = 0
    for i in range(1, parts_to_divide + 1):
        subset_data = data_full[data_full[column_seconds].between(b, c)]
        table = create_pivot(subset_data)
        plot = create_heat_modified(table, c, b, round_minut_param)
        plot.get_figure().savefig(path + str(i) + ".png")
        plt.clf()
        c += step
        b += step

#preprocessing
wholeDataset = convert_to_meters(wholeDataset,68,105)
wholeDataset.drop(['a','injurytime_play', 'through_ball', 'throw_ins'], axis = 1, inplace = True)
pitch_devisions = make_division(68,105,3,4)
dd = create_div_cols(pitch_devisions, wholeDataset).copy() #dataset with divided field columns

pivot_table = create_pivot(dd) #preprocessing for heatmap
#create_heat(pivot_table) #simple heatmap
#plt.show()
generate_images(dd, 20, direc, 30695, 1) ##function to be used for the dynamic heatmaps + kivy

#example of create_heat with edge_filter_dimension returned table
create_heat(edge_filter_dimension(pivot_table, 4))
#plt.show()

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