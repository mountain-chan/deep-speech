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
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
pprint.pprint(status)
