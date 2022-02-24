import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './google_cloud_key.json'

# import autosub


# import os
#
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './google_cloud_key.json'
#
# import librosa
# import soundfile
#
# expected_sr = 16000
#
# data, sr = librosa.load('music/Fish.ogg', expected_sr)
# assert sr == expected_sr
#
# # data = data[sr * 5:sr * 10]
#
# filename = 'music/_recognition.wav'
# soundfile.write(filename, data, sr)
#
# from google.cloud import speech_v1p1beta1 as speech
#
# client = speech.SpeechClient()
#
# with open(filename, 'rb') as audio_file:
#     content = audio_file.read()
# # content = data
#
# # Max 60 seconds
# audio = speech.RecognitionAudio(content=content)
#
# config = speech.RecognitionConfig(
#     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz=sr,
#     language_code='en-US',
# )
#
# operation = client.long_running_recognize(config=config, audio=audio)
#
# print('Waiting for operation to complete...')
# response = operation.result(timeout=90)
#
# print(response.results)
#
# for result in response.results:
#     print(result)  ##
#
#     # The first alternative is the most likely one for this portion.
#     print(u"Transcript: {}".format(result.alternatives[0].transcript))
#     print("Confidence: {}".format(result.alternatives[0].confidence))
