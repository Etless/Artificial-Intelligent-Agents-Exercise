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
def load_data(path, sheet):
    df = pd.read_excel(EXCEL_PATH, sheet_name=sheet)

    # Keep only the value column (assume column name is 'value')
    values = df.iloc[:, 2].values.reshape(-1, 1)

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
def plot_results(trainY, testY, train_predict, test_predict, title="RNN Prediction"):

    # Convert predictions to 1D
    train_predict = train_predict.flatten()
    test_predict = test_predict.flatten()

    # Create full-length arrays filled with NaN
    total_length = len(trainY) + len(testY)

    train_actual_plot = np.empty(total_length)
    train_actual_plot[:] = np.nan
    train_actual_plot[:len(trainY)] = trainY

    train_predict_plot = np.empty(total_length)
    train_predict_plot[:] = np.nan
    train_predict_plot[:len(trainY)] = train_predict

    test_actual_plot = np.empty(total_length)
    test_actual_plot[:] = np.nan
    test_actual_plot[len(trainY):] = testY

    test_predict_plot = np.empty(total_length)
    test_predict_plot[:] = np.nan
    test_predict_plot[len(trainY):] = test_predict

    # Plot
    plt.figure(figsize=(14,6))
    plt.plot(train_actual_plot, label="Train Actual")
    plt.plot(train_predict_plot, label="Train Prediction")
    plt.plot(test_actual_plot, label="Test Actual")
    plt.plot(test_predict_plot, label="Test Prediction")

    plt.title(title)
    plt.xlabel("Time Steps")
    plt.ylabel("Scaled Exchange Rate")
    plt.legend()
    plt.grid(True)
    plt.show()

# Variables used:
EXCEL_PATH = "C:\\Users\\Askar\\Downloads\\EXR2.xlsx"

time_steps = 12
SPLIT_PERCENT = 0.8

CURRENCY_SHEET = "BASE_CUR_EUR"

SHEETS = ["BASE_CUR_EUR", "BASE_CUR_GBP", "BASE_CUR_DKK", "BASE_CUR_USD"]

for SHEET in SHEETS:

    print(f"Currency: {SHEET}")
    # Normalize data
    data_ = load_data(EXCEL_PATH, SHEET)
    train_data, test_data, data = get_train_test(data_, SPLIT_PERCENT)

    train_X, train_Y = get_XY(train_data, time_steps)  # Training set
    test_X, test_Y = get_XY(test_data, time_steps)  # Test set

    model = create_RNN(
        hidden_units=3,
        dense_units=1,
        input_shape=(time_steps, 1),
        activation=["tanh", "tanh"]
    )

    model.fit(
        train_X, train_Y,
        epochs=20,
        batch_size=1,
        verbose=0
    )

    # Make predictions
    train_predict = model.predict(train_X)
    test_predict = model.predict(test_X)

    # Mean square error
    print_error(train_Y, test_Y, train_predict, test_predict)



    # Step 6
    plot_results(train_Y, test_Y, train_predict, test_predict,
             title=f"RNN Prediction - {SHEET}")


"""
# Step 1 & 2
# Get normalized data types
data_ = load_data(EXCEL_PATH, CURRENCY_SHEET)
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
"""