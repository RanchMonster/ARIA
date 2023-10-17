# Advanced real-time intelligent assistant
import openai
from betterLogging import *
from content_formatter import *
from transcribe import transcribe_audio
from gen_stream import *
import os
import speech_recognition as sr

def start(trigger: str, api_key: str, messages = None):
    debug('Initilizing OpenAI')
    openai.api_key = api_key
    info(f'OpenAI loaded with key "{api_key}"')

    output_dir = './audio/'
    if not os.path.exists(output_dir):
        info('Creating audio output directory')
        os.makedirs(output_dir)
    r = sr.Recognizer()
    trigger_detected = False
    def transcribe(gen_out: bool = True):
        nonlocal trigger_detected, messages
        if trigger_detected or not gen_out:
            info('Generating transcript')
            with open('./audio/latest.wav', 'wb') as f: f.write(audio_data)
            trigger_detected = False
            output = transcribe_audio(api_key, gen_out)
        else: output = None
        try: os.remove('./audio/latest.wav')
        except: pass
        return output
    debug('Initalizing microphone')
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        info('Starting new listener cycle')
        while True:
            audio = r.listen(source)
            audio_data = audio.get_wav_data()
            try:
                if messages: return transcribe()
                if not trigger_detected:
                    recognized_text = r.recognize_google(audio)
                    if trigger in recognized_text:
                        trigger_detected = True
                        info('Trigger detected')
                        if trigger == recognized_text: continue
                        debug(recognized_text)
                        return generate(format(trigger, transcribe(False)), api_key)
                else:
                    info('Sending second audio part')
                    return transcribe()
            except sr.UnknownValueError:
                debug('No text could be transcribed (Python transcription)')
                return None
            except sr.RequestError as e:
                warn(f'Could not request results; {e}')
                return None
            except Exception as e:
                error(f'An error occured: {e}')
                return None
