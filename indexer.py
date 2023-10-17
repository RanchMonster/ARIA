import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{index}, {name}')

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak Anything!")
    audio = r.listen(source)

    r.energy_threshold = 300
    r.pause_threshold = 1

    try:
        text = r.recognize_google(audio)
        print("You said : {}".format(text))
    except:
        print("Sorry could not recognize what you said!")
