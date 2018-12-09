import os
import pandas as pd

def read_data(path):
    ext = os.path.splitext(path)[-1].lower()
    if ext == ".txt":
        data = pd.read_table(path, delim_whitespace=True)
    elif ext == ".csv":
        data = pd.read_csv(path)

    return data

def wipe(path):
    folder = os.listdir(path)

    for item in folder:
        if item.endswith(".png"):
            os.remove(os.path.join(path, item))

class data_iterator():
    def __init__(self, df, shift_over, n, interval):
        self.__state__ = 0
        self.df = df
        self.shift_over = shift_over
        self.n = n
        self.interval = interval
        self.min_of_shift = min(df[shift_over])
        self.step_of_shift = (max(df[shift_over]) - min(df[shift_over]) - interval) / (n-1)

    def __iter__(self):
        return self

    def __next__(self):
        self.__state__ += 1

        if self.__state__ > self.n:
            raise StopIteration

        df_subset = self.df.loc[(self.df[self.shift_over] >= self.min_of_shift + self.step_of_shift*self.__state__) &
                                (self.df[self.shift_over] <= self.min_of_shift + self.step_of_shift*self.__state__+self.interval)]
        return df_subset
