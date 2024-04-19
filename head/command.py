import speech_recognition as sr
from head.speaking import speak

def take_command():
    s = sr.Recognizer()
    with sr.Microphone() as source:
        s.energy_threshold = 10000
        s.adjust_for_ambient_noise(source, 1.2)
        print("Listening...")
        s.pause_threshold = 1
        audio = s.listen(source)
    try:
        print('Recognizing...')
        query = s.recognize_google(audio)
    except Exception as e:
        print("Exception: your voice is not recognized")
        speak("your voice is not recognized...")
        return "None"
    return query