import pandas as pd
import tensorflow as tf
import numpy as np
import warnings
import os
from tensorflow.keras.utils import load_img
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense

warnings.filterwarnings('ignore')

create_model = False
learning_sets_path = "data/learning_sets"
save_model_path = "data/models/true_mine_recognizer2.h5"
load_model_path = "data/models/true_mine_recognizer2.h5"
image_size = 128


class NeuralNetwork():
    def __init__(self):
        if create_model:
            input_path = []
            label = []

            for class_name in os.listdir(learning_sets_path):
                for path in os.listdir(learning_sets_path + "/" + class_name):
                    if class_name == 'mine':
                        label.append(0)
                    else:
                        label.append(1)
                    input_path.append(os.path.join(learning_sets_path, class_name, path))
            print(input_path[0], label[0])
            df = pd.DataFrame()
            df['images'] = input_path
            df['label'] = label
            df = df.sample(frac=1).reset_index(drop=True)
            df.head()
            df['label'] = df['label'].astype('str')
            df.head()

            train, test = train_test_split(df, test_size=0.2, random_state=42)

            train_generator = ImageDataGenerator(
                rescale=1. / 255,
                rotation_range=40,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True,
                fill_mode='nearest'
            )

            val_generator = ImageDataGenerator(rescale=1. / 255)

            train_iterator = train_generator.flow_from_dataframe(
                train,
                x_col='images',
                y_col='label',
                target_size=(image_size, image_size),
                batch_size=512,
                class_mode='binary'
            )

            val_iterator = val_generator.flow_from_dataframe(
                test,
                x_col='images',
                y_col='label',
                target_size=(image_size, image_size),
                batch_size=512,
                class_mode='binary'
            )

            self.model = Sequential([
                Conv2D(16, (3, 3), activation='relu', input_shape=(image_size, image_size, 3)),
                MaxPool2D((2, 2)),
                Conv2D(32, (3, 3), activation='relu'),
                MaxPool2D((2, 2)),
                Conv2D(64, (3, 3), activation='relu'),
                MaxPool2D((2, 2)),
                Flatten(),
                Dense(512, activation='relu'),
                Dense(1, activation='sigmoid')
            ])
            self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            self.model.summary()
            self.model.fit(train_iterator, epochs=10, validation_data=val_iterator)
            self.model.save(save_model_path)
        else:
            self.model = keras.models.load_model(load_model_path,
                                                 compile=True
                                                 )

    def recognize(self, image_path):
        image = load_img(image_path, target_size=(image_size, image_size))
        image_array = keras.utils.img_to_array(image)
        image_array = keras.backend.expand_dims(image_array, 0)

        prediction = self.model.predict(image_array)
        if prediction[0] > 0.5:
            predict = "notmine"
        elif prediction[0] <= 0.5:
            predict = "mine"

        print("Image: ", image_path, " is classified as: ", predict)
        if predict == "mine":
            return True
        else:
            return False
