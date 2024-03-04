import tkinter as tk
import random
import mouse

class CircleGame(tk.Tk):
    def __init__(self, move_decision_callback, train=False):
        super().__init__()
        # Create the game window
        self.title("Circle Game")
        self.geometry("800x600+400+200")
        self.canvas = tk.Canvas(self, bg="white", width=800, height=600)
        self.canvas.pack()
        self.circle = None
        # Train runs don't have a time limit and the circle only moves when it is clicked.
        self.train = train
        self.create_circle()
        # Stop the game with the Escape key
        self.stop_flag = False
        self.score = 0
        self.canvas.bind("<Button-1>", self.on_click)
        self.bind("<Escape>", self.stop)
        # Circle game can be played with a variety of move decision scripts which is defined here
        self.move_decision_callback = move_decision_callback
        if not train:
            # End game after 1 minutes (60000 ms) if not a training session
            self.after(1000 * 60, self.end_game)

    def create_circle(self):
        # Draw Circle on a random spot
        if self.circle:
            self.canvas.delete(self.circle)
        x = random.randint(40, 760)
        y = random.randint(40, 560)
        self.circle = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="red")
        if not self.train:
            self.move_circle_timeout()

    def on_click(self, event):
        # Mouse clicks occur when the mouse is in the circle at the end of a move
        x, y = event.x, event.y
        self.score += 1
        self.create_circle()
        if not self.train:
            self.canvas.after_cancel(self.move_timeout)
            self.update_title()
    def move_circle_timeout(self):
        # Set a timer to move the circle during play sessions
        self.move_timeout = self.canvas.after(5000, self.create_circle)  # Move circle every 5 seconds
    def update_title(self):
        # Keep Score in the title bar
        self.title(f"Circle Game - Score: {self.score}")

    def end_game(self):
        # End the game after the 60 second timer on play runs
        self.canvas.unbind("<Button-1>")
        self.canvas.create_text(400, 300, text="Game Over", font=("Arial", 24), fill="black")
        self.event_generate("<Escape>")
    def move_mouse_and_click(self):
        # Looping script that manages the mouse movement and clicking when the mouse gets to the circle
        if not self.stop_flag and self.focus_displayof() == self:
            circle_x, circle_y = self.canvas.coords(self.circle)[:2]
            circle_x += 20  # Adjust for the circle radius
            circle_y += 20  # Adjust for the circle radius

            # Calculate the absolute position of the circle on the screen
            window_x, window_y = self.winfo_rootx(), self.winfo_rooty()
            target = window_x + circle_x, window_y + circle_y

            # Get a new mouse position from the decider
            current_position, new_position = self.move_decision_callback(target)
            new_mouse_x, new_mouse_y = new_position

            # Move the mouse to the new coordinates
            mouse.move(new_mouse_x, new_mouse_y)

            # Click if the mouse is close enough to the circle
            distance_sq = (new_mouse_x - target[0]) ** 2 + (new_mouse_y - target[1]) ** 2
            if distance_sq <= 64:
                mouse.click()

            self.after(80, self.move_mouse_and_click)  # Call this function every 80 milliseconds

    def stop(self, event):
        self.stop_flag = True
