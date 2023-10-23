import listener
from betterDateTime import *
import betterLogging as log
from gen_stream import *
import betterSmartAssist as BDT
import threading
from vars import api_key,Name

log.info('.env variables loaded')
threading.Thread(target=BDT.AlarmClass.AlarmSys).start()
log.info('Initilizing completion loop')
while True:
    log.info('Initilizing new listener loop')
    listener.start(Name, api_key)
    log.info('Listener loop closed')