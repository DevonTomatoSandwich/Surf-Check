# Time
from ..kook_check import globals

# Plotting
import matplotlib
matplotlib.use('Agg') # important for web
import matplotlib.pyplot as plt

import matplotlib as mpl
from matplotlib.dates import date2num
from matplotlib.lines import Line2D # legend
import matplotlib.dates as mdates # for formatting dates in graph
# Arrow marker
import numpy as np
from matplotlib.path import Path

# Arrow: arrowUp is the Path of a upward pointing arrow that will be later rotated
vertices = np.array([ 
  [ 0  ,  1],
  [ 1  ,  0],
  [ 0.3,  0],
  [ 0.3, -1],
  [-0.3, -1],
  [-0.3,  0],
  [-1  ,  0],
  [ 0  ,  1],  
]) 
codes = [Path.LINETO] * 8
codes[0] = Path.MOVETO
codes[-1] = Path.CLOSEPOLY
arrowUp = Path(vertices, codes)


# plots the dataframes using matplotlib
def graph(frames):
  
  # Pre formatting
  fig, ax = plt.subplots(2, sharex=True)
  fig.suptitle('Kook Check: Port Kembla', size='x-large')
  plt.subplots_adjust(top=0.95, bottom=0.15) # space for title and legend
  for a in ax:
    a.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
  plt.xticks(rotation=45)
  legend_elements = [
    Line2D([0], [0], color='b', lw=4, label='Observed'),
    Line2D([0], [0], color='r', lw=4, label='Forecast'),
    Line2D([], [], color='#1f77b4', marker='|', linestyle='None',\
    markersize=10, markeredgewidth=4, label='Current time')
  ]
  plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0,-0.6,1,0.2), mode="expand", borderaxespad=0, ncol=3) # plot outside chart

  ax[0].tick_params(bottom=False, top=False)
  ax[1].tick_params(bottom=False, top=False)
  fig.patch.set_facecolor('w')
  
  # Wind Subplot
  ax[0].set_title('Wind Speed (km/h)')
  box = ax[0].get_position()
  ax[0].set_position([box.x0*0.5, box.y0, box.width * 1.1, box.height * 0.8]) # makes space for legend
  if(not frames['WindObservation'].empty):
    plotMyDF(ax[0], frames['WindObservation'], 'speed', 'b')
  if(not frames['WindForecast'].empty):
    plotMyDF(ax[0], frames['WindForecast'], 'speed', 'r')
  
  # Swell Subplot
  ax[1].set_title('Swell Height (m)')
  box = ax[1].get_position()
  ax[1].set_position([box.x0*0.5, box.y0 + 0.07, box.width * 1.1, box.height * 0.8]) # makes space for legend
  if(not frames['SwellObservation'].empty):
    plotMyDF(ax[1], frames['SwellObservation'], 'height', 'b')
  if(not frames['SwellForecast'].empty):
    plotMyDF(ax[1], frames['SwellForecast'], 'height', 'r')
    
  
  # Daylight plotting
  for index, row in frames['Daylight'].iterrows():
    ax[0].axvspan(date2num(row['lightStartTime']), date2num(row['lightFinishTime']), facecolor=row['lightColor'], alpha=0.5)
    ax[1].axvspan(date2num(row['lightStartTime']), date2num(row['lightFinishTime']), facecolor=row['lightColor'], alpha=0.5)

  # Post formatting
  plt.xlim(globals.startTime, globals.finishTime)
  ax[0].set_ylim(-1, getMaxSpeed(frames)) # ranges
  ax[1].set_ylim(-0.2, getMaxHeight(frames))
  ax[0].grid(axis='x') # gridlines must be set after plotting
  ax[1].grid(axis='x')
  fig.canvas.draw() # extra formatting for label text
  labels = [item.get_text() for item in ax[1].get_xticklabels()]
  for i, s in enumerate(labels):
    if len(s) != 0:
      if s[2:5] == ':00':
        s = s[:2] + s[5:]
      if s[0] == '0':
        s = s[1:]
      labels[i] = s
  ax[1].set_xticklabels(labels, rotation=45, ha='right')

  # save png to file (for repl)
  # plt.savefig('./react/kook_plot.png')
  # plt.show()
  return plt
  
def getMaxSpeed(frames): # plotting y limits for speed
  smallestMax = 50 # plot shows up to at least 50km/h
  extraSpace = 5 # range between top speed and top of plot if over smallestMax 
  speedListObs = frames['WindObservation']['speed']
  speedListFor = frames['WindForecast']['speed']
  if(frames['WindObservation'].empty):
    return max(max(speedListFor) + extraSpace, smallestMax)
  if(frames['WindForecast'].empty):
    return max(max(speedListObs) + extraSpace, smallestMax)
  return max(max(max(speedListObs), max(speedListFor)) + extraSpace, smallestMax)
  
def getMaxHeight(frames): # plotting y limits for height
  smallestMax = 3 # plot shows up to at least 3m
  extraSpace = 1 # range between top height and top of plot if over smallestMax 
  heightListObs = frames['SwellObservation']['height']
  heightListFor = frames['SwellForecast']['height']
  if(frames['SwellObservation'].empty):
    return max(max(heightListFor) + extraSpace, smallestMax)
  if(frames['SwellForecast'].empty):
    return max(max(heightListObs) + extraSpace, smallestMax)
  return max(max(max(heightListObs), max(heightListFor)) + extraSpace, smallestMax)

def plotMyDF(ax, df, colVal, color): # for plotting each dataframe
  ax.plot(df.index, df[colVal], c=color) # line between points
  for i, angleTo in enumerate(df['direction']):
    new_star = arrowUp.transformed(mpl.transforms.Affine2D().rotate_deg(angleTo))
    ax.plot(df.index[i],df[colVal][i], color, marker=new_star, markersize=10) # arrow on points