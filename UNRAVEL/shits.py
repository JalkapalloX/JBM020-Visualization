import pandas as pd
import numpy as np

data = pd.read_csv("C:/Users/sdannehl/Downloads/facebook-links.csv")

table = pd.crosstab(data["start"], data["target"], values=data["time"], aggfunc=np.sum)

data.head()
