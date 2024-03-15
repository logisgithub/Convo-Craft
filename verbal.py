import speech_recognition as sr
import pyttsx3
import time
import matplotlib.pyplot as plt
import numpy as np
import keyboard
from fluency import get_sentences

r = sr.Recognizer()

engine = pyttsx3.init()

target_duration = 60

start_time = time.time()

audio_samples = []

c=0

def check_space_pressed():
    return keyboard.is_pressed('space')

while True:
    try:
        if c==0:
            with sr.Microphone() as source:
                string = "Explain about Your College Life for about 2 minutes. Press the space bar to stop recording."
                engine.say(string)
                print(string)
                engine.runAndWait()

                audio = r.listen(source, timeout=target_duration - (time.time() - start_time), phrase_time_limit=10)

                if check_space_pressed():
                    break

                text = r.recognize_google(audio)
                audio_samples.extend(audio.get_raw_data())
                print(text)
                get_sentences(text)
                c+=1
        else:
            string="Thank you!"
            engine.say(string)
            print(string)
            break

    except sr.UnknownValueError:
        print("Speech not recognized")
        continue
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        break

    except KeyboardInterrupt:
        print("Program interrupted by the user")
        break

audio_samples_np = np.array(audio_samples)

plt.figure(figsize=(10, 4))
plt.specgram(audio_samples_np, Fs=2)
plt.title('Spectrogram of Recorded Speech')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.show()
quit()