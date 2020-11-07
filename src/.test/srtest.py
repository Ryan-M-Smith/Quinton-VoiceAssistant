# FILENAME: srtest.py
# DESCRIPTION: A test using the SpeechRecognition Python library with the Houndify API

import speech_recognition as sr, sys

def main():
    CLIENT_ID = "OS1PN9QoHiKYs7ksCLLIGw=="
    CLIENT_KEY = "qHZ0xLnM1uaGB_yA5KY-SWKrYyqTXplWbRzQDzIsv7DpUbCJSXXCQlENP9ZUoqQtXBe8OO0C4DasfKJdIMXkCg==q"
    
    r = sr.Recognizer()

    for i, hwname in enumerate(sr.Microphone.list_microphone_names()):
        if ("USB" in hwname) or ("usb" in hwname):
            mic = sr.Microphone(device_index=i)

    with mic as source:
        r.adjust_for_ambient_noise(source)
        #print("\n\n--- Listening for speech ---")
        audio = r.listen(source, timeout=4, phrase_time_limit=4)
    
    try:
        print(r.recognize_houndify(audio, CLIENT_ID, CLIENT_KEY))
    except sr.UnknownValueError:
        print("Could not understand.")
    except sr.RequestError as e:
        print(f"Houndify error; {e}")

if (__name__ == "__main__"):
    sys.exit(main())
