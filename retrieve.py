# Time
from datetime import datetime, timedelta
from dateutil.parser import parse # to parse strings as dates
import pytz # for timeZones
# Dataframe
import pandas as pd 
# Json connection for wind
import requests
# Json connection for swell
import shutil
import urllib.request as request
from contextlib import closing


# get current time
tzAus = pytz.timezone('Australia/Sydney')
currentTimeTZ = datetime.now(tzAus)
currentTime = datetime(currentTimeTZ.year, currentTimeTZ.month, currentTimeTZ.day, \
currentTimeTZ.hour, currentTimeTZ.minute, 0) # make timezone naive for comparison later

# domain from 6 hours ago for next 24 hours
startTime = currentTime - timedelta(hours=6) 
finishTime = (currentTime + timedelta(hours=18))

# constant to convert knots to km/h
knToKmph = 1.852

# for wind data. e.g. northerly 'N' means heading south (180deg anti-c from N)
directionDict = { 
  'NE': 135, 'NNE': 157.5, 'N': 180, 'NNW': -157.5, 'NW': -135,
  'WNW': -112.5, 'W': -90, 'WSW': -67.5,
  'SW': -45, 'SSW': -22.5, 'S': 0, 'SSE': 22.5, 'SE': 45,
  'ESE': 67.5, 'E': 90, 'ENE': 112.5
}

# pandas dataframes for: wind/swell obswervation/forecast
def getDataFrames():
  frames = {}
  frames['WindObservation'] = initObservationWind()
  frames['WindForecast'] = initForecastWind()
  frames['SwellObservation'] = initObservationSwell()
  frames['SwellForecast'] = initForecastSwell()
  frames['Daylight'] = initDaylight()
  return frames

def initObservationWind():
  try:
    # from http://www.bom.gov.au/products/IDN60801/IDN60801.95745.shtml#other_formats under JSON link
    r = requests.get(url = "http://www.bom.gov.au/fwo/IDN60701/IDN60701.95745.json")
    data = r.json() 
    dataList = data['observations']['data']
    
    dates = []
    speeds = []
    directions = []
    
    for pnt in dataList:
      date = parse(pnt['local_date_time_full'])
      if(startTime <= date and date <= finishTime):
        dates.append(date)
        speeds.append(pnt['wind_spd_kt'] * knToKmph)
        directions.append(directionDict[pnt['wind_dir']])
    
    df = pd.DataFrame(index=dates)
    df['speed'] = speeds # km/h
    df['direction'] = directions # towards anti-c +ve from N in degrees
    
    return df
    
  except requests.exceptions.RequestException as e:
    print('ERROR with requests.get() :\n' + str(e))

def initForecastWind():
  try:
    # from https://github.com/tonyallan/weather-au use the first two links under 'Weather API'
    r = requests.get(url = "https://api.weather.bom.gov.au/v1/locations/r3g7cg/forecasts/3-hourly")
    data = r.json() 
    dataList = data['data']
    
    dates = []
    speeds = []
    directions = []
    for pnt in dataList:
      date = parse(pnt['time']).replace(tzinfo=None)
      if(currentTime <= date and date <= finishTime):
        dates.append(date)
        speeds.append(pnt['wind']['speed_kilometre'])
        directions.append(directionDict[pnt['wind']['direction']])
    
    df = pd.DataFrame(index=dates)
    df['speed'] = speeds # km/h
    df['direction'] = directions # towards anti-c +ve from N in degrees
    return df
    
  except requests.exceptions.RequestException as e:
    print('ERROR with requests.get() :\n' + str(e))

# public version returns a blank data frame for private url
def initObservationSwell():
  # opens the csv at a given <url> and saves it in this directory as swell_observation.
  # with closing(request.urlopen(<url>)) as r:
  #   with open('swell_observation', 'wb') as f:
  #     shutil.copyfileobj(r, f)
  
  # with open('swell_observation') as f:
  #   lineList = f.readlines()
  
  # dates = []
  # heights = []
  # directions = []
  
  # lineList = list(x.replace('\n', '') for x in lineList)
  # lineList = list(filter(lambda x: x != '', lineList))
  # for i in range(1, len(lineList)): 
  #   row = lineList[i].split(",")
    
  #   date = parse(row[<x>])
  #   if(startTime <= date and date <= finishTime):
  #     dates.append(date)
  #     heights.append(float(row[<x>])) # hSig define below
  #     directions.append(180 - int(row[<x>])) # 180 - bearing is anti-c +ve from North
  
  # df = pd.DataFrame(index=dates)
  # df['height'] = heights
  # df['direction'] = directions
  # return df
  return pd.DataFrame() 

# public version returns a blank data frame for private url
def initForecastSwell():
  # opens the csv at a given <url> and saves it in this directory as swell_forecast.
  # with closing(request.urlopen(<url>)) as r:
  #   with open('swell_forecast', 'wb') as f:
  #     shutil.copyfileobj(r, f)
  
  # with open('swell_forecast') as f:
  #   lineList = f.readlines()
  
  # dates = []
  # heights = []
  # directions = []
  
  # lineList = list(x.replace('\n', '') for x in lineList)
  # lineList = list(filter(lambda x: x != '', lineList))
  # for i in range(1, len(lineList)):
  #   row = lineList[i].strip().split(",")
  #   date = parse(row[<x>])
  #   if(currentTime <= date and date <= finishTime):
  #     dates.append(date)
  #     heights.append(float(row[<x>])) # Hsm define below
  #     directions.append(180 - float(row[<x>])) # 180 - bearing is anti-c +ve from North (Dirf)
  
  # df = pd.DataFrame(index=dates)
  # df['height'] = heights
  # df['direction'] = directions
  # return df
  return pd.DataFrame() 

def initDaylight():
  day = '#FFFA4F' # day yellow colour for da sun :)
  night = '#7733FF' # puple night colour
  current = 'c' # cyan color to indicate the current time. Included in last df row
  
  # Thanks to the devs at Sunrise - Sunset. See https://sunrise-sunset.org/api
  r = requests.get(url = "https://api.sunrise-sunset.org/json?lat=-34.5&lng=150.9&formatted=0")
  data = r.json() 
  
  # civil_twilight_begin/civil_twilight_end is civil_dawn/civil_dusk or firstlight/lastlight
  # civil_dawn/civil_dusk is roughly when artificial light is suggested for outdoor activities like sarfing
  firstLightRaw = parse(data['results']['civil_twilight_begin'])
  lastLightRaw = parse(data['results']['civil_twilight_end'])

  firstLight = firstLightRaw.astimezone(tzAus).replace(tzinfo=None)
  lastLight = lastLightRaw.astimezone(tzAus).replace(tzinfo=None)

  fL_hour = firstLight.hour
  fL_min = firstLight.minute
  lL_hour = lastLight.hour
  lL_min = lastLight.minute

  day_delta = lastLight - firstLight
  night_delta = timedelta(hours=24) - day_delta

  df = pd.DataFrame()
  firstTime = startTime # first time before start where day/night transition occurs
  if ((not isBeforeTime(startTime, fL_hour, fL_min)) and isBeforeTime(startTime, lL_hour, lL_min)): # day light
    firstTime = startTime.replace(hour=fL_hour, minute=fL_min)
    df['lightColor'] = [day, night, day, current]
    df['lightStartTime'] = [
      firstTime, 
      firstTime + day_delta,
      firstTime + day_delta + night_delta,
      currentTime - timedelta(minutes=5)
    ]
    df['lightFinishTime'] = [
      firstTime + day_delta, # the first interval is day so add the daylight duration
      firstTime + day_delta + night_delta,
      firstTime + day_delta + night_delta + day_delta,
      currentTime + timedelta(minutes=5)
    ]
  else:
    if((not isBeforeTime(startTime, lL_hour, lL_min)) and isBeforeTime(startTime, 24, 0)): # arvo night
      firstTime = startTime.replace(hour=lL_hour, minute=lL_min)
    else: # early hours
      firstTime = startTime - timedelta(hours=fL_hour, minutes=fL_min)
      firstTime = firstTime.replace(hour=lL_hour, minute=lL_min)
    df['lightColor'] = [night, day, night, current]
    df['lightStartTime'] = [
      firstTime, 
      firstTime + night_delta,
      firstTime + night_delta + day_delta,
      currentTime - timedelta(minutes=5)
    ]
    df['lightFinishTime'] = [
      firstTime + night_delta, # the first interval is night so add the night duration
      firstTime + night_delta + day_delta,
      firstTime + night_delta + day_delta + night_delta,
      currentTime + timedelta(minutes=5)
    ]
  return df

def isBeforeTime(date, hour, minute):
  return (date.hour < hour) or (date.hour == hour and date.minute < minute)