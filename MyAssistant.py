import random
import pywhatkit as kit
import pyautogui as pg
from mail.sendMail import send_email
from GPTAssistant.assist_gpt import GPT
from greetings.greeting import greetings
from head.speaking import speak
from head.command import take_command
from date_and_time.date_time import current_time
from IPL.ipl_matches import PlayingIPL
from ImageGeneration.imageGenerator import GenerateImage
from GPTAssistant.self_correction import SelfCorrection
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy


asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

if __name__=="__main__":
    speak(random.choice(greetings))
    speak("Now the time is " + current_time())
    
    while True:
        query = take_command().lower()
        print(query)
        if "jokes" in query or "joke" in query:
            content = GPT(query)
            speak(content)
        elif "make a conversation" in query:
            speak("what type of conversation do you want?")
            q = take_command().lower()
            res = GPT(q)
            speak(res)
        elif "play ipl match" in query:
            speak("here you go")
            PlayingIPL()
        elif "play yotube" in query:
            name = query.replace("play","")
            speak("Enjoy your video boss..")
            kit.playonyt(name)
        elif "open brave" in query:
            speak("here you go")
            pg.press('win')
            pg.typewrite('brave')
            pg.press('enter')
        elif "close" in query or "closing" in query:
            pg.hotkey("ctrl","w")
        elif "send an email" in query or "compose an email" in query:
            speak("provide an email to whom to send")
            email = input("email address: ")
            speak("provide a subject")
            subject = take_command().lower()
            print(subject)
            speak("what should send to {email}")
            content = input("write a content...")
            print(content)
            message = GPT(content)
            send_email(email, subject, message)
            speak("email send successfully..")
        elif "write a python code" in query:
            correction = SelfCorrection()
            correction.main(query)
        elif "generate image" in query or "create image" in query:
            GenerateImage(query)
        elif "goodbye" in query or "i see you later" in query:
            res = GPT(query)
            speak(res)
            break
    

