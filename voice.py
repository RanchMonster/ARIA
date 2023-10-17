import azure.cognitiveservices.speech as speechsdk
from betterLogging import *
import betterLogging as log
import commands as command

info('Configuring Azure speech engine')
speech_config = speechsdk.SpeechConfig(subscription="29037678ff9841b9a75aa04cf6dd6d51", region="eastus")
speech_config.speech_synthesis_voice_name = "en-GB-AlfieNeural"
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
