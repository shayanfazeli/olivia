import pandas
import numpy
from datetime import datetime


def get_as_datetime(x):
    es = [int(e) for e in x.split('-')]
    return datetime(year=es[0], month=es[1], day=es[2])


def floatify_df(df):
    for col in df.columns.tolist():
        if col in ['county', 'state', 'day_of_the_year', 'location', 'confirmed_date']:
            continue
        else:
            df[col] = df[col].astype(numpy.float32)
    return df


def floatify_dict(df):
    for col in df.keys():
        if col == 'confirmed_date':
            continue
        elif col in ['county', 'state', 'day_of_the_year', 'location']:
            df[col] = str(df[col])
        else:
            df[col] = float(df[col])
    return df
