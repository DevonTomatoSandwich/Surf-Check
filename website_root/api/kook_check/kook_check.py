from ..kook_check import globals
from .retrieve import *
from .graph import *

def generate_kook_plot():
  print('generate_kook_plot called')
  globals.initGlobalTimes()
  # pandas dataframes for: wind/swell obswervation/forecast
  frames = getDataFrames()
  
  # plots the dataframes using matplotlib
  plt = graph(frames)

  return plt