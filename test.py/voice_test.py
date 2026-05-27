import pyttsx3

engine = pyttsx3.init(driverName='sapi5')

engine.say("Voice is working")

engine.runAndWait()