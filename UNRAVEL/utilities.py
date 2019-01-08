import os
import pandas as pd

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from collections import defaultdict
from heapq import *

def get_file():
    Tk().withdraw()
    return askopenfilename()

def read_data(path):
    ext = os.path.splitext(path)[-1].lower()
    if ext == ".txt":
        new_data = pd.read_table(path, delim_whitespace=True)
    elif ext == ".csv":
        new_data = pd.read_csv(path)

    return new_data

def wipe(path):
    folder = os.listdir(path)

    for item in folder:
        if item.endswith(".png"):
            os.remove(os.path.join(path, item))

def data_filter(df, cols, minmax):
    for i in range(len(cols)):
        df = df.loc[(df[df.columns[i]] >= minmax[2*i]) & (df[df.columns[i]] <= minmax[2*i+1]),]

def newline_insert(text, split_char, n):
    lst = text.split(split_char)
    new_string = lst.pop(0)

    # DECIDE FOR EACH ELEMENT WHETHER IT STILL FITS INTO LINE
    this_lines_chars = len(new_string) # Number of chars in line
    while(len(lst) > 0):
        if this_lines_chars + len(lst[0]) + 1 < n:
            # ADD TO OLD LINE
            last_element = lst.pop(0)
            new_string += split_char + last_element
            this_lines_chars += len(last_element)
        else:
            # ADD TO NEW LINE
            last_element = lst.pop(0)
            new_string += split_char + "\n" + last_element
            this_lines_chars = len(last_element)

    return new_string

# From https://gist.github.com/kachayev/5990802
def dijkstra(df, cstart, cend, cdist, start_node, end_node):
    edges = list(df.apply(lambda x: (x[cstart], x[cend], x[cdist]), axis=1))
    lst_path = []

    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,start_node,())], set(), {start_node: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == end_node:
                while len(path) > 0:
                    lst_path.append(path[0])
                    path = path[1]

                return (cost, lst_path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf")
