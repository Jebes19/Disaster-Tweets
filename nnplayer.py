import mouse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint
from circlegame import CircleGame
from algoplayer import calculate_loss

# Learning with a strict Neural network learns the general idea of moving toward the target but struggles to actually get to the target

def build_model():
    # Create the neural network model
    model = Sequential()
    model.add(Dense(256, activation="relu", input_shape=(4,)))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(64, activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(2, activation="linear"))

    model.compile(optimizer="adam", loss="mse")

    return model
def mouse_move_decision(target):
    absolute_x, absolute_y = target
    current_position = mouse.get_position()
    mouse_x, mouse_y = current_position
    input_data = np.array([[mouse_x, mouse_y, absolute_x, absolute_y]])
    new_position = model(input_data, training=False).numpy().astype(int)[0]

    calculate_loss(current_position, new_position, target)

    return current_position, new_position



def load_data():
    data = pd.read_csv("train data.csv", header=None, names=["current_x", "current_y", "target_x", "target_y", "new_x", "new_y", "loss"])

    X = data[["current_x", "current_y", "target_x", "target_y"]].values
    y = data[["new_x", "new_y"]].values

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_val = X_val.reshape(X_val.shape[0], X_val.shape[1], 1)

    return X_train, X_val, y_train, y_val

def fitting(model):
    # Define early stopping and model checkpoint callbacks
    early_stopping = EarlyStopping(monitor="val_loss", patience=5, verbose=1, restore_best_weights=True)

    # Train the model with callbacks
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=8,
              callbacks=[early_stopping])

    return model


if __name__ ==  '__main__':
    # Load data
    X_train, X_val, y_train, y_val = load_data()
    model = build_model()
    model = fitting(model)

    game = CircleGame(mouse_move_decision)
    game.after(1000, game.move_mouse_and_click)
    game.mainloop()