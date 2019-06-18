"""
Author: Tonatiuh Rangel

Sample code to transfer learning using tensorflow_hub and Keras.

This is a modification of  
https://github.com/tensorflow/hub/blob/master/examples/colab/tf2_image_retraining.ipynb
"""

import numpy as np
from tensorflow import ConfigProto, Session
import tensorflow_hub as hub
from tensorflow.keras import layers, Sequential, preprocessing
from tensorflow.keras.utils import get_file
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard
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
    Build a model by downloading a pre-trained headless model and adding 
    a final softmax layer for the actual number of classes
    """
    # Download the headless model
    # TensorFlow Hub also distributes models without the top classification layer.
    # These can be used to easily do transfer learning.
    # Any TensorFlow 1.x image feature vector URL from tfhub.dev will work here.
    # Note that only "tf2-preview" models are supported for now
    # feature_extractor_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/2"
    feature_extractor_url = (
        "https://tfhub.dev/google/tf2-preview/inception_v3/feature_vector/4"
    )

    feature_extractor_layer = hub.KerasLayer(
        feature_extractor_url, input_shape=IMAGE_SHAPE + (3,)
    )

    # Freeze the variables in the feature extractor layer, so that the training only
    # modifies the new classifier layer.
    feature_extractor_layer.trainable = False

    # Attach the classification head
    model = Sequential(
        [
            feature_extractor_layer,
            layers.Dense(image_data.num_classes, activation="softmax"),
        ]
    )

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
