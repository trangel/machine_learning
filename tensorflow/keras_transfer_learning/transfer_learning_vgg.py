"""
Author: Tonatiuh Rangel

Sample code to transfer learning using Keras.
This code is a simple modification of sample VGG image classification in the platform.

Other documentation can be found in 
https://towardsdatascience.com/keras-transfer-learning-for-beginners-6c9b8b7143e    
https://medium.com/@14prakash/transfer-learning-using-keras-d804b2e04ef8
"""


import numpy as np
from tensorflow import ConfigProto, Session
import tensorflow_hub as hub
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras import layers, Sequential, preprocessing
from tensorflow.keras.utils import get_file
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras import models
from tensorflow.keras import layers
import datetime
from keras import backend
from os import environ

IMAGE_SHAPE = (229, 229)

#
# Configuration
#
environ["CUDA_VISIBLE_DEVICES"] = "0"
config = ConfigProto()
backend.tensorflow_backend.set_session(Session(config=config))


def get_tensorboard_callback():

    log_dir = "logs/" + datetime.datetime.now().isoformat()
    tensorboard_callback = TensorBoard(
        log_dir=log_dir,
        histogram_freq=1,
        write_grads=True,
        write_images=True,
        update_freq="batch",
    )
    return tensorboard_callback


def get_input():
    data_root = get_file(
        "flower_photos",
        "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz",
        untar=True,
    )
    labels_path = get_file(
        "ImageNetLabels.txt",
        "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt",
    )
    image_labels = np.array(open(labels_path).read().splitlines())

    # Use ImageDataGeneration to iterate over images and due data agumentation
    image_generator = preprocessing.image.ImageDataGenerator(rescale=1 / 255)
    # image_data is an iterator that returns `image_batch, label_batch` pairs.
    image_data = image_generator.flow_from_directory(
        str(data_root), target_size=IMAGE_SHAPE
    )

    for image_batch, label_batch in image_data:
        print("Image batch shape: ", image_batch.shape)
        print("Label batch shape: ", label_batch.shape)
        break

    return image_data, image_labels


def build_model(image_data):
    """
    Builds a model starting from a VGG trained network.
    It sets last 2 layers as trainable
    Adds few layers at the end including the final softmax for the actual
    number of classes
    """

    # Load trained VGG. Note: don't include the top layer
    vgg_conv = VGG16(
        input_shape=IMAGE_SHAPE + (3,), weights="imagenet", include_top=False
    )

    # Freeze the layers except the last 2 layers
    for layer in vgg_conv.layers[:-2]:
        layer.trainable = False

    # Check the trainable status of the individual layers
    for layer in vgg_conv.layers:
        print(layer, layer.trainable)

    # Create the model
    model = models.Sequential()

    # Add the vgg convolutional base model
    model.add(vgg_conv)

    # Add new layers and final softmax with number of classes
    model.add(layers.Flatten())
    model.add(layers.Dense(1024, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(image_data.num_classes, activation="softmax"))

    return model


def train_model(model, image_data, tensorboard_callback):
    model.compile(optimizer=Adam(), loss="categorical_crossentropy", metrics=["acc"])

    steps_per_epoch = np.ceil(image_data.samples / image_data.batch_size)

    model.fit(
        image_data,
        epochs=2,  # too low just for testing
        steps_per_epoch=steps_per_epoch,
        callbacks=[tensorboard_callback],
    )


def main():

    tensorboard_callback = get_tensorboard_callback()

    image_data, _ = get_input()

    model = build_model(image_data)
    print(model.summary())

    train_model(model, image_data, tensorboard_callback)


if __name__ == "__main__":
    main()
