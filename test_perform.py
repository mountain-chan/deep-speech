import timeit

setup = """
# import wave
# 
# import numpy as np
# from deepspeech import Model
# 
# model_file_path = "models/deepspeech-0.9.3-models.pbmm"
# lm_file_path = "models/deepspeech-0.9.3-models.scorer"
# audio_file_path = "audios/woman1_wb.wav"
# beam_width = 500
# lm_alpha = 0.93
# lm_beta = 1.18
# 
# model = Model(model_file_path)
# model.enableExternalScorer(lm_file_path)
# model.setScorerAlphaBeta(lm_alpha, lm_beta)
# model.setBeamWidth(beam_width)
# 
# 
# def read_wav_file(filename):
#     with wave.open(filename) as w:
#         rate = w.getframerate()
#         frames = w.getnframes()
#         buffer = w.readframes(frames)
# 
#     return buffer, rate
# 
# 
# def transcribe(audio_file):
#     buffer, rate = read_wav_file(audio_file)
#     data16 = np.frombuffer(buffer, dtype=np.int16)
#     return model.stt(data16)



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

with sr.AudioFile("audios/woman1_wb.wav") as source:
    audio = r.record(source)

"""

setup_aws = """
# AWS set up
import time

import boto3
import pprint

transcribe = boto3.client('transcribe')
transcribe.delete_transcription_job(
    TranscriptionJobName='temp1'
)
job_name = "temp1"  # non-existent job name
job_uri = "s3://survey-transcribe/woman1_wb.wav"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    LanguageCode='en-US'
)
"""

ex1 = """ 
print(transcribe(audio_file_path))
"""

ex_ibm = """ 
with open('audios/woman1_wb.wav', 'rb') as audio_file:
    text = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/wav',
        model='en-US_BroadbandModel')
    
    print(text)
"""

ex_google = """ 
print(r.recognize_google(audio))
"""

ex_aws = """
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(2)
"""

# long = timeit.timeit(ex1, setup=setup, number=1)
# print("Spending Time when using Model: ", long)

long = timeit.timeit(ex_ibm, setup=setup, number=1)
print("Spending Time when using IBM API: ", long)

long = timeit.timeit(ex_google, setup=setup, number=1)
print("Spending Time when using Google API: ", long)

long = timeit.timeit(ex_aws, setup=setup_aws, number=1)
print("Spending Time when using AWS API: ", long)
