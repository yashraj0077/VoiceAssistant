import weather
import podcast
import spot
import icloud
import sys
import SpeechRecognizer
import pyttsx
sys.path.insert(0, 'SnowBoy')
import snowboydecoder


# This is the main method that uses Snowboy to detect the hot word, in this case
# being "pi". On startup listen_loop is called where it will stay checking
# for the hot word every 0.03 seconds. When it gets the word, it starts the startRequest
# method, which sends the voice recording to SpeechRecognizer for the text
# interpretation. Main then parses the request and decides which file to send the
# request to. After a request is performed, Main will use speech() to have
# the pi say the desired response. Once everything is done, the program goes
# back to listen_loop.


def listen_loop():
    detector = snowboydecoder.HotwordDetector("Pi.pmdl", sensitivity=0.5)
    print("Waiting for 'Pi!'")
    detector.start(detected_callback=lambda: startRequest(detector),
               sleep_time=0.03)


def speech(script):
    engine = pyttsx.init()
    engine.setProperty('rate', engine.getProperty('rate')-20)
    engine.say(script)
    engine.runAndWait()


def startRequest(detector):
    detector.terminate()
    spotPlay = spot.playing()
    spotChanged = False
    podcastPlay = podcast.playing()
    podcastChanged = False
    if spotPlay is True:
        spot.pause()
        spotChanged = True
    if podcastPlay is True:
        podcast.pause()
        podcastChanged = True
    request = ""
    try:
        request = SpeechRecognizer.getVoice()
    except:
        speech("Sorry something went wrong.")

    print(request)
    response = []
    if "spotify" in request:
        spot.interpret(request)
    elif "podcast" in request:
        response.append(podcast.interpret(request))
    elif "weather" in request:
        response.append(weather.interpret(request))
    elif "icloud" in request:
        response.append(icloud.interpret(request))
    else:
        response.append("Sorry, try using spotify, podcast, weather, or icloud commands")
    newSpotPlaying = spot.playing()
    newPodcastPlaying = podcast.playing()
    if spotChanged is False and newSpotPlaying is True:
        podcast.quit()
    elif spotChanged and "pause" not in request:
        spot.play()
    elif podcastChanged and "pause" not in request:
        podcast.play()

    for quote in response:
        speech(quote)
    listen_loop()

if __name__ == "__main__":
    listen_loop()
