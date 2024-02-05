#!/usr/bin/env phython3

#the usage for this script by a .sh script
#read all .tsv diles in data/ dir passed as the first argument(sys.argv[1]), and plot somethings
#python3 lab05.py data/

import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

cpiall_path = 'mycpiall.csv';
cpicity_path = 'mycpicity.csv';
exrate_path = 'myexrate.csv';

cpiall = pd.read_csv(cpiall_path, sep=',', header=0)
cpicity = pd.read_csv(cpicity_path, sep=',', header=0)
exrate = pd.read_csv(exrate_path, sep=',', header=0)

import datetime;
import calendar; #REV; we can get month names from numbers etc.

#plot 1
#monthly change of cpi from 1970 to 2023, for 10 major group index
print(cpiall.columns);
cpiall['datestr'] = cpiall.year.astype(str) + '-' + cpiall.month.astype(str) + '-' + '28'; #all months are 28
print(cpiall['datestr'].head(5));
cpiall['date'] = pd.to_datetime(cpiall['datestr'], format='%Y-%m-%d');
print(cpiall['date'].head(5));

fig1 = plt.figure(figsize=(10,7));
cpiall = cpiall.sort_values(by='date').reset_index(drop=True);

plt.plot(cpiall.date, cpiall.総合, label='All items', color='black', linewidth=3.5);
windowsize=12; #rolling average 12month a year
cpiall['rollave_all'] = cpiall.総合.rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_all, label='Rolling Ave', color='black', linestyle='dashed', linewidth=3.5);

plt.plot(cpiall.date, cpiall.食料, label='Food', color='red');
cpiall['rollave_food'] = cpiall.食料.rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_food, label='Rolling Ave', color='red', linestyle='dashed');

plt.plot(cpiall.date, cpiall.住居, label='Housing', color='blue');
cpiall['rollave_housing'] = cpiall.住居.rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_housing, label='Rolling Ave', color='blue', linestyle='dashed');

plt.plot(cpiall.date, cpiall['光熱・水道'], label='Fuel, light and water', color='green');
cpiall['rollave_energy'] = cpiall['光熱・水道'].rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_energy, label='Rolling Ave', color='green', linestyle='dashed');

plt.plot(cpiall.date, cpiall['家具・家事用品'], label='Furniture', color='purple');
cpiall['rollave_furniture'] = cpiall['家具・家事用品'].rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_furniture, label='Rolling Ave', color='purple', linestyle='dashed');

plt.plot(cpiall.date, cpiall.被服及び履物, label='Clothing', color='orange');
cpiall['rollave_clothing'] = cpiall.被服及び履物.rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_clothing, label='Rolling Ave', color='orange', linestyle='dashed');

plt.plot(cpiall.date, cpiall['交通・通信'], label='Transportation', color='brown');
cpiall['rollave_transport'] = cpiall['交通・通信'].rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_transport, label='Rolling Ave', color='brown', linestyle='dashed');

plt.plot(cpiall.date, cpiall.教育, label='Education', color='pink');
cpiall['rollave_education'] = cpiall.教育.rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_education, label='Rolling Ave', color='pink', linestyle='dashed');

plt.plot(cpiall.date, cpiall.保健医療, label='Medical care', color='cyan');
cpiall['rollave_medical'] = cpiall.保健医療.rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_medical, label='Rolling Ave', color='cyan', linestyle='dashed');

plt.plot(cpiall.date, cpiall.教養娯楽, label='Culture and recreation', color='gray');
cpiall['rollave_culture'] = cpiall.教養娯楽.rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_culture, label='Rolling Ave', color='gray', linestyle='dashed');

plt.plot(cpiall.date, cpiall.諸雑費, label='Others', color='olive');
cpiall['rollave_others'] = cpiall.諸雑費.rolling(window=windowsize).mean();
plt.plot(cpiall.date,cpiall.rollave_others, label='Rolling Ave', color='olive', linestyle='dashed');

