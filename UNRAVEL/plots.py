import utilities
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import time
import networkx as nx
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.figure import Figure

def create_static_plot(plot_type, df, **kwargs):
    if plot_type == "Heatmap":
        static_heatmap("graphs/", df, **kwargs)
    elif plot_type == "Node-Link Diagram":
        static_node_link("graphs/", df, **kwargs)
    else:
        interleaved_network("graphs/", data=df, **kwargs)

def generate_matrix_reorderd(pivot_table):
    """
    Function to genereate clustergrid object. If followed by plt.show(),
    it will display a hierarchically clustered heatmap with a dendogram
    """
    pivot_table = pivot_table.fillna(0)
    ax = sns.clustermap(pivot_table, cmap="Blues", fmt='g')
    return ax

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

# FUNCTION FOR STATIC HEATMAP CREATION
def static_heatmap(path, df, X, Y, values="", aggfunc="Sum", ordering="Default", **kwargs):
    """
    ~~~ ARGS ~~~
    path         str           folder to store images in
    df           pd.DataFrame  data frame
    X            str           Name of column for X-axis
    Y            str           Name of column for Y-axis
    values       str           Name of column to summarize
    aggfunc      function      Function to summarize values column
    **kwargs     -             Additional arguments to be passed into sns.heatmap()
    """

    sns.set(rc={'figure.figsize':(14.79,9.74)})
    sns.set_style("ticks")
    sns.set_context("paper")

    summary_funcs = {"Sum": np.sum, "Mean": np.mean}
    aggfunc = summary_funcs[aggfunc]

    # IF NO VALUE COLUMN IS SET JUST USE FREQUENCIES
    if values=="":
        df["#@frequency_column"] = 1
        values = "#@frequency_column"

    # CALCULATES TABLE AND PLOTS IT AS HEATMAP
    table = pd.crosstab(df[Y], df[X], values=df[values], aggfunc=aggfunc)

    if ordering == "Dendrogram":
        row_order, column_order = get_hierachical_order(table)
        table = reorder_pivot_table(row_order, column_order, table)

    plt.clf() # Clear window
    sns.despine()
    plot = sns.heatmap(table, **kwargs)


    # SET BASIC INFORMATION
    plot.set_xlabel(X)
    plot.set_ylabel(Y)
    plot.set_title("")

    # SAVES FIGURE IN DIR
    plot.get_figure().savefig(path + str(int(time.time())) + ".png")


# Variable node sizes
# Variable colors for nodes
# Variable colors for edges
# Highlight

