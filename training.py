import random
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

#Load Training Data

lemmatizer=WordNetLemmatizer()
intents=json.loads(open('topics.json').read())

words=[]
classes=[]
documents=[]
ignore_letters=['?','!','.',',']
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list=nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#print(documents)

# Training Data

words=[lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words=sorted(set(words))
#print(words)

classes=sorted(set(classes))

pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

training=[]
ouput_empty=[0]*len(classes)

for document in documents:
    bag=[]
    word_patterns=document[0]
    word_patterns=[lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
        
    output_row=list(ouput_empty)
    output_row[classes.index(document[1])]=1
    training.append([bag, output_row])
    
random.shuffle(training)
training=np.array(training,dtype='object')

train_x=list(training[:,0])
train_y=list(training[:,1])

# Neural Network

model=Sequential()
model.add(Dense(128,input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd=SGD(learning_rate=0.01, weight_decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist=model.fit(np.array(train_x), np.array(train_y),epochs=200, batch_size=5, verbose=1)
plt.figure(figsize=(12, 6))

# Plot Loss
plt.subplot(1, 2, 1)
plt.plot(hist.history['loss'])
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')

# Plot Accuracy
plt.subplot(1, 2, 2)
plt.plot(hist.history['accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')

plt.tight_layout()
plt.show()

model.save('chatbottopicsmodel.keras',hist)
print("Done")