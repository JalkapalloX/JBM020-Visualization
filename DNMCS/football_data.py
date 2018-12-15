import pandas as pd
import numpy as np
import math

DATA_DIR = "C:/Users/sdannehl/Documents/Docs/University/Y2/Q2/Visualization/all_passes.csv"
relevant_columns = ["start_x", "start_y", "end_x", "end_y", "minsec", "player_id", "team_id", "match_id", "type", "assist"]

# def split_equally(column, n, min=None, max=None, alias=False):
#     if min is None: min = min(column)
#     if max is None: max = max(column)
#     stepsize = (max - min) / n
#
#     if alias is True:
#         return pd.factorize(pd.cut(column), sort = True)
#
#     pd.cut(column, )

# SELECT RELEVANT COLUMNS & DO SIMPLE TRANSFORMATIONS
data = pd.read_csv(DATA_DIR)
data["assist"] = data["a"].equals(1)        # Create assist column
data = data[relevant_columns]
data["type"] = (data["type"] == "completed") | (data["type"] == "assist") # Create completion column

# DO GROUPING
data["region_start_x"] = pd.factorize(pd.cut(data["start_x"], [0, 33, 66, 100]), sort=True)[0] + 1
data["region_start_y"] = pd.factorize(pd.cut(data["start_y"], [0, 33, 66, 100]), sort=True)[0] + 1
data["region_end_x"] = pd.factorize(pd.cut(data["end_x"], [0, 33, 66, 100]), sort=True)[0] + 1
data["region_end_y"] = pd.factorize(pd.cut(data["end_y"], [0, 33, 66, 100]), sort=True)[0] + 1

data.head()
