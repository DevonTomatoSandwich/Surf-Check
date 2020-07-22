# Kook-Check
Python graphs showing surf conditions at Port Kembla (Australia NSW) 

## What does it show?
![](https://github.com/DevonTomatoSandwich/Kook-Check/blob/master/readme_pic.png)


- Observed wind speed and direction in blue
- Forecast wind speed and direction in red
- Observed swell height and direction in blue
- Forecast swell height and direction in red
- First/last light in yellow/purple transition
- Current time indicated by cyan line
- Shows all conditions between 6 hours ago and 18 hours ahead (i.e. 24 hour window)

## How to run
[Run using repl](https://repl.it/@billybud/Kook-Check)

The code for the repl can also be found in the repl folder here

## The tech

Kook Check is built in python. It requests data in time indexed pandas dataframes and outputs using matplotlib. 
Wind data is taken from [BOM](http://www.bom.gov.au/). Swell data is taken from [forecast.waves.nsw.gov.au](forecast.waves.nsw.gov.au). 
First/last light times are from [Sunrise - Sunset 's api](https://sunrise-sunset.org/api) (thanks!). The requested data format is either JSON or CSV.

The website_root folder shows important content that exists in the root folder for my website. My website runs a flask backend which can run the python code to generate the matplotlib image. This is then sent to the react frontend and displayed.

## Why?
Surfers arn't as simple as they seem. A keen surfer will check conditions before heading out. 
This means looking at graphs and interpreting data quickly. Some sites like coastal watch and swellnet 
are effective but graphs can be convuluted by multiple y axes and irrelevant data. 
Some basic information that you need is the wind and swell data.

## Future

- [ ] The code is not published yet but can be ran on repl (see how to run)

