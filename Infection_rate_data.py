"""@author Hannah Spurgeon"""

import numpy as np
import pandas as pd

#-----------------------------------------------------------------------------

# Function which calculates the infection rate for a given month based off of case numbers
# Inputs:
    # month = the month of cases to base infection rate off of in form where 320 corresponds to march 2020
    # data available until 521, May 2021 and from 320, march 2020 inclusive
# Outputs:
    # inf_rate = infection rate calculated based off of case numbers

def infection_rate(month):
    #data collection and preparation
    df = pd.read_csv('COVID_Bristol_infections.csv') #importing the daily case numbers for Bristol from a csv
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None) # converting the dates to datetime variables rather than integers
    # calculating the monthly average mean of cases per 100,000 and storing in the df
    infection_rates = df.groupby(pd.PeriodIndex(df['date'], freq="M"))['newCasesBySpecimenDate'].mean()
    infection_rates = infection_rates / 300  # estimating the infection rate based off of the number of cases in the bristol region
    infection_rates = infection_rates.to_numpy() # converting to a numpy array
    # if statements to extract the relevent infection rate
    months = [320,420,520,620,720,820,1020,1120,1220,121,221,321,421,521]
    for i in [i for i, x in enumerate(months) if x == month]:
        inf_rate_m = infection_rates[i]
    return inf_rate_m