def static_node_link(path, df, start_node, end_node, layout,
                     directed=True, edge_weight="None", node_size="", color="",
                     color_nodes=True, color_edges=False, cmap="jet", highlight=[]):
    """
    ~~~ ARGS ~~~
    path         str           folder to store images in
    df           pd.DataFrame  data frame
    start_node   str           Name of column for start node (U)
    end_node     str           Name of column for end node (V)
    layout       str           Kind of node link diagram (Circular or Fruchterman-Reingold)
    directed     function      Determines whether lines have arrows or not
    edge_weight  str           Optional: Column for associated weights
    node_size    str           Optional: Column for node sizes (Will be summed over start nodes (Dir) or nodes involved (NDir))
    **kwargs     -             Additional arguments to be passed into nx.draw()
    """

    plt.figure(figsize=(9.74,9.74))
    plt.axis("off")

    # GROUPS BY START AND END NODE THEN SUMS WEIGHTS
    df = df.groupby([start_node, end_node], as_index=False).sum()

    # CREATE EMPTY CANVAS
    canvas_dict = {True: nx.DiGraph, False: nx.Graph}
    G = canvas_dict[directed]()

    # ADD NODES TO PLOT
    all_nodes = sorted(list(set(df[start_node].append(df[end_node]))))
    for node in all_nodes:
        G.add_node(node)

    # ADD EDGES TO PLOT
    if edge_weight == "":
        df.apply(lambda row: G.add_edge(row[start_node], row[end_node], weight=1), axis=1)
    else:
        df.apply(lambda row: G.add_edge(row[start_node], row[end_node], weight=row[edge_weight]), axis=1)

    # GET NORMALIZED NODE COLORS
    cmap_dict = {"jet": plt.cm.jet, "terrain": plt.cm.terrain, "plasma": plt.cm.plasma, "viridis": plt.cm.viridis}
    if (color != "") & (color_nodes == True):
        node_colors = df.groupby(start_node)[[color]].sum()\
                       .reindex(index=all_nodes)\
                       .iloc[:,0].values
        node_colors[np.isnan(node_colors)] = np.nanmin(node_colors)
        node_colors = list(0.9 - node_colors / max(node_colors) + 0.1)
    else:
        node_colors = [0.1] * len(all_nodes)


     # GET NORMALIZED NODE SIZES
    if node_size == "":
        degrees = nx.degree(G)
        node_sizes = np.array([d[1] for d in G.degree])
    else:
        node_sizes = df.groupby(start_node)[[node_size]].sum()\
                       .reindex(index=all_nodes)\
                       .iloc[:,0].values
        node_sizes[np.isnan(node_sizes)] = np.nanmin(node_sizes)

    node_sizes = list(195 * node_sizes / max(node_sizes) + 5)

    # GET EDGE WIDTHS
    weights = np.array([G[u][v]['weight'] for u,v in G.edges()])
    if edge_weight != "":
        weights = list(3 * weights / max(weights) + 1)
    else:
        weights = list(weights)

    # GET EDGE COLORS
    if color_edges == True:
        colors = list(1-weights / max(weights))
    else:
        colors = "dimgray"
    if edge_weight == "":
        colors = "dimgray"

    if len(highlight) > 0:
        for i in highlight:
            node_sizes[all_nodes.index(i)] = 300
            node_colors[all_nodes.index(i)] = 1
    # node_order = sorted(range(len(node_sizes)), key=node_sizes.__getitem__)

    # k=4*...
    # GET POSITIONS OF NODES
    pos_layout_dict = {"Fruchterman-Reingold": (nx.spring_layout(G, k=10*1/np.sqrt(len(G.nodes())), weight=1, iterations=350)),
                       "Circular": (nx.circular_layout(G))}
    pos = pos_layout_dict[layout]

    # DRAW NETWORK
    nx.draw_networkx_edges(G, pos=pos, #alpha=0.9,
                           edgelist=G.edges(),
                           width=weights,
                           edge_color=colors,
                           edge_cmap=cmap_dict[cmap],
                           vmax=1, vmin=0)
    nx.draw_networkx_nodes(G, pos=pos,
                           node_list=all_nodes, node_size=node_sizes,
                           node_color=node_colors,
                           cmap=cmap_dict[cmap], vmax=1, vmin=0, with_labels=False)

    plt.savefig(path + str(int(time.time())) + ".png")

def interleaved_network(path, data, start_node, end_node , edge_weight, time, colormap):
    """
    ~~~ ARGS ~~~
    path         str           folder to store images in
    data         pd.DataFrame  Data Frame object
    start_node   str           Name of column for start node (U)
    end_node     str           Name of column for end node (V)
    edge_weight  str           Column for associated weights
    time         str           Column for associated time stamps
    color_map    str           Color map to be used. Defaults to "Oranges_r"
    **kwargs     -             Additional arguments to be passed into ...
    Received some help from Jaap while builidng this func.
    """
    df = data.copy()

    # Get the infromation needed about the data
    df['freq'] = df.groupby([time, start_node, end_node])[edge_weight].transform('count')
    unique_stamps = df[time].unique()
    agg = {}

    # Intialising the plotting variables
    ax = plt.figure(figsize=(14.79,9.74), dpi=100)
    fig = ax.add_subplot(111)

    fig.axis('off') # gets rid of the border
    fig.get_xaxis().set_visible(False) # turns of the x axis
    #fig.get_yaxis().set_visible(False) # turns of the x axis

    offset = 3
    acc = 0

    # Creates dict for the  location of lines
    while acc < len(unique_stamps):
        try:
            agg[unique_stamps[acc]] = unique_stamps[acc + offset]
        except:
            agg[unique_stamps[acc]] = 'agg+' + str(acc + offset - len(unique_stamps))
        acc += 1

    norm = Normalize(vmin=df[edge_weight].min(), vmax=df[edge_weight].max())
    cmap = cm.get_cmap(name=colormap)
    mapping= cm.ScalarMappable(norm=norm, cmap=cmap)

    # Put the rows on the plot
    for index, instance in df.iterrows():
        a = [instance[time], agg[instance[time]]]
        b = [instance[start_node], instance[end_node]]
        fig.plot(a, b, alpha=0.25, c = mapping.to_rgba(instance[edge_weight]))

    plt.savefig(path + "hey.png")
