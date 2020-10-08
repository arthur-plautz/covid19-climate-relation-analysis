import numpy as np
import pandas as pd

def remove_values(df, column, target=[]):
    target = [str(t).lower() for t in target] + ['nan', 'undefined', 'null', 'none', '']
    values = df[column].unique()
    mapping = {}
    for value in values:
        if str(value).lower() not in target:
            mapping[value] = value
        else:
            mapping[value] = np.nan
    df[column] = df[column].map(mapping)
    return df[df[column].notna()]