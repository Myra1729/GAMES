from tkinter import *
import random

# Constants
snake_color = "#0000FF"
food_color = "#FFFF00"
bg_color = "#000000"
game_width = 1000
game_height = 500
food_size = 50
snake_part = 50
speed = 100
n = 3  # Initial size of the snake
score = 0  # Initial score
direction = "down"  # Initial direction of the snake

class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = n
        self.coordinates = []
        self.parts = []
        # Initialize the snake starting from the middle of the canvas
        start_x = game_width // 2
        start_y = game_height // 2
        for i in range(0, n):
            self.coordinates.append([start_x, start_y - i * snake_part])
        for x, y in self.coordinates:
            part = canvas.create_rectangle(x, y, x + snake_part, y + snake_part, fill=snake_color, tag="snake")
            self.parts.append(part)

class Food:
    def __init__(self, canvas):
        # Randomly position the food within the canvas
        x = random.randint(0, (game_width // food_size) - 1) * food_size
        y = random.randint(0, (game_height // food_size) - 1) * food_size
        self.canvas = canvas
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + food_size, y + food_size, fill=food_color, tag="food")

def turn(snake, food):
    global score, direction

    # Calculate new head position based on current direction
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= snake_part
    elif direction == "down":
        y += snake_part
    elif direction == "left":
        x -= snake_part
    elif direction == "right":
        x += snake_part

    # Insert new head position at the beginning of the snake
    snake.coordinates.insert(0, [x, y])
    part = canvas.create_rectangle(x, y, x + snake_part, y + snake_part, fill=snake_color)
    snake.parts.insert(0, part)

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"SCORE={score}")
        canvas.delete("food")
        food = Food(canvas)
    else:
        # Remove the last part of the snake if no food was eaten
        del snake.coordinates[-1]
        canvas.delete(snake.parts[-1])
        del snake.parts[-1]

    # Check for collisions
    if check_collision(snake):
        game_over()
    else:
        # Schedule next turn
        game_window.after(speed, turn, snake, food)

def change_dir(new_dir):
    global direction
    # Change direction if the new direction is not directly opposite to the current one
    if new_dir == 'left' and direction != 'right':
        direction = new_dir
    elif new_dir == 'right' and direction != 'left':
        direction = new_dir
    elif new_dir == 'up' and direction != 'down':
        direction = new_dir
    elif new_dir == 'down' and direction != 'up':
        direction = new_dir

def check_collision(snake):
    x, y = snake.coordinates[0]
    # Check if the snake's head collides with the walls
    if x < 0 or x >= game_width or y < 0 or y >= game_height:
        return True
    # Check if the snake's head collides with its body
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    # Display "GAME OVER" message
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("consolas", 40), text="GAME OVER", fill="red", tag="game_over")

# Set up the game window
game_window = Tk()
game_window.title("NOKIA snake game")
game_window.resizable(False, False)
score = 0
direction = "down"

# Set up the score label
label = Label(game_window, text="SCORE=0", font=("Consolas", 40))
label.pack()

# Set up the canvas for the game
canvas = Canvas(game_window, bg=bg_color, width=game_width, height=game_height)
canvas.pack()

# Center the game window on the screen
game_window.update()
window_width = game_window.winfo_width()
window_height = game_window.winfo_height()
screen_width = game_window.winfo_screenwidth()
screen_height = game_window.winfo_screenheight()

x0 = (int)((screen_width - window_width) / 2)
y0 = (int)((screen_height - window_height) / 2)
game_window.geometry(f"{window_width}x{window_height}+{x0}+{y0}")

# Bind arrow keys to change direction
game_window.bind('<Left>', lambda event: change_dir("left"))
game_window.bind('<Right>', lambda event: change_dir("right"))
game_window.bind('<Up>', lambda event: change_dir("up"))
game_window.bind('<Down>', lambda event: change_dir("down"))

# Create the snake and food objects
snake = Snake(canvas)
food = Food(canvas)

# Start the game
turn(snake, food)
game_window.mainloop()
