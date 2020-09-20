#!/user/bin/env python3 -W ignore
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import sys
## Define the default values
parser = argparse.ArgumentParser()
parser.add_argument('-csv'   , action='store',dest='csvfile',help='path to csvfile first column x axis',type=str)
parser.add_argument('-xlabel', action='store',dest='xlabel' ,help='label for the x axis',type=str)
parser.add_argument('-ylabel', action='store',dest='ylabel' ,help='label for the y axis',type=str)
parser.add_argument('-output', action='store',dest='output' ,help='name of the output file',type=str)
parser.add_argument('-title', action='store' ,dest='title'  ,help='title of the plot',type=str)
results = parser.parse_args()

if not (results.csvfile): sys.exit("Error:csv file not defined")
if not (results.output): results.output = "mylineplot"
if not (results.title): results.title = "mytitle"
file = open(results.csvfile,'r')
df = pd.read_csv(file)

## Testing stuff
#print(df)
#print('Max', df['3x'].max())
#print('Min', df['2x'].min())

X = list(df)
myplot=df.plot(X[0],X[1:])
myplot.set_xlabel(results.xlabel)
myplot.set_ylabel(results.ylabel)
plt.title(results.title)
plt.savefig(results.output)
