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
    if month == 320:
        inf_rate = infection_rates[0]
    elif month == 420:
        inf_rate = infection_rates[1]
    elif month == 520:
        inf_rate = infection_rates[2]
    elif month == 620:
        inf_rate = infection_rates[3]
    elif month == 720:
        inf_rate = infection_rates[4]
    elif month == 820:
        inf_rate = infection_rates[5]
    elif month == 920:
        inf_rate = infection_rates[6]
    elif month == 1020:
        inf_rate = infection_rates[7]
    elif month == 1120:
        inf_rate = infection_rates[8]
    elif month == 1220:
        inf_rate = infection_rates[9]
    elif month == 121:
        inf_rate = infection_rates[10]
    elif month == 221:
        inf_rate = infection_rates[11]
    elif month == 321:
        inf_rate = infection_rates[12]
    elif month == 421:
        inf_rate = infection_rates[13]
    elif month == 521:
        inf_rate = infection_rates[14]
    return inf_rate

