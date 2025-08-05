import pyaudio
import speech_recognition as sr
import webbrowser as wb
import requests
import asyncio
import edge_tts
import os
import platform
import pygame
import google.generativeai as genai
import musiclib as music  

r = sr.Recognizer()
newsapi = "c45efdc0577d466f8d90de0029c26127"


async def speak(text):
    output_file = "temp.mp3"
    communicate = edge_tts.Communicate(text=text, voice="en-US-AriaNeural")
    await communicate.save(output_file)

    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove(output_file)

def speak_sync(text):
    asyncio.run(speak(text))


def geminicommand(command):
    genai.configure(api_key="YOUR-API-KEY FROM GEMEINI")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(
        f"You are a virtual assistant named Sage skilled in general tasks like Alexa and Google Cloud. {command}"
    )
    return response.text


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
        result = geminicommand(c)
        speak_sync(result)


if platform.system() == "Emscripten":
    async def main():
        speak_sync("Initializing Sage...")
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening for wake word...")
                    audio = r.listen(source, timeout=2, phrase_time_limit=1)
                word = r.recognize_google(audio)
                print(f"You said: {word}")

                if word.lower() == "sage":
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
        await asyncio.sleep(1.0 / 60)  

    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        speak_sync("Initializing Sage...")
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening for wake word...")
                    audio = r.listen(source, timeout=2, phrase_time_limit=1)
                word = r.recognize_google(audio)
                print(f"You said: {word}")

                if word.lower() == "sage":
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