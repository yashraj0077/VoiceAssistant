import requests
from bs4 import BeautifulSoup
import subprocess



# This is the file that takes care of playing podcasts on my pi.
# As of now I only have it for The Daily, but an be used for any RSS audio feed.
# I use a get request to grab the audio from the feed then save it to an mp3 file,
# create a subprocess and have that thread play the podcast.

running = False
daily = ""

def start_daily():
    feeduUrl = "https://rss.art19.com/the-daily"
    feed = requests.get(feeduUrl).content
    parser = BeautifulSoup(feed,'xml')
    episodes = parser.findAll("item")
    recentPodcast = episodes[0]
    url = str(recentPodcast.enclosure['url'])
    response = requests.get(url)
    data = response.content
    mp3Name = "daily.mp3"
    song = open(mp3Name, "wb")
    song.write(data)
    song.close()
    global daily
    daily = subprocess.Popen(["mpg321", "-R", 'anyword'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    daily.stdin.write("L daily.mp3\n")
    global running
    running = True

def play():
    if running is False:
        if daily is not "":
            daily.stdin.write("P\n")
            global running
            running = True

def pause():
    if running is True:
        if daily is not "":
            daily.stdin.write("P\n")
            global running
            running = False


def quit():
    global daily
    if daily is not "":
        global daily
        daily.stdin.write("Q\n")
        global running
        running = False
        global daily
        daily = ""


def interpret(r):
    if "daily" in r:
        start_daily()
    elif daily != "":
        if "play" in r:
            play()
        elif "pause" in r or "stop" in r:
            pause()
        elif "quit" in r:
            quit()
        else:
            return "Sorry, I could not understand your request."
    else:
        return "Sorry, I could not understand your request. You do not have a podcast running."


def playing():
    global running
    return running
