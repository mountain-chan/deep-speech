import json
from os.path import join, dirname
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

with open('audios/woman1_wb.wav', 'rb') as audio_file:
    text = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/wav',
        model='en-US_BroadbandModel')

print(text)
