from datetime import datetime, timedelta
import pytz # for timeZones

currentTime = None
startTime = None
finishTime = None
tzAus = None

def initGlobalTimes():
  global currentTime
  global startTime
  global finishTime
  global tzAus

  # get current time
  tzAus = pytz.timezone('Australia/Sydney')
  currentTimeTZ = datetime.now(tzAus)
  currentTime = datetime(currentTimeTZ.year, currentTimeTZ.month, currentTimeTZ.day, \
  currentTimeTZ.hour, currentTimeTZ.minute, 0) # make timezone naive for comparison later

  print('From globals.py, currentTime = ' + str(currentTime))

  # domain from 6 hours ago for next 24 hours
  startTime = currentTime - timedelta(hours=6) 
  finishTime = (currentTime + timedelta(hours=18))