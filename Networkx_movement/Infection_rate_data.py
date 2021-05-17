import numpy as np
import pandas as pd
#importing the daily case numbers for Bristol
df = pd.read_csv('COVID_Bristol_infections.csv')
#converting the dates to datetime variables rather than integers
df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
df['month'] = df.date.dt.month
#calculating the monthly average mean of cases per 100,000 and storing in the df
infection_rates = df.groupby(pd.PeriodIndex(df['date'], freq="M"))['newCasesBySpecimenDate'].mean()
infection_rates = infection_rates / 300
#converting to a numpy array
infection_rates = infection_rates.to_numpy()
# function to be called in simulation to pull out the relevent infection rate for the month the user can input
def infection_rate(month):
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
    return inf_rate



