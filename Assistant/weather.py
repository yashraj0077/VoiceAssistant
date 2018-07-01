import requests
import json


# this file is called by the main.py to call the api for the weather.
# It first splits the request and then checks for "in" which is an
# indecator that the user is specifying a place other than providence.
# Then I use the getWeather method to call OpenWeatherMap for the current
# temp., parse it into a sentance and then return it to the repl in main.py

apiKey = "40094d8bd12833f0984421a8dac46c2b"
def getWeather(location):
    location = ' '.join(location)
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" +location+ "&units=imperial&appid=" + apiKey)
    weatherData = json.loads(r.text)
    return str(weatherData["main"]["temp"]) + " degrees in " + location


def interpret(r):
    r = r.split(" ")
    if "in" in r:
        return getWeather(r[r.index("in") + 1:])
    else:
        return getWeather(["providence"])
