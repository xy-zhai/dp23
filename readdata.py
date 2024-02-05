#!/usr/bin/env python3

#Data comes from the website https://www.e-stat.go.jp/stat-search/files?tclass=000001138364&cycle=1&year=20230&month=24101212

#import sys
#cpiall_path = sys.argv[1];
#cipcity_path = sys.argv[2];
#exchangerate_path = sys.argv[3];

#path for local testing
cpiall_path = './japancpi/cpi_all.csv'
cipcity_path = './japancpi/cpi_city.csv'
exchangerate_path = './japancpi/exchange_rate.csv'

import pandas as pd
import numpy as np

cpiall = pd.read_csv(cpiall_path, sep=',', encoding='utf-8')
cpicity = pd.read_csv(cipcity_path, sep=',', encoding='utf-8')
#problem by reading csv with diff col
exchangerate = pd.read_csv(exchangerate_path, names = range(2), sep=',', encoding='utf-8') #more seperator in specific row

#first look at the data
print(cpiall.head(5));
print(cpicity.head(5));
print(exchangerate.head(5));


#1. Data cleaning for cpiall
#find the index for "類・品目符号" and save related data as a new dataframe
catrowidx = None;
catcolidx = None;

for j in range(0, len(cpiall.columns)):
    for i in range(0, len(cpiall)):
        if cpiall.iloc[i, j] == "類・品目符号":
            catrowidx = i;
            catcolidx = j;
            break;
    if catrowidx != None:
        break;

print(catrowidx, catcolidx);#7,11
#save the data for "類・品目符号" as a new dataframe
cpitype = cpiall.iloc[catrowidx:(catrowidx+3), catcolidx:];
cpitype = cpitype.reset_index(drop=True);
print(cpitype.head(5));

#find the col for "年月", and drop the col before it
#search for the index for the "年月"
rowidx = None;
colidx = None;
for j in range(0, len(cpiall.columns)):
    for i in range(0, len(cpiall)):
        if cpiall.iloc[i, j] == "年月":
            rowidx = i;
            colidx = j;
            break;
    if rowidx != None:
        break;

print(rowidx, colidx);#12,8
#drop the col before "年月"
cpiall = cpiall.iloc[rowidx:, colidx:]
print(cpiall.head(5));

#replace the "単位なし" by category name
idx = [cpiall.columns.get_loc(j) for j in cpitype.columns];
print(idx);
cpiall.iloc[0, idx] = cpitype.iloc[1,];
print(cpiall.head(5));  


cpiall.iloc[0,];
cpiall.columns = cpiall.iloc[0,];
cpiall = cpiall.iloc[1:,];
cpiall = cpiall.reset_index(drop=True);
print(cpiall.head(5));

#save the data for "年月"(yearandmonth) for 2 new col for year and month
cpiall['year'] = cpiall['年月'].str.extract(r'(\d+)年')[0];
cpiall['month'] = cpiall['年月'].str.extract(r'(\d+)月')[0];
print(cpiall.head(5));

#drop the col before " 総合"(total), no use
dropidx = cpiall.columns.get_loc('総合'); 
cpiall = cpiall.iloc[:, dropidx:];
cpiall = cpiall.reset_index(drop=True);
#add note for final version
print('THIS IS THE FINAL VERSION FOR CPIALL');
print(cpiall.head(5));


#2. Data cleaning for cipcity
## drop all cols including a value of "%"
dropcolidx2 = [i for i in range(0, len(cpicity.columns)) if '％' in cpicity.iloc[:, i].values];
print(dropcolidx2);
cpicity = cpicity.drop(cpicity.columns[dropcolidx2], axis=1);
cpicity = cpicity.reset_index(drop=True);
print(cpicity.head(20));


## find the index for "類・品目符号" and save related data as a new dataframe
len(cpicity)
catrowidx2 = [i for i in range(0, len(cpicity)) if '類・品目符号' in cpicity.iloc[i,:].values];
catcolidx2 = [j for j in range(0, len(cpicity.columns)) if '類・品目符号' in cpicity.iloc[:, j].values];
print(catrowidx2, catcolidx2); #[7],[11] 

cpicitytype = cpicity.iloc[catrowidx2[0]:catrowidx2[0]+3, catcolidx2[0]:]; #[0] for 1st elements of the list
print(cpicitytype);


## find the index of "年月"
rowidx2 = [i for i in range(0, len(cpicity)) if '年月' in cpicity.iloc[i,:].values];
colidx2 = [j for j in range(0, len(cpicity.columns)) if '年月' in cpicity.iloc[:, j].values];
print(rowidx2, colidx2); #[10],[8]
cpicity = cpicity.iloc[rowidx2[0]:, colidx2[0]:];
cpicity = cpicity.reset_index(drop=True);
print(cpicity.head(5));

## replace the "単位なし" by category name
b = cpicity.columns.intersection(cpicitytype.columns);
print(b);
b == cpicitytype.columns; #True, just for checking
binx = [cpicity.columns.get_loc(j) for j in b];
print(binx);
cpicity.iloc[0, binx] = cpicitytype.iloc[1,];
print(cpicity.head(5));

## set the 1st row as the col names
cpicity.iloc[0,]; #check the 1st row
cpicity.columns = cpicity.iloc[0,];
cpicity = cpicity.iloc[1:,];
cpicity = cpicity.reset_index(drop=True);
print(cpicity.head(5));

## fill "地域コード"(region code for japan cities) to 5 digits with 0 at the beginning
cpicity['地域コード'] = cpicity['地域コード'].astype(str).str.zfill(5);

## save the data for "年月"(yearandmonth) for 2 new col for year and month
cpicity['year'] = cpicity['年月'].str.extract(r'(\d+)年')[0];
cpicity['month'] = cpicity['年月'].str.extract(r'(\d+)月')[0];
## check col names
cpicity.columns;
cpicity = cpicity.drop('年月', axis=1);
cpicity = cpicity.drop('類・品目', axis=1);
print('THIS IS THE FINAL VERSION FOR CPICITY');
print(cpicity.head(5));


#3. Data cleaning for exchangerate
#find the row for date and drop the rows before it
rowidx3 = exchangerate[exchangerate[0] == 'date'].index.values; #return the index of the row with 'date'
print(exchangerate.iloc[rowidx3[0]:,]);
exchangerate = exchangerate.iloc[rowidx3[0]:,];
exchangerate = exchangerate.reset_index(drop=True);
#set header
exchangerate.columns = exchangerate.iloc[0,];
exchangerate = exchangerate.iloc[1:,];
exchangerate = exchangerate.reset_index(drop=True);
#add 3 new col for year, month and day
exchangerate['year'] = exchangerate['date'].str.extract(r'(\d+)-')[0];
exchangerate['month'] = exchangerate['date'].str.extract(r'-(\d+)-')[0];
exchangerate['day'] = exchangerate['date'].str.extract(r'-(\d+)$')[0];

#summarize the data
print('THIS IS THE FINAL VERSION FOR CPIALL');
print(cpiall.head(5));
print('THIS IS THE FINAL VERSION FOR CPICITY');
print(cpicity.head(5));
print('THIS IS THE FINAL VERSION FOR EXCHANGERATE');
print(exchangerate.head(5));  



#save as csv file
cpiall.to_csv('mycpiall.csv', index=False, encoding='utf-8');
cpicity.to_csv('mycpicity.csv', index=False, encoding='utf-8');
exchangerate.to_csv('myexrate.csv', index=False, encoding='utf-8');