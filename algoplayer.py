import mouse
from circlegame import CircleGame

def mouse_move_decision(target):
    absolute_x, absolute_y = target
    # Calculate the direction vector and normalize it
    mouse_x, mouse_y = mouse.get_position()

    # Move the mouse up to 5 pixels closer to the circle
    new_mouse_x = move_closer(absolute_x, mouse_x)
    new_mouse_y = move_closer(absolute_y, mouse_y)

    # Save the mouse position log
    current_position = (mouse_x, mouse_y)
    new_position = (new_mouse_x, new_mouse_y)

    speed_loss = calculate_loss(current_position, new_position, target)

    return current_position, new_position

def move_closer(target, input_number):
    # A strict move command that returns the target when close enough
    distance = abs(target - input_number)
    if distance <= 5:
        output = target
    # Or returns a number 5 closer to the target
    elif input_number < target:
        output = input_number + 5
    else:
        output = input_number - 5
    return output

def calculate_loss(current_position, new_position, target):
    current_x, current_y = current_position
    new_x, new_y = new_position
    target_x, target_y = target

    # Calculate the loss in x direction
    x_loss = 0
    if abs(target_x - current_x) > 5:
        if (new_x - current_x) * (target_x - current_x) > 0:
            x_loss = 1 - abs(new_x - current_x) / 5
        else:
            x_loss = 1 + abs(new_x - current_x) / 5
    elif new_x != target_x:
        x_loss = abs(new_x - target_x) / 5

    # Calculate the loss in y direction
    y_loss = 0
    if abs(target_y - current_y) > 5:
        if (new_y - current_y) * (target_y - current_y) > 0:
            y_loss = 1 - abs(new_y - current_y) / 5
        else:
            y_loss = 1 + abs(new_y - current_y) / 5
    elif new_y != target_y:
        y_loss = abs(new_y - target_y) / 5

    # Calculate the overall loss
    loss = (x_loss + y_loss) / 2

    save_mouse_position_log(current_position, target, new_position, loss)

    return loss

def save_mouse_position_log(current_position, target_position, new_position, loss):
    with open("mouse_position_logs.csv", "a") as file:
        log_entry = f"{current_position[0]},{current_position[1]},{target_position[0]},{target_position[1]},{new_position[0]},{new_position[1]},{loss}\n"
        file.write(log_entry)

if __name__ == '__main__':
    game = CircleGame(mouse_move_decision, train=False)
    game.after(1000, game.move_mouse_and_click)  # Start moving the mouse and clicking after a 1-second delay
    game.mainloop()