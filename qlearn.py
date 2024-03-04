import numpy as np
import random
import mouse
from keras.models import Sequential
from keras.layers import Dense, LeakyReLU
from circlegame import CircleGame

alpha = 0.1
gamma = 0.99
epsilon = 0.1


def mouse_move_decision(target):
    absolute_x, absolute_y = target
    current_position = mouse.get_position()
    mouse_x, mouse_y = current_position

    relative_x, relative_y = absolute_x - mouse_x, absolute_y - mouse_y
    current_state = np.array([[mouse_x, mouse_y, relative_x, relative_y]])


    action = epsilon_greedy(current_state, epsilon)
    new_mouse_x, new_mouse_y = apply_action(action)
    new_position = new_mouse_x, new_mouse_y

    relative_x, relative_y = absolute_x - new_mouse_x, absolute_y - new_mouse_y
    new_state = np.array([[new_mouse_x, new_mouse_y, relative_x, relative_y]])

    # Calculate reward
    reward = calculate_reward(current_state, new_state)

    # Update Q-values
    q_values = model.predict(current_state)
    next_q_values = model.predict(new_state)
    q_values[0, action] = q_values[0, action] + alpha * (reward + gamma * np.max(next_q_values) - q_values[0, action])

    # Train the model with the updated Q-values
    model.fit(current_state, q_values, epochs=1, verbose=0)

    return current_position, new_position

def mouse_move_decision_abs(target):
    absolute_x, absolute_y = target
    current_position = mouse.get_position()
    mouse_x, mouse_y = current_position
    current_state = np.array([[mouse_x, mouse_y, absolute_x, absolute_y]])

    action = epsilon_greedy(current_state, epsilon)
    new_mouse_x, new_mouse_y = apply_action(action)
    new_position = new_mouse_x, new_mouse_y

    new_state = np.array([[new_mouse_x, new_mouse_y, absolute_x, absolute_y]])

    # Calculate reward
    reward = calculate_reward(current_state, new_state)

    # Update Q-values
    q_values = model.predict(current_state)
    next_q_values = model.predict(new_state)
    q_values[0, action] = q_values[0, action] + alpha * (reward + gamma * np.max(next_q_values) - q_values[0, action])

    # Train the model with the updated Q-values
    model.fit(current_state, q_values, epochs=1, verbose=0)

    return current_position, new_position

def apply_action(action):
    match action:
        case 0:
            mouse.move(5,0, absolute=False)
        case 1:
            mouse.move(5,5, absolute=False)
        case 2:
            mouse.move(0,5, absolute=False)
        case 3:
            mouse.move(-5,5, absolute=False)
        case 4:
            mouse.move(-5,0, absolute=False)
        case 5:
            mouse.move(-5,-5, absolute=False)
        case 6:
            mouse.move(0,-5, absolute=False)
        case 7:
            mouse.move(5,-5, absolute=False)
    new_position = mouse.get_position()
    return new_position


def build_model():
    # Create the neural network model
    model = Sequential()
    model.add(Dense(128, activation=LeakyReLU(alpha=0.01), input_shape=(4,)))
    model.add(Dense(64, activation=LeakyReLU(alpha=0.01)))
    model.add(Dense(32, activation=LeakyReLU(alpha=0.01)))
    model.add(Dense(8, activation="linear"))

    model.compile(optimizer="adam", loss="mse")

    return model


def epsilon_greedy(state, epsilon):
    if random.random() < epsilon:
        return random.randint(0, 7)  # Choose a random action from the action space
    else:
        return np.argmax(model.predict(state))  # Choose the action with the highest Q-value

def calculate_reward(current_state, new_state):
    current_x, current_y, relative_target_x, relative_target_y = current_state[0]
    new_x, new_y = new_state[0][:2]

    current_distance = np.sqrt(relative_target_x ** 2 + relative_target_y ** 2)
    new_relative_target_x, new_relative_target_y = relative_target_x - (new_x - current_x), relative_target_y - (new_y - current_y)
    new_distance = np.sqrt(new_relative_target_x ** 2 + new_relative_target_y ** 2)

    # Distance difference is another way of saying speed toward target
    distance_difference = current_distance - new_distance

    # Calculate the reward based on how it is getting closer to the target
    reward = (800 / new_distance) * distance_difference
    print(reward)

    return reward

def calculate_reward_abs(current_state, new_state):
    current_x, current_y, target_x, target_y = current_state[0]
    new_x, new_y = new_state[0][:2]

    current_distance = np.sqrt((current_x - target_x) ** 2 + (current_y - target_y) ** 2)
    new_distance = np.sqrt((new_x - target_x)**2 + (new_y - target_y)**2)

    # Distance difference is another way of saying speed toward target
    distance_difference = current_distance - new_distance

    # Calculate the loss based on how it is getting closer to the target
    reward = (800 / new_distance) * distance_difference
    print(reward)

    return reward

def calculate_reward_old(current_state, new_state):
    current_x, current_y, target_x, target_y = current_state[0]
    new_x, new_y = new_state[0][:2]
    # Calculate the Euclidean distance between the current state and the target and then the new state and the target
    current_distance = np.sqrt((current_x - target_x)**2 + (current_y - target_y)**2)
    new_distance = np.sqrt((new_x - target_x)**2 + (new_y - target_y)**2)

    # Distance difference is another way of saying speed toward target
    distance_difference = current_distance - new_distance

    # Calculate the loss based on how well the new state got closer to the target
    reward = 10 - (distance_difference - 5) ** 2

    return reward


if __name__ ==  '__main__':
    model = build_model()

    game = CircleGame(mouse_move_decision, train=True)
    game.after(1000, game.move_mouse_and_click)
    game.mainloop()