import requests
import pandas as pd
# Time
import globals
from datetime import datetime, timedelta
from dateutil.parser import parse
import pytz # for timeZones

# constant to convert knots to km/h
knToKmph = 1.852

# for wind data. the angle is where the wind is coming from, measured anti-c from N
# e.g. westerly 'W' means heading east (pointing -90deg anti-c from N)
directionDict = { 
  'NE': 135, 'NNE': 157.5, 'N': 180, 'NNW': -157.5, 'NW': -135,
  'WNW': -112.5, 'W': -90, 'WSW': -67.5,
  'SW': -45, 'SSW': -22.5, 'S': 0, 'SSE': 22.5, 'SE': 45,
  'ESE': 67.5, 'E': 90, 'ENE': 112.5,
  'CALM': -90
}

# pandas dataframes for: wind/swell obswervation/forecast
def getDataFrames():
  frames = {}
  frames['WindObservation'] = initObservationWind()
  frames['WindForecast'] = initForecastWind()
  frames['SwellObservation'], frames['SwellForecast'] = initSwell()
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
      if(globals.startTime <= date and date <= globals.finishTime):
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
      if(globals.currentTime <= date and date <= globals.finishTime):
        dates.append(date)
        speeds.append(pnt['wind']['speed_kilometre'])
        directions.append(directionDict[pnt['wind']['direction']])
    
    df = pd.DataFrame(index=dates)
    df['speed'] = speeds # km/h
    df['direction'] = directions # towards anti-c +ve from N in degrees
    return df
    
  except requests.exceptions.RequestException as e:
    print('ERROR with requests.get() :\n' + str(e))

def initSwell():
  # 3000876 is the location coming into port kembla main beach @30m depth
  url = 'https://forecast.waves.nsw.gov.au/?page=series&id=3000876'
  
  response = requests.get(url)
  itemList = response.text.split("\n")
  
  DateObserved = []
  DateForecast = []
  Hsm = []
  # Tpm = [] # T is period (might need later)
  Dirm = []
  Hsf = []
  # Tpf = []
  Dirf = []
  
  itemList.pop(0) # pops heading: Date,Hsm,Tpm,Dirm,Hsf,Tpf,Dirf
  for x in itemList: 
    row = x.split(",")
    if len(row) != 7:
      continue
    
    if row[1] != '': # observed height exists
      DateObserved.append(parse(row[0]))
      Hsm.append(float(row[1]))
      Dirm.append(180 - float(row[3]))
    if row[4] != '': # forecast height exists
      DateForecast.append(parse(row[0]))
      Hsf.append(float(row[4]))
      Dirf.append(180 - float(row[6]))
  
  dfObserved = pd.DataFrame(index=DateObserved)
  dfObserved['height'] = Hsm # Nearshore significant wave height tranformation from measured (m)
  dfObserved['direction'] = Dirm # Nearshore wave direction transformation from measured (° TNorth)
  
  dfForecast = pd.DataFrame(index=DateForecast)
  dfForecast['height'] = Hsf # Nearshore significant wave height tranformation from forecast (m)
  dfForecast['direction'] = Dirf # Nearshore wave direction transformation from forecast (° TNorth)
  
  return dfObserved, dfForecast

def initDaylight():
  day = '#FFFA4F' # day yellow colour for da sun :)
  night = '#7733FF' # puple night colour
  current = 'c' # cyan color to indicate the current time. Included in last df row
  
  # Thanks to the devs at Sunrise - Sunset. See https://sunrise-sunset.org/api
  r = requests.get(url = "https://api.sunrise-sunset.org/json?lat=-34.5&lng=150.9&formatted=0")
  data = r.json() 
  
  # civil_twilight_begin/civil_twilight_end is civil_dawn/civil_dusk or firstlight/lastlight
  # civil_dawn/civil_dusk is rougly the time needed where 
  # artificial light should be used for outdoor activities
  firstLightRaw = parse(data['results']['civil_twilight_begin'])
  lastLightRaw = parse(data['results']['civil_twilight_end'])

  firstLight = firstLightRaw.astimezone(globals.tzAus).replace(tzinfo=None)
  lastLight = lastLightRaw.astimezone(globals.tzAus).replace(tzinfo=None)

  fL_hour = firstLight.hour
  fL_min = firstLight.minute
  lL_hour = lastLight.hour
  lL_min = lastLight.minute

  day_delta = lastLight - firstLight
  night_delta = timedelta(hours=24) - day_delta

  df = pd.DataFrame()
  firstTime = globals.startTime # first time before start where day/night transition occurs
  if ((not isBeforeTime(globals.startTime, fL_hour, fL_min)) and isBeforeTime(globals.startTime, lL_hour, lL_min)): # day light
    firstTime = globals.startTime.replace(hour=fL_hour, minute=fL_min)
    df['lightColor'] = [day, night, day, current]
    df['lightStartTime'] = [ 
      firstTime, 
      firstTime + day_delta,
      firstTime + day_delta + night_delta,
      globals.currentTime - timedelta(minutes=5)
    ]
    df['lightFinishTime'] = [
      firstTime + day_delta, # the first interval is day so add the daylight duration
      firstTime + day_delta + night_delta,
      firstTime + day_delta + night_delta + day_delta,
      globals.currentTime + timedelta(minutes=5)
    ]
  else:
    if((not isBeforeTime(globals.startTime, lL_hour, lL_min)) and isBeforeTime(globals.startTime, 24, 0)): # arvo night
      firstTime = globals.startTime.replace(hour=lL_hour, minute=lL_min)
    else: # early hours
      firstTime = globals.startTime - timedelta(hours=fL_hour, minutes=fL_min)
      firstTime = firstTime.replace(hour=lL_hour, minute=lL_min)
    df['lightColor'] = [night, day, night, current]
    df['lightStartTime'] = [ 
      firstTime, 
      firstTime + night_delta,
      firstTime + night_delta + day_delta,
      globals.currentTime - timedelta(minutes=5)
    ]
    df['lightFinishTime'] = [
      firstTime + night_delta, # the first interval is night so add the night duration
      firstTime + night_delta + day_delta,
      firstTime + night_delta + day_delta + night_delta,
      globals.currentTime + timedelta(minutes=5)
    ]
  return df

def isBeforeTime(date, hour, minute):
  return (date.hour < hour) or (date.hour == hour and date.minute < minute)