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
        print(rate)
        print(frames)

    return buffer, rate


def transcribe(audio_file):
    buffer, rate = read_wav_file(audio_file)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    return model.stt(data16)


print(transcribe(audio_file_path))
