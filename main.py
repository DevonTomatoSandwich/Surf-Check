from retrieve import * # backend
from graph import * # frontend


def main():
  
  # pandas dataframes for: wind/swell obswervation/forecast
  frames = getDataFrames()
  
  # plots the dataframes using matplotlib
  graph(frames)
  
main()