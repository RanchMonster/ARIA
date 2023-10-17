import listener
from betterDateTime import *
import os
from dotenv import load_dotenv
import betterLogging as log
from gen_stream import *
import betterSmartAssist as BDT
import threading
load_dotenv()
def env(s: str): return os.environ.get(s)
log.info('Loading .env variables')
api_key = env('api_key')
log.info('.env variables loaded')
threading.Thread(target=BDT.AlarmClass.AlarmSys).start()
log.info('Initilizing completion loop')
while True:
    log.info('Initilizing new listener loop')
    listener.start('Jarvis', api_key)
    log.info('Listener loop closed')