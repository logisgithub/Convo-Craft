import speech_recognition as sr
import pyttsx3
import json
import random
from keras.models import load_model
import matplotlib.pyplot as plt
from fluency import get_sentences

r = sr.Recognizer()

intents = json.loads(open('intents.json').read())
model = load_model('chatbotmodel.keras')

accuracy_scores = []
answers=[]

'''def get_question(questions):
    x=random.randint(0,28)
    if x not in questions:
        return x
    get_question(questions)'''
    
def analyze_answer(user_answer, x, intents_json):
    count = 0
    list_of_intents = intents_json['intents']
    answer_list = list_of_intents[x]['responses']
    for i in range(len(answer_list)):
        if answer_list[i] in user_answer:
            count += 1
    if count > 0:
        accuracy_scores.append(1)
    else:
        accuracy_scores.append(0.25)

question_numbers=random.sample(range(0,28),10)
c = 0

while True:
    try:
        with sr.Microphone() as source:
            engine = pyttsx3.init()
            if c == 0:
                string = "Introduce Yourself"
                engine.say(string)
                print(string)
                engine.runAndWait()
                c += 1
            elif c == 11:
                string = "Thank you"
                engine.say(string)
                print(string)
                break
            else:
                index = question_numbers[c-1]
                list_of_intents = intents['intents']
                string = random.choice(list_of_intents[index]['patterns'])
                engine.say(string)
                print(string)
                engine.runAndWait()
                c += 1
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print(text)
            answers.append(text)
            if c>1: 
                analyze_answer(text, index, intents)

            # Plot the accuracy score after each interaction

    except sr.UnknownValueError:
        print("Speech not recognized")
        continue
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        break
    except KeyboardInterrupt:
        print("Program interrupted by the user")
        break

plt.plot(accuracy_scores)
plt.title('Accuracy Score Over Interactions')
plt.xlabel('Interaction')
plt.ylabel('Accuracy Score')
plt.show()

words=""
for i in range(len(answers)):
    words+=answers[i]
get_sentences(words)