# FILENAME: ibmwatsontest.py
# DESCRIPTION: A test using the IBM Watson TTS Python library

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator

authenticator = BasicAuthenticator("rysmith2113@gmail.com", "mast3rPr0gr@mm3r")

tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url("https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/455e458b-b19c-459f-9723-9b6652c02756")

with open("hello.wav", "wb") as audio_file:
    audio_file.write(tts.synthesize("Hello World", voice="en-US_AllisonVoice", accept="audio/wav").get_result().content)
