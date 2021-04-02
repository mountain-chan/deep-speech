import timeit

setup = """
import wave

import numpy as np
from deepspeech import Model

model_file_path = "models/deepspeech-0.9.3-models.pbmm"
lm_file_path = "models/deepspeech-0.9.3-models.scorer"
audio_file_path = "audios/OSR_us_000_0010_8k.wav"
beam_width = 500
lm_alpha = 0.93
lm_beta = 1.18

model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)
model.setScorerAlphaBeta(lm_alpha, lm_beta)
model.setBeamWidth(beam_width)


def read_wav_file(filename):
    with wave.open(filename) as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)

    return buffer, rate


def transcribe(audio_file):
    buffer, rate = read_wav_file(audio_file)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    return model.stt(data16)



# IBM set up
import json
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = "fOe0DnaM5jbMy7mplz5mP5WX_IxbiKZoXyROm-qAlomc"
apikeyT = 'y743rTxYWLSf1J6MTIRPWDlvJi_YAHUzgGsAxUuYeos4'
url = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/420bc585-744a-44af-be17-e6d2e4c0e59c"
urlT = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/4211a4dd-2d28-4975-9168-89130243f4bc'

authenticator = IAMAuthenticator(apikey)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(url)


class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))


myRecognizeCallback = MyRecognizeCallback()


# Google API set up
import speech_recognition as sr

r = sr.Recognizer()

with sr.AudioFile("audios/OSR_us_000_0010_8k.wav") as source:
    audio = r.record(source)

"""

ex1 = """ 
print(transcribe(audio_file_path))
"""

ex2 = """ 
with open('audios/OSR_us_000_0010_8k.wav', 'rb') as audio_file:
    audio_source = AudioSource(audio_file)
    speech_to_text.recognize_using_websocket(
        audio=audio_source,
        content_type='audio/wav',
        recognize_callback=myRecognizeCallback,
        model='en-US_BroadbandModel',
        timestamps=True,
        max_alternatives=3)
"""

ex3 = """ 
print(r.recognize_google(audio))
"""

long = timeit.timeit(ex1, setup=setup, number=1)
print("Time spent when using Model: ", long)

long = timeit.timeit(ex2, setup=setup, number=1)
print("Time spent when using IBM API: ", long)

long = timeit.timeit(ex3, setup=setup, number=1)
print("Time spent when using Google API: ", long)
