import random
import tkinter
from tkinter import *

GAME_WIDTH = 1200
GAME_HEIGHT = 800
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill = SNAKE_COLOR, tags="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")

def next_move(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="score:{}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_move, snake, food)

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
        print("GAME OVER")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True

    return False

def game_over():
    global gameover
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('ds-digital', 70), text="GAME OVER", fill="red", tags="gameover")
    R = Button(window, text="Play again", command=restart, font=('ds-digital', 50), width=10, bg="gray",
               fg="green", activeforeground="green")   # PLAY AGAIN button
    canvas.create_window(600, 700,  window=R)

    S = Button(window, text="settings", command=settings, font=('ds-digital', 30), width=10, bg="gray", fg="black")
    canvas.create_window(1000, 700,  window=S)     # SETTINGS button

    gameover = True

def restart():
    canvas.delete(ALL)
    main()

def settings():
    canvas.delete(ALL)
    label.config(text="Settings")   # Settings window

    # TEXT
    canvas.create_text(100, 100, anchor=tkinter.NW, font=('ds-digital', 40),
                       text="speed: {}".format(SPEED), fill="grey")
    canvas.create_text(100, 200, anchor=tkinter.NW, font=('ds-digital', 40),
                       text="body parts: {}".format(BODY_PARTS), fill="grey")
    canvas.create_text(100, 300, anchor=tkinter.NW, font=('ds-digital', 40),
                       text="space size: {}".format(SPACE_SIZE), fill="grey")
    canvas.create_text(100, 400, anchor=tkinter.NW, font=('ds-digital', 40),
                       text="none", fill="grey")

    # Entry Boxes
    entry_speed = tkinter.Entry(window)
    canvas.create_window(canvas.winfo_width()/2, 125, window=entry_speed)
    entry_body_parts = tkinter.Entry(window)
    canvas.create_window(canvas.winfo_width() / 2, 225, window=entry_body_parts)
    entry_space_size = tkinter.Entry(window)
    canvas.create_window(canvas.winfo_width() / 2, 325, window=entry_space_size)

    # Save function
    def save():
        if entry_speed.get() != 0:
            SPEED = entry_speed.get()
        if entry_speed.get() != 0:
            BODY_PARTS = entry_body_parts.get()
        if entry_speed.get() != 0:
            SPACE_SIZE = entry_space_size.get()
        canvas.update()

    # Buttons
    R = Button(window, text="Play again", command=restart, font=('ds-digital', 50), width=10, bg="gray",
               fg="green", activeforeground="green")  # PLAY AGAIN button
    canvas.create_window(600, 700, window=R)
    Save = Button(window, text="SAVE", command=save, font=('ds-digital', 30), width=10, bg="gray", fg="black")
    canvas.create_window(1000, 700, window=Save)  # SAVE button


def main():
    global score
    score = 0

    label.config(text="score:{}".format(score))
    label.pack()
    canvas.pack()
    window.update()

    snake = Snake()
    food = Food()

    next_move(snake, food)

    window.mainloop()

window = Tk()
window.title("The Snake")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('ds-digital', 50))
label.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Up>', lambda event: change_direction('up'))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

snake = Snake()
food = Food()

next_move(snake, food)

window.mainloop()

main()