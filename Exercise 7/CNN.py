import tensorflow as tf
from tensorflow.keras import layers, models
import os

def task2a():
    # Task 2a
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.MaxPooling2D(2, 2),

        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    model.summary()

    return model

def task2b(model):
    # Base path to build other directories from
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Variables
    DIR_NAME = "data"
    train_dir = os.path.join(BASE_DIR, DIR_NAME, "train")
    val_dir = os.path.join(BASE_DIR, DIR_NAME, "val")
    test_dir = os.path.join(BASE_DIR, DIR_NAME, "test")

    img_size = (128, 128)
    batch_size = 32

    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size= img_size,
        batch_size=batch_size,
        label_mode="binary"
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        image_size= img_size,
        batch_size=batch_size,
        label_mode="binary"
    )

    test_ds = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        image_size= img_size,
        batch_size=batch_size,
        label_mode="binary"
    )

    # Normalize pixel values
    normalization_layer = layers.Rescaling(1. / 255)

    # Data is ready
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
    test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y))

    return train_ds, val_ds, test_ds

def task2c(model, train_ds, val_ds,):

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=20
    )

    return history