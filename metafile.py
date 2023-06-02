import numpy as np
import pandas as pd
import json

def meta(file):
  df = pd.DataFrame(file["data"],index = None, columns = file["index"])
  print(df.apply(lambda x: x.duplicated().sum()))