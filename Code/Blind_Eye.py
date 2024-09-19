import openai
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import winsound
import os
import numpy as np

# OpenAI API Key
openai.api_key = "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"

# Speech Recognition
engine = pyttsx3.init()


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Could not understand audio")


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=4000,
        n=1,
        stop=None,
    )
    return response["choices"][0]["text"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        print("Hello, I'm Blind Eye. What would you like to know? say Blind to start listening.")

        # wait for user to say "Blind Eye"
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription == "blind":
                print("Listening...")
                # play sound to indicate listening
                winsound.Beep(440, 500)

                # record audio
                filename = "input.wav"
                print("Recording...")
                                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())

                # transcribe audio to text
                text = transcribe_audio_to_text(filename)
                if text:
                    print("You said: " + text)

                    # generate response using OpenAI
                    print("Generating response...")
                    response = generate_response(text)
                    print("Response: " + response)
                    # record audio with gtts for video
                    tts = gTTS(text=response, lang="en")
                    tts.save("sample.wav")
                    # read response using pyttsx3
                    speak_text(response)
        except Exception as e:
            print("An error occurred: {}".format(e))


if __name__ == "__main__":
    main()
