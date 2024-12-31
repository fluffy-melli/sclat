# This STT feature is currently unfinished and not available for normal use, so please wait for the next release.
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from setting import setting as user_setting
import speech_recognition as sr

if user_setting.stt:
    recognizer_instance = sr.Recognizer()

def run(vid):
    global vid_run
    vid_run = True

    while vid_run:
        with sr.Microphone() as source:
            recognizer_instance.adjust_for_ambient_noise(source)
            try:
                audio_data = recognizer_instance.listen(source, timeout=1, phrase_time_limit=3)

                result = recognizer_instance.recognize_whisper(
                    audio_data, model="tiny", language="ko"
                )
                # TODO: Add a command that can be executed when the user speaks
                print(result)

            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
            except Exception as e:
                print(e)
                pass

def stop():
    global vid_run
    vid_run = False