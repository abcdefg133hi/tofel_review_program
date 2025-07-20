import threading
import json
import time
import sounddevice as sd
import numpy as np
import wave
import pyttsx3
import os
import platform
import pyaudio
import random


# === Configuration ===
PREPARATION_TIME = 15  # seconds
SPEAKING_TIME = 45     # seconds
SAMPLE_RATE = 44100    # Hz
CHANNELS = 1           # Mono recording
PROBLEM_FILE = "./speaking/problems.json"
AUDIO_PATH = "./tmp/recording"
PREP_TIME = 15     # seconds for preparation
SPEAK_TIME = 45    # seconds for speaking
FS = 44100         # sample rate
RECORDING_FILENAME = "response.wav"
BEEP_DURATION = 0.2
BEEP_FREQ = 440    # A4 note
DELETE_AUDIO_PATH = True

suffix = ["Please prepare your answer after the beep.", "Please speak your answer after the beep."]

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def beep(freq=BEEP_FREQ, duration=BEEP_DURATION, fs=FS):
    t = np.linspace(0, duration, int(fs * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    sd.play(tone, samplerate=fs)
    sd.wait()

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def load_questions(filename):
    with open(filename, "r") as f:
        return json.load(f)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def countdown_old(seconds, message):
    print(f"\n{message} ({seconds} seconds)")
    for i in range(seconds, 0, -1):
        print(f"{i}...", end='', flush=True)
        time.sleep(1)
    print("\n")

def countdown(seconds, message, suffix = None):
    print(f"\n{message} ({seconds} seconds)")
    for i in range(seconds, 0, -1):
        print(f"\r{i}...", end='', flush=True)
        time.sleep(1)
    if suffix:
        print(f"\r{suffix}     \n")  # Overwrite the last line with "Go!"

def record_voice(duration, filename):
    print(f"🎙️  Recording... Speak now!")

    FORMAT = pyaudio.paInt16
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(SAMPLE_RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(frames))

    print(f"✅ Recording saved to {filename}")

def aplay_audio(filename):
    CHUNK = 1024
    wf = wave.open(filename, 'rb')
    audio = pyaudio.PyAudio()

    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    audio.terminate()

def play_audio(filename, volume_gain=3.0):  # volume_gain = 2.0 means 200% volume
    CHUNK = 1024
    wf = wave.open(filename, 'rb')
    audio = pyaudio.PyAudio()

    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

    sample_width = wf.getsampwidth()
    dtype = {1: np.int8, 2: np.int16, 4: np.int32}[sample_width]

    data = wf.readframes(CHUNK)
    while data:
        audio_array = np.frombuffer(data, dtype=dtype)
        # Amplify audio
        louder_array = np.clip(audio_array * volume_gain, np.iinfo(dtype).min, np.iinfo(dtype).max).astype(dtype)
        stream.write(louder_array.tobytes())
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    audio.terminate()





def main():
    questions = load_questions(PROBLEM_FILE)
    os.makedirs(AUDIO_PATH, exist_ok=True)
    random.shuffle(questions)
    idx = 1
    repeat_question = None
    while True:
        if repeat_question:
            question = repeat_question
        else:
            question = questions[idx-1]
        clear_screen()
        print(f"\n===== Question {idx} =====\n{question}")

        if not repeat_question:
            speak(question + " " + suffix[0])
            countdown(PREPARATION_TIME, "🕒 Preparation Time", "GO")

        speak(suffix[1])

        audio_filename = os.path.join(AUDIO_PATH, f"response_{idx}.wav")
        record_thread = threading.Thread(target=record_voice, args=(SPEAKING_TIME, audio_filename))
        record_thread.start()
        countdown(SPEAKING_TIME, "🕒 Speaking Time", "STOP")
        record_thread.join()
        #countdown(0, "🎤 Speaking Time Starts Now")
        #countdown(SPEAKING_TIME, "🕒 Speaking Time", "STOP")
        #record_voice(SPEAKING_TIME, audio_filename)

        a = input("Play your recording audio? [y/n]")
        if a in ["y", "Y", "Yes", "yes"]:
            play_audio(audio_filename)


        a = input("Do you want to pratice the same questions again? [y/n]")

        if a in ["y", "Y", "Yes", "yes"]:
            repeat_question = question
            continue

        repeat_question = None

        a = input("Do you want to keep continuing? [y/n]")

        if a not in ["y", "Y", "Yes", "yes"]:
            break

        if DELETE_AUDIO_PATH:
            os.remove(audio_filename)

        idx += 1

    if DELETE_AUDIO_PATH:
        os.system(f"rm -rf {AUDIO_PATH}")

    print("🎉 All questions completed!")

if __name__ == "__main__":
    main()
