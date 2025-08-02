import pyaudio
import speech_recognition as sr
import webbrowser as wb
import requests
import asyncio
import edge_tts
import os
import pygame
from openai import OpenAI
import musiclib as music  # Make sure this exists

r = sr.Recognizer()
newsapi = "your-API KEY"  #REMEMBER ITS PAID FROM OPENAIAPIS

# Async speak using edge-tts + pygame
async def speak(text):
    output_file = "temp.mp3"
    communicate = edge_tts.Communicate(text=text, voice="en-US-AriaNeural")
    await communicate.save(output_file)

    # Play using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove(output_file)

# Run async speak from sync context
def speak_sync(text):
    asyncio.run(speak(text))

# Handle OpenAI command
def openaicommand(command):
    client = OpenAI(
        api_key="YOUR-API-KEY " ) # api of chatgpt is paid so you have to pay 5 dollars to access to api of openai

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Sage skilled in general tasks like Alexa and Google Cloud"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

# Process spoken commands
def processcommand(c):
    if "open google" in c.lower():
        wb.open("https://google.com")
    elif "open youtube" in c.lower():
        wb.open("https://youtube.com")
    elif "open facebook" in c.lower():
        wb.open("https://facebook.com")
    elif "open linked in" in c.lower():
        wb.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        try:
            song = c.lower().split(" ")[1]
            link = music.music[song]
            wb.open(link)
        except:
            speak_sync("Sorry, I could not find that song.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # limit to 5 headlines
                speak_sync(article['title'])
        else:
            speak_sync("Unable to fetch news right now.")
    else:
        result = openaicommand(c)
        speak_sync(result)

# Main program
if __name__ == "__main__":
    speak_sync("Initializing Sage...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            print(f"You said: {word}")

            if word.lower() == "hello":
                speak_sync("Yes, how can I help you?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = r.listen(source)
                command = r.recognize_google(audio)
                print(f"Command: {command}")
                processcommand(command)

        except sr.UnknownValueError:
            print("SAGE could not understand audio")
        except Exception as e:
            print(f"SAGE error: {e}")
