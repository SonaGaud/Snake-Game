from tkinter import *
import random

# Constants for the game
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 150
SPACE_SIZE = 20
BODY_PARTS = 1
SNAKE_COLOR = "Green"
FOOD_COLOR = "purple"
BACKGROUND_COLOR = "black"

# class is a bluepint of real world objects
class Snake:
    # constructor with class members 
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize the snake's body parts
        for i in range(0, BODY_PARTS):
            # snake will appear in top left corner with [0,0]
            self.coordinates.append([0, 0])

        # Create rectangles representing the snake on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        # Generate food at random coordinates within the game area
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


# Global variables
score = 0
direction = 'down'
label = None
canvas = None

def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('arial',30), text="GAME OVER", fill="red", tag="gameover")

def restart_game():
    global score, direction, label, canvas, snake, food
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)


window = Tk()
window.title("Snake Game")
window.resizable(True, True)
# initial score
score = 0
# initial direction
direction = 'down'

# Restart Button
restart_button = Button(window, text="Restart Game", command=restart_game)
restart_button.pack()

label = Label(window, text="Score:{}".format(score), font=('arial', 18))
label.pack()
# our game window 
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
# to make our game window appear in centre will first update window
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# settting geometry
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# calling snake and food 
snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()