import azure.cognitiveservices.speech as speechsdk
from betterLogging import *
import betterLogging as log
import commands as command
from vars import gender,voice,azure
if azure==None:raise("please put in azure subscription")
info('Configuring Azure speech engine')
speech_config = speechsdk.SpeechConfig(subscription=azure, region="eastus")
if gender and voice=="male": speech_config.speech_synthesis_voice_name = "en-GB-AlfieNeural"
elif gender and voice=="female":speech_config.speech_synthesis_voice_name = "en-US-JaneNeural"
elif gender!=True and voice!=None:speech_config.speech_synthesis_voice_name = voice
else:speech_config.speech_synthesis_voice_name = "en-US-JaneNeural";log.error("no voice was set default voice is being used")
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
info('Azure speech engine configured')



#audio_config = speechsdk.AudioConfig(use_default_microphone=False,device_name="DELL S2522HG (NVIDIA High Definition Audio)")




#speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def speak(text: str):
    info(f'Generating speech from text:\n{text}')
    text =command.execute_encoded_message(text)
    if text==None:
        exit()
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        if cancellation_details.reason == speechsdk.CancellationReason.Error: raise Exception(f"Speech synthesis canceled: {cancellation_details.reason}\nError details: {cancellation_details.error_details}")
        raise Exception(f"Speech synthesis canceled: {cancellation_details.reason}")
    return text
