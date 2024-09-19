import os
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
from google.cloud import speech

# Google Cloud Speech-to-Text authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "blinde-eye-d6a430d20681.json"
client = speech.SpeechClient()

# Speech synthesis engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    with open(filename, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    if len(response.results) > 0:
        return response.results[0].alternatives[0].transcript
    else:
        return "Could not transcribe audio"

def generate_response(prompt):
    # Your OpenAI response generation code here
    pass

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Hello, I'm Blind Eye. What would you like to know?")
        # wait for user to say "Blind Eye"
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == "blind":
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
                    tts.save("sample.mp3")
                    # read response using pyttsx3
                    speak_text(response)
        except Exception as e:
            print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()