# Set x-axis major ticks to a 5-year interval
plt.gca().xaxis.set_major_locator(mdates.YearLocator(base=5));
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'));

plt.axhline(100, linestyle='--', color=(0.5,0.5,0.5));#for 2020=100
plt.xlabel("Date (Year-Month)");
plt.ylabel("CPI (Year2020 = 100)");
plt.legend(loc='lower right', ncol=2);
plt.title("Monthly CPI For Every Year ({}-{})".format(cpiall.year.min(), cpiall.year.max()));

#plt.show();#show the plot
plt.savefig('figure1.png');
plt.clf();#clear the plot
print("figure1.png created");

#plot 2
#monthly change of exchange rate from 1970 to 2023
#the higher, the weaker of JPY (1 dollar = ? JPY)
print(exrate.columns);
print(exrate['date'].head(5));
exrate['date'] = pd.to_datetime(exrate['date'], format='%Y-%m-%d');

#exrate_monthly = exrate.groupby([exrate.date.dt.year, exrate.date.dt.month]).mean().reset_index();
#exratem = exrate.resample('ME', on='date').mean().reset_index(); #ME is not a valid frequency on my server
#but locally, FutureWarning: 'M' is deprecated and will be removed in a future version, please use 'ME' instead.
exratem = exrate.resample('M', on='date').mean().reset_index();
exratem.head(5);
#exratem.date = pd.to_datetime(exratem.date, format='%Y-%m-%d');
exratem.rename(columns={' value':'value'}, inplace=True);
#turn year into integer
exratem['year'] = exratem.date.dt.year;
exratem['month'] = exratem.date.dt.month; 
print(exratem.columns);


fig2 = plt.figure(figsize=(10,7));
plt.plot(exratem.date, exratem.value, color='black', label='Monthly');
windowsize=12; #12month a year
exratem['rollave'] = exratem.value.rolling(window=windowsize).mean();
plt.plot(exratem.date,exratem.rollave, label='Rolling Ave', color='black', linestyle='dashed');
# Set x-axis major ticks to a 5-year interval
plt.gca().xaxis.set_major_locator(mdates.YearLocator(base=5));
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'));
plt.xlabel("Date (Year-Month)");
plt.ylabel("Exchange rate (USD to JPY)");
plt.legend(loc='upper right');
plt.title("Monthly Exchange Rate For Year ({}-{})".format(exratem.year.min(), exratem.year.max()));

#plt.show();#show the plot
plt.savefig('figure2.png');
plt.clf();#clear the plot
print("figure2.png created");


#plot 3
#scatter plot of cpi and exchange rate
#only the rows with matching b values in both DataFrames are included in the result.
df = pd.merge(cpiall, exratem, on=['year', 'month'], how='inner');#inner join
#add  3 labels to the scatter plot
lab = [1990,1995,2020,2023];
x = [df.value[df.year==1990].values[0],df.value[df.year==1995].values[0], df.value[df.year==2020].values[0], df.value[df.year==2023].values[0]];
y= [df.総合[df.year==1990].values[0], df.総合[df.year==1995].values[0], df.総合[df.year==2020].values[0], df.総合[df.year==2023].values[0]];

fig3 = plt.figure(figsize=(10,7));
#cmap specifies the colormap used to map numbers to colors
plt.scatter(df.value, df.総合, c=df.year, cmap='viridis', s=50, alpha=0.5);
plt.colorbar(label='Year');

for i, txt in enumerate(lab):
    plt.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center');

plt.xlabel("Exchange rate (USD to JPY)");
plt.ylabel("CPI (Year2020 = 100)");
plt.legend(loc='upper right');
plt.title("Scatter Plot of CPI (all items) and Exchange Rate");

#plt.show();#show the plot
plt.savefig('figure3.png');
plt.clf();#clear the plot
print("figure3.png created")