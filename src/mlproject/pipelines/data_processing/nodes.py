import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def preprocessing_date(df : pd.DataFrame):
    df["Time"] = df["published_at"].str.split(" ", expand=True)[1]
    df["Date"] = df["published_at"].str.split(" ", expand=True)[0]
    # We are interested in the year so we are going to split the date columns into 3 columns, day - month and year
    df["Day"] = df["Date"].str.split("-", expand=True)[2]
    df["Month"] = df["Date"].str.split("-", expand=True)[1]
    df["Year"] = df["Date"].str.split("-", expand=True)[0]
    # indeed, the type was wrong so we'll switch it from object to integer
    df['Year'] = df['Year'].astype('int')
    df['Month'] = df['Month'].astype('int')
    df['Day'] = df['Day'].astype('int')
    # We delete all the rows that contain videos published during the year 2020
    df = df[df['Year'] != 2020]
    return df


def preprocessing_final(df : pd.DataFrame):
    df_new = df.drop(['video_id', 'published_at', 'channel_id', 'channel_title',
         'Date', 'Day', 'Month', 'Year', 'Time'], axis=1)
    # we filtered enough data to get the same amount of rows '23 000' at the end of each filtering.
    # We can now apply these changes to our main dataframe
    df_new = df_new[df_new['likes'] >= 5000]
    df_new = df_new[df_new['view_count'] >= 250000]
    df_new = df_new[df_new['dislikes'] >= 150]
    # as long as our dataset is big, we can delete the rows that contain null values because they won't affect our work
    df_new.dropna(axis=0, how='any', subset=None, inplace=False)
    # We have finished the cleaning/preprocessing phase, our dataset is now ready to be expoilted and used
    return df_new

