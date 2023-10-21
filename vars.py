from dotenv import load_dotenv
import betterLogging as log
import os
load_dotenv()
def env(s: str): return os.environ.get(s)
log.info('Loading .env variables')
api_key = env('api_key')
Name = env("name")
azure = env("azure")
gender= env("gender")
voice = env("voice")
