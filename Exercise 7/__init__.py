import matplotlib.pyplot as plt
import CNN

print("\n\n ==== TASK 2A ==== ")
model = CNN.task2a()
print("\n\n ==== TASK 2B ==== ")
train_ds, val_ds, test_ds = CNN.task2b(model)
print("\n\n ==== TASK 2C ==== ")
history = CNN.task2c(model, train_ds, val_ds)

# Plot figure
plt.figure()
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title('Training vs Validation Loss')
plt.show()

# Evaluate on Test Set
test_loss, test_acc = model.evaluate(test_ds)
print("Test Accuracy:", test_acc)

"""

model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_gen = datagen.flow_from_directory(
    "data/",
    target_size=(128,128),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    "data/",
    target_size=(128,128),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

history = model.fit(
    train_gen,
    epochs=20,
    validation_data=val_gen
)

import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.show()
"""