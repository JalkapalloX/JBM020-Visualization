import utilities
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import time

def create_plot():
    dynamic_heatmap("graphs/", data, "start", "target", "time", 30, 100)
    return

def dynamic_heatmap(path, df, X, Y, shift_over, n, interval, values=None, aggfunc=np.sum, **kwargs):
    """
    ~~~ ARGS ~~~
    path:        str           folder to store images in
    df:          pd.DataFrame  data frame
    X:           str           Name of column for X-axis
    Y:           str           Name of column for Y-axis
    shift_over   str           Name of column to apply shift over
    n            int           Number of shifts
    interval     float         Interval of shift column at each iteration
    values       str           Name of column to summarize
    aggfunc      function      Function to summarize values column
    **kwargs     -             Additional arguments to be passed into sns.heatmap()
    """
    # CREATE DIR FOR GRAPHS
    if not os.path.exists(path):
        os.makedirs(path)

    # IF NO VALUE COLUMN IS SET JUST USE FREQUENCIES
    if values is None:
        df["#@frequency_column"] = 1
        values = "#@frequency_column"

    iterator = utilities.data_iterator(df, shift_over, n, interval)

    idx = 0
    for i in iterator:
        idx += 1

        # CALCULATES TABLE AND PLOTS IT AS HEATMAP
        table = pd.crosstab(i[X], i[Y], values=i[values], aggfunc=aggfunc)
        plt.clf() # Clear window
        plot = sns.heatmap(table, **kwargs)

        # SAVES FIGURE IN DIR
        plot.get_figure().savefig(path + "plot_" + str(idx) + ".png")
