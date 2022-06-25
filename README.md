# Surf-Check
Python graphs showing surf conditions at Port Kembla (Australia NSW) 

## What does it show?
![](https://github.com/DevonTomatoSandwich/Surf-Check/blob/master/readme_pic.png)


- Observed wind speed and direction in blue
- Forecast wind speed and direction in red
- Observed swell height and direction in blue
- Forecast swell height and direction in red
- First/last light in yellow/purple transition
- Current time indicated by cyan line
- Shows all conditions between 6 hours ago and 18 hours ahead (i.e. 24 hour window). Can be changed in config.json

## Code Structure

All the python code is in `surf_check.ipynb`. This file retrieves data from various sources and graphs the chart in the final cell.

Timezone, time domain and location are specified in `config.json`.

A map of compass direction to bearing ° TNorth of motion direction is specified in `directions.json`.

Coordinates for the downward pointng arrow marker are specified in `arrow.csv`.

## How to run

Install the classic Jupyter Notebook with:

`pip install notebook`

To run the notebook:

`jupyter notebook`


## The tech

Surf Check is built in python. It requests data in time indexed pandas dataframes and outputs using matplotlib. 
Wind data is taken from [BOM](http://www.bom.gov.au/). Swell data is taken from [forecast.waves.nsw.gov.au](forecast.waves.nsw.gov.au). 
First/last light times are from [Sunrise - Sunset 's api](https://sunrise-sunset.org/api) (thanks!). The requested data format is either JSON or CSV.

## Why?
Surfers arn't as simple as they seem. A keen surfer will check conditions before heading out. 
This means looking at graphs and interpreting data quickly. Some sites like coastal watch and swellnet are effective but graphs can be convoluted by multiple y axes and irrelevant data. 
Some basic information that you need is the wind and swell data.
