import speech_recognition as sr
import time

r = sr.Recognizer()

with sr.Microphone() as source:
    print("You have 5 seconds to say something...")
    # read the audio data from the default microphone
    time.sleep(1)
    print(3)
    time.sleep(1)
    print(2)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print("Recording...")
    audio_data = r.record(source, duration=5)
    print("Recognizing...")
    # convert speech to text
    text = r.recognize_google(audio_data)
    print(text)
