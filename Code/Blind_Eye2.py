import openai
import pyttsx3
import speech_recognition as sr
from gtts import gTTS

# OpenAI API Key
openai.api_key = "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"

# Speech Recognition
recognizer = sr.Recognizer()

# Text-to-Speech
engine = pyttsx3.init()


def transcribe_audio_to_text(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Error occurred while transcribing audio")


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=4000,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        print("Hello, I'm Blind Eye. What would you like to know?")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == "blind":
                print("Recording...")
                speak_text("Recording")
                audio_file = "input.wav"
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source)

                with open(audio_file, "wb") as f:
                    f.write(audio.get_wav_data())

                # Transcribe audio to text
                text = transcribe_audio_to_text(audio_file)
                if text:
                    print("You said:", text)

                    # Generate response using OpenAI
                    print("Generating response...")
                    response = generate_response(text)
                    print("Response:", response)

                    # Save response as audio using gTTS
                    tts = gTTS(text=response, lang="en")
                    tts.save("sample.mp3")

                    # Read response aloud
                    speak_text(response)

        except sr.UnknownValueError:
            print("Sorry, I could not understand you.")
        except sr.RequestError:
            print("Sorry, an error occurred during speech recognition.")


if __name__ == "__main__":
    main()
