import matplotlib.pyplot as plt
import CNN
import task3

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

print("\n\n ==== TASK 3 ==== ")
task3.task3()