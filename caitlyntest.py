import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
import cv2
from os import listdir
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
import pathlib

data_dir = pathlib.Path("presivir/Games by Gameness")

batch_size = 32
img_height = 272
img_width = 480

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

size = (136, 240)

train_ds = train_ds.map(lambda x, y: (tf.image.resize(x, size), y))
val_ds = val_ds.map(lambda x, y: (tf.image.resize(x, size), y))

batch_size = 128
img_height = 272
img_width = 480

size = (136, 240)

input_shape = (136, 240, 3)

base_model = ResNet50(weights='imagenet', input_shape=input_shape, include_top=False)
base_model.trainable = False

inputs = keras.Input(shape=input_shape)
x = base_model(inputs, training=False)
x = keras.layers.GlobalAveragePooling2D()(x)
x = keras.layers.Dropout(0.2)(x)
x = keras.layers.Dense(1)(x)
outputs = keras.activations.sigmoid(x)
model = keras.Model(inputs, outputs)

model.compile(optimizer = keras.optimizers.Adam(lr=0.0001),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=[keras.metrics.BinaryAccuracy(name='accuracy', threshold=0.95),
                      keras.metrics.FalsePositives(thresholds=0.95),
                      keras.metrics.FalseNegatives(thresholds=0.95),
                      keras.metrics.Precision(thresholds=0.95),
                      keras.metrics.Recall(thresholds=0.95)])

checkpoint_path = "labs/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

model.load_weights(checkpoint_path)

game = 0
notgame = 0

for folder in listdir("presivir/test/"):
    for file in listdir("presivir/test/" + folder):
        if folder == "Sea of Thieves":
            for fil2e in listdir("presivir/test/" + folder + "/" + file):
                img = cv2.imread("presivir/test/" + folder + "/" + file + "/" + fil2e)
                image1 = image.load_img("presivir/test/" + folder + "/" + file + "/" + fil2e, target_size=(136, 240))
                image1 = image.img_to_array(image1)
                image1 = np.expand_dims(image1, axis = 0)
                model.predict(image1)
                output = model(image1)
                if output > 0.97:
                    cv2.imshow("test", img)
                    cv2.waitKey(0)
                print(output)

# for folder in listdir("presivir/test/"):
    
#     if folder == "osu!":

#         data_dir = pathlib.Path("presivir/test/" + folder)
#         print(data_dir)
            
#         test_ds = tf.keras.preprocessing.image_dataset_from_directory(
#             data_dir,
#             image_size=(img_height, img_width),
#             batch_size=batch_size)

#         test_ds = test_ds.map(lambda x, y: (tf.image.resize(x, size), y))

#         output = model.predict(test_ds)
#         print(output)

# model.evaluate(val_ds)