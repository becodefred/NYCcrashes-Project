import pandas as pd
import numpy as np

def reduce_unique_val(df, col_names, sub_str, unique_str):
    """ 
    Example: if sub_str = "tow" and unique_str = "Tow", then expressions such as
    Tow Truck, TOW, tow t, etc., in typevehi (i = 1, 2,..., 5), will be replaced by Tow. 
    """   
    xval = df[col_names].values.ravel()
    x = pd.unique(xval)
    y = list(pd.Series(x).str.lower())
    z = np.core.defchararray.find(y, sub_str, start = 0, end = None)
    filt = x[z >= 0]
    
    s = ""
    for i in range(len(sub_str)):
        s += str("[" + sub_str[i] + sub_str[i].upper() + "]")

    pattern = ".*" + s + ".*"
    
    test = pd.Series(filt).str.replace(pattern, unique_str, regex = True)
    if len(pd.unique(test)) == 1:
        print("Successfully reduced the number of unique values")   
                
    df[col_names] = df[col_names].replace(pattern, unique_str, regex = True)
    return df
    

