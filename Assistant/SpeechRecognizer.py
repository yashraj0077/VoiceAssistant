import speech_recognition as sr
import sys
import time
import os
sys.path.insert(0, 'SnowBoy')
import snowboydecoder


# This file is called for the google speech to text

def getVoice(prompt=True):
    print("getting voice...")
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("in microphone")
            r.adjust_for_ambient_noise(source, duration = 0.5)
            print("listening")

            os.system("aplay -q SnowBoy/resources/ding.wav")



            audio = r.listen(source)
        print("out of microphone")
        speech = r.recognize_google(audio)
        return speech.lower()
    except:
        return "Could not understand"
