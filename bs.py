import sounddevice as sd

print(sd.query_devices())
device_id = sd.query_devices(kind='output')['name'].tolist()[0] 
