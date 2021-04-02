import speech_recognition as sr

r = sr.Recognizer()

with sr.AudioFile("audios/woman1_wb.wav") as source:
    audio = r.record(source)

print(r.recognize_google(audio))

# with speech_recognition.Microphone() as source:
#     print("Speak some thing:...")
#     audio = r.listen(source)
#
#     try:
#         text = r.recognize_google(audio, language="en-EN")
#         print(f"You said: {text}")
#     except Exception as ex:
#         print(str(ex))
