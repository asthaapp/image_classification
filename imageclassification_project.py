# -*- coding: utf-8 -*-
"""imageclassification_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mHM6dCrum7kDOmbiqTDFaFq6yE4h7EWy
"""

from keras.datasets import cifar10
import matplotlib.pyplot as plt

(train_X,train_Y),(test_X,test_Y)=cifar10.load_data()

n=6
plt.figure(figsize=(20,10))
for i in range(n):
  plt.subplot(330+1+i)
  plt.imshow(train_X[i])
plt.show()

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from tensorflow.keras.constraints import max_norm
from keras.optimizers import SGD
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from tensorflow.keras.utils import to_categorical

train_x=train_X.astype('float32')
test_X=test_X.astype('float32')

train_X=train_X/255.0
test_X=test_X/255.0

train_Y=to_categorical(train_Y)
test_Y=to_categorical(test_Y)

num_classes=test_Y.shape[1]

model=Sequential()
model.add(Conv2D(32,(3,3),input_shape=(32,32,3),
    padding='same',activation='relu',
    kernel_constraint=max_norm(3)))
model.add(Dropout(0.2))
model.add(Conv2D(32,(3,3),activation='relu',padding='same',kernel_constraint=max_norm(3)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(512,activation='relu',kernel_constraint=max_norm(3)))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

from keras.optimizers.schedules import ExponentialDecay


initial_learning_rate = 0.01
decay_rate = 0.01 / 25
lr_schedule = ExponentialDecay(
    initial_learning_rate,
    decay_steps=100000,
    decay_rate=decay_rate,
    staircase=True
)
sgd = SGD(learning_rate=lr_schedule, momentum=0.9, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.summary()

model.fit(train_X,train_Y,
    validation_data=(test_X,test_Y),
    epochs=10,batch_size=32)

_,acc=model.evaluate(test_X,test_Y)
print(acc*100)

model.save("model1_cifar_10epoch.h5")

results={
   0:'aeroplane',
   1:'automobile',
   2:'bird',
   3:'cat',
   4:'deer',
   5:'dog',
   6:'frog',
   7:'horse',
   8:'ship',
   9:'truck'
}

from PIL import Image
import numpy as np
im=Image.open("horse.jpeg")
# the input image is required to be in the shape of dataset, i.e (32,32,3)

im=im.resize((32,32))
im=np.expand_dims(im,axis=0)
im=np.array(im)
pred=model.predict_classes([im])[0]
print(pred,results[pred])

from PIL import Image
import numpy as np

try:
    im = Image.open("horse.jpeg")  # Or provide the full path
    # the input image is required to be in the shape of dataset, i.e (32,32,3)
    im = im.resize((32, 32))
    im = np.expand_dims(im, axis=0)
    im = np.array(im)
    pred = model.predict_classes([im])[0]
    print(pred, results[pred])

except FileNotFoundError:
    print("Error: The image file 'horse.jpeg' was not found.")

import numpy as np
from keras.models import load_model
from PIL import Image
import matplotlib.pyplot as plt
from google.colab import files

# Load the trained model
model = load_model('model1_cifar_10epoch.h5')

# CIFAR-10 classes
classes = {
    0: 'aeroplane',
    1: 'automobile',
    2: 'bird',
    3: 'cat',
    4: 'deer',
    5: 'dog',
    6: 'frog',
    7: 'horse',
    8: 'ship',
    9: 'truck'
}

def classify(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        image = image.resize((32, 32))
        image = np.expand_dims(image, axis=0)
        image = np.array(image) / 255.0  # Normalize to [0, 1]

        # Get prediction probabilities
        predictions = model.predict([image])[0]
        pred = np.argmax(predictions)  # Get class with highest probability
        sign = classes[pred]
        confidence = predictions[pred]  # Get confidence score

        return sign, confidence
    except Exception as e:
        return None, str(e)

def upload_and_classify():
    uploaded = files.upload()
    for fn in uploaded.keys():
        print(f'User uploaded file "{fn}"')
        sign, confidence = classify(fn)
        if sign:
            print(f"Prediction: {sign} ({confidence:.2f})")
            image = Image.open(fn)
            plt.imshow(image)
            plt.title(f"{sign} ({confidence:.2f})")
            plt.axis('off')
            plt.show()
        else:
            print(f"Error: {confidence}")

# Run the upload and classify function
upload_and_classify()