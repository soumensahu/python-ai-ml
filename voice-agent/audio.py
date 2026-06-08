import sounddevice as sd
import speech_recognition as sr


SAMPLE_RATE = 16000
DURATION = 5

def stt():
    recognizer = sr.Recognizer()
    print("Speak now...")

    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    print("Processing...")

    audio_data = sr.AudioData(
        recording.tobytes(),
        SAMPLE_RATE,
        2
    )

    text = recognizer.recognize_google(audio_data)

    print("You said:", text)
    return text