# Kook-Check
Python graphs showing surf conditions at Port Kembla (Australia NSW) 

# What do kooks need?
Surfers arn't as simple as they seem. A keen surfer will check conditions before heading out. This means looking at graphs and interpreting data quickly. Some sites like coastal watch and swellnet are effective but graphs can be convuluted by multiple y axes and irrelevant data. Some basic information that you need is the wind and swell data. Some surfers plan ahead for travelling however for a kook stuck in port kembla you only need to know the immediate conditions. This leads to the name 'Kook Check' i.e a place for kooks to check!

## What does it show?
![](https://github.com/DevonTomatoSandwich/Kook-Check/blob/master/readme_pic.png)


- Observed wind speed and direction in blue
- Forecast wind speed and direction in red
- Observed swell height and direction in blue
- Forecast swell height and direction in red
- First/last light in yellow/purple transition
- Current time indicated by cyan line
- Shows all conditions between 6 hours ago and 18 hours ahead (i.e. 24 hour window)

## how to run
todo

## The techsplination


Kook Check is built in python. It requests data in time indexed pandas dataframes and outputs using matplotlib. All data is taken from BOM except first/last light times which is from Sunrise - Sunset 's api (thanks!). See https://sunrise-sunset.org/api. The requested data format is either JSON or CSV. 


## Future

- [ ] write how to run
- [ ] The code is not published yet but can be ran on repl (see how to run)

