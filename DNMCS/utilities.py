import os
import pandas as pd

from tkinter import Tk
from tkinter.filedialog import askopenfilename

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

class data_iterator():
    def __init__(self, df, shift_over, n, interval=None):
        self.__state__ = 0
        self.df = df
        self.shift_over = shift_over
        self.n = n
        self.interval = interval

        if interval is not None:
            self.min_of_shift = min(df[shift_over])
            self.step_of_shift = (max(df[shift_over]) - min(df[shift_over]) - interval) / (n-1)
        else:
            self.step_of_shift = (max(df[shift_over]) - min(df[shift_over])) / n

    def __iter__(self):
        return self

    def __next__(self):
        self.__state__ += 1
        if self.interval:
            # STOP AT LAST ITERATION
            if self.__state__ > self.n:
                raise StopIteration

            df_subset = self.df.loc[(self.df[self.shift_over] >= self.min_of_shift + self.step_of_shift*self.__state__) &
                                    (self.df[self.shift_over] < self.min_of_shift + self.step_of_shift*self.__state__+self.interval)]
            return df_subset
        else:
            # STOP AT LAST ITERATION
            if self.__state__ > self.n:
                raise StopIteration

            df_subset = self.df.loc[(self.df[self.shift_over] >= self.step_of_shift*(self.__state__-1)) &
                                    (self.df[self.shift_over] < self.step_of_shift*self.__state__)]
