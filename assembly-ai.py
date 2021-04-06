import time

import requests

API_TOKEN = "6033b6b044e8444ab0be8d3c96ff46e2"

filename = "audios/woman1_wb.wav"

st = time.time()


# upload

def read_file(_filename, chunk_size=5242880):
    with open(_filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


headers = {'authorization': "6033b6b044e8444ab0be8d3c96ff46e2"}
response = requests.post('https://api.assemblyai.com/v2/upload',
                         headers=headers,
                         data=read_file(filename))

print(response.json()['upload_url'])

# transcript
endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
    "audio_url": response.json()['upload_url']
}

headers = {
    "authorization": "6033b6b044e8444ab0be8d3c96ff46e2",
    "content-type": "application/json"
}

response = requests.post(endpoint, json=json, headers=headers)

print(response.json())

e = time.time()

print(e - st)

print(response.json()["id"])

time.sleep(20)

# Get result

endpoint = f"https://api.assemblyai.com/v2/transcript/{str(response.json()['id'])}"

headers = {
    "authorization": API_TOKEN,
}

response = requests.get(endpoint, headers=headers)

print(response.json())


