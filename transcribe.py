import openai
import betterLogging as log
from gen_stream import generate

def transcribe_audio(api_key, gen_out: bool = True):
    log.debug('Initilizing OpenAI')
    openai.api_key = api_key
    log.info(f'OpenAI loaded with key "{api_key}"')
    log.info('Processing audio data')
    transcribed_text = openai.Audio.transcribe('whisper-1', open('./audio/latest.wav', 'rb'))['text'].replace('Arya', "Aria")
    print(transcribed_text)
    try: return generate(transcribed_text, api_key) if gen_out else transcribed_text
    except Exception as e: log.error(f'Transcription failed:\n{e}')