import speech_recognition as sr
import pyttsx3
import json
import random
from keras.models import load_model
import matplotlib.pyplot as plt
from fluency import get_sentences

r = sr.Recognizer()

intents = json.loads(open('topics.json').read())
model = load_model('chatbottopicsmodel.keras')

accuracy_scores = []
answers=[]
questions_numbers=[]
skills=[]

with open('sharing.txt', 'r', encoding='utf-8') as file:
    for line in file:
        skills.append(line.strip())

def skill_numbers(skills,intents):
    list_of_intents=intents['intents']
    skill_set=[]
    fields=[]
    for i in range(0,31):
        fields.append(list_of_intents[i]['tag'])
    print(fields)
    for i in range(len(skills)):
        for j in range(len(fields)):
            if skills[i] in fields[j]:
                skill_set.append(j)
    return skill_set
skill_set_numbers=skill_numbers(skills,intents)
skill_set_numbers=set(skill_set_numbers)
skill_set_numbers=list(sorted(skill_set_numbers))
'''def get_question(questions):
    x=random.randint(0,30)
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
                c+= 1
            elif c == len(skill_set_numbers)+1:
                string = "Thank you"
                engine.say(string)
                print(string)
                break
            else:
                index = c-1
                list_of_intents = intents['intents']
                string = list_of_intents[index]['patterns']
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