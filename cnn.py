# -*- coding: utf-8 -*-
#Importing the libraries

from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

#Initialising the CNN

classifier = Sequential()

#Convolution

classifier.add(Convolution2D(32, 3, 3, input_shape =(64,64,3), activation='relu'))

#Pooling

classifier.add(MaxPooling2D(pool_size = (2,2)))

#Adding a second convolutional layer
classifier.add(Convolution2D(32, 3, 3, activation='relu'))
classifier.add(MaxPooling2D(pool_size = (2,2)))

#Flattening

classifier.add(Flatten())

#Full connection

classifier.add(Dense(units=128, activation = 'relu'))
classifier.add(Dense(units=1, activation = 'sigmoid'))

#Compiling the CNN

classifier.compile(optimizer='adam', loss= 'binary_crossentropy', metrics = ['accuracy'])

import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator

#Preparing image augmentation
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

#Preprocessing

training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

# Fitting the CNN
classifier.fit_generator(training_set,
                         steps_per_epoch=len(training_set),
                         epochs=25,
                         validation_data=test_set,
                         validation_steps=len(test_set))

#Making Predictions

import numpy as np
from keras.preprocessing import image

test_image = image.load_img('dataset/single_prediction/cat_or_dog_1.jpg',target_size=(64,64))
test_image=image.img_to_array(test_image)
test_image=np.expand_dims(test_image,axis=0) #for extra dim while predicting
result=classifier.predict(test_image)

training_set.class_indices

if result[0][0] ==1:
  prediction = 'dog'
else:
  prediction = 'cat'
