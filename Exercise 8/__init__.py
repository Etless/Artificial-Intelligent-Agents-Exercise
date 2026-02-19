import math

from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np

# Step 1
# Load data from Excel file
def load_data(path):
    df = pd.read_excel(EXCEL_PATH)

    # Keep only the value column (assume column name is 'value')
    values = df.iloc[:, 2].values.reshape(-1, 1)
    print(values)

    return values

# Step 2
# Split data into training and test data
def get_train_test(data, split_percent=0.2):
    scaler = MinMaxScaler(feature_range=(0,1))
    data = scaler.fit_transform(data).flatten()
    n = len(data)

    split = int(n * split_percent)
    train_data = data[range(split)]
    test_data = data[split:]

    return train_data, test_data, data

# Step 3
def get_XY(dat, time_steps):
    # Indices of target array
    Y_ind = np.arange(time_steps, len(dat), time_steps)
    Y = dat[Y_ind]

    # Prepare X
    rows_x = len(Y)
    X = dat[range(time_steps*rows_x)]
    X = np.reshape(X, (rows_x, time_steps, 1))

    return X, Y

# Step 4
def create_RNN(hidden_units, dense_units, input_shape, activation):
    model = Sequential()

    # RNN layer
    model.add(SimpleRNN(units=hidden_units,
                        activation=activation[0],
                        input_shape=input_shape))

    # Output layer
    model.add(Dense(units=dense_units,
                    activation=activation[1]))

    # Compile model
    model.compile(loss='mean_squared_error',
                  optimizer='adam')

    return model

# Step 5
def print_error(train_Y, test_Y, train_predict, test_predict):
    # Error of predictions
    train_rmse = math.sqrt(mean_squared_error(train_Y, train_predict))
    test_rmse = math.sqrt(mean_squared_error(test_Y, test_predict))

    print("\nTrain RMSE:", train_rmse)
    print("Test RMSE:", test_rmse)

# Step 6
def plot_results(trainY, testY, train_predict, test_predict):

    plt.figure(figsize=(12,6))

    # Training predictions
    plt.plot(trainY, label='Train Actual')
    plt.plot(train_predict, label='Train Prediction')

    # Shift test predictions for proper visualization
    offset = len(trainY)
    test_actual_plot = np.empty(len(trainY) + len(testY))
    test_actual_plot[:] = np.nan
    test_actual_plot[offset:] = testY

    test_predict_plot = np.empty(len(trainY) + len(testY))
    test_predict_plot[:] = np.nan
    test_predict_plot[offset:] = test_predict.flatten()

    plt.plot(test_actual_plot, label='Test Actual')
    plt.plot(test_predict_plot, label='Test Prediction')

    plt.legend()
    plt.title("RNN Prediction of NOK Exchange Rate")
    plt.show()

# Variables used:
EXCEL_PATH = "C:\\Users\\Askar\\Downloads\\EXR2.xlsx"
SPLIT_PERCENT = 0.8

# Step 1 & 2
# Get normalized data types
data_ = load_data(EXCEL_PATH)
train_data, test_data, data = get_train_test(data_, SPLIT_PERCENT)

# Step 3
time_steps = 12
train_X, train_Y = get_XY(train_data, time_steps) # Training set
test_X, test_Y   = get_XY(test_data, time_steps)  # Test set

# Step 4
model = create_RNN(
        hidden_units = 3,
        dense_units = 1,
        input_shape=(time_steps, 1),
        activation = ["tanh", "tanh"]
    )

model.fit(
    train_X, train_Y,
    epochs = 20,
    batch_size = 1,
    verbose = 2
)

# Step 5
# Make predictions
train_predict = model.predict(train_X)
test_predict = model.predict(test_X)

# Mean square error
print_error(train_Y, test_Y, train_predict, test_predict)

# Step 6
plot_results(train_Y, test_Y, train_predict, test_predict)