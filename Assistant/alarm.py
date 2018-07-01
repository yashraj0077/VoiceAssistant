import time
import datetime
import threading
import pyttsx


alarms = []

def speech(script):
    engine = pyttsx.init()
    engine.setProperty('rate', engine.getProperty('rate')-20)
    engine.say(script)
    engine.runAndWait()


def setAlarm(request):
    request = request.split(" ")
    if "tomorrow" in request:
        delta = 1
    else:
        try:
            delta = int(request[request.index("days")-1])
        except:
            delta = 0
    try:
        hour = int(request[request.index("hour")+1])
        minute = int(request[request.index("minute")+1])
        alarm.append(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=delta, hours=hour, minutes=minute))
        return "Alarm set for tomorrow at " + hour + " : " + minute
    except:
        try:
            hour = int(request[request.index("hour")+1:])
            alarm.append(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=delta, hours=hour))
            return "Alarm set for tomorrow at " + hour + " O'clock"
        except:
            return "Sorry could not understant the time"


def alarmLoop():
    while True:
        for alarm in alarms:
            if alarm == datetime.datetime.now():
              speech("Alarm Now")
              alarms.remove(alarm)
              break


def interprate(request):
    if "set alarm" in request:
        return setAlarm(request)
    else:
        return "Sorry could not understant your request for an alarm"

t = threading.Thread(name='alarm loop', target=alarmLoop)
t.start()
