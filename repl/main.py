import globals
from retrieve import getDataFrames # backend
from graph import graphDataFrames # frontend

def main():
  print('main called')
  globals.initGlobalTimes()
  # pandas dataframes for: wind/swell obswervation/forecast
  frames = getDataFrames()
  
  # plots the dataframes using matplotlib
  graphDataFrames(frames)
  
main()