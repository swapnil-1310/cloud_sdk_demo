import tkinter as tk
import random

# -----------------------------
# CATCH THE STARS - PYTHON GAME
# -----------------------------

WIDTH = 600
HEIGHT = 500

root = tk.Tk()
root.title("⭐ Catch the Stars")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black"
)
canvas.pack()

# Game variables
score = 0
lives = 3
game_over = False

# Player
player_width = 90
player_height = 20

player = canvas.create_rectangle(
    WIDTH // 2 - player_width // 2,
    HEIGHT - 50,
    WIDTH // 2 + player_width // 2,
    HEIGHT - 30,
    fill="cyan"
)

# Star
star = None
star_x = 0
star_y = 0
star_speed = 5


def create_star():
    global star, star_x, star_y

    star_x = random.randint(20, WIDTH - 20)
    star_y = 0

    star = canvas.create_text(
        star_x,
        star_y,
        text="⭐",
        font=("Arial", 24)
    )


def move_left(event):
    x1, y1, x2, y2 = canvas.coords(player)

    if x1 > 0:
        canvas.move(player, -30, 0)


def move_right(event):
    x1, y1, x2, y2 = canvas.coords(player)

    if x2 < WIDTH:
        canvas.move(player, 30, 0)


def update_score():
    canvas.itemconfig(
        score_text,
        text=f"Score: {score}     Lives: {'❤️' * lives}"
    )


def game_loop():

    global score, lives, game_over

    if game_over:
        return

    canvas.move(star, 0, star_speed)

    star_box = canvas.bbox(star)
    player_box = canvas.bbox(player)

    # Check collision
    if star_box and player_box:

        if (
            star_box[2] >= player_box[0]
            and star_box[0] <= player_box[2]
            and star_box[3] >= player_box[1]
            and star_box[1] <= player_box[3]
        ):

            score += 1

            canvas.delete(star)
            create_star()

            # Increase difficulty
            global star_speed
            star_speed = 5 + score // 5

            update_score()

    # Star missed
    elif star_box and star_box[1] > HEIGHT:

        lives -= 1
        update_score()

        canvas.delete(star)

        if lives <= 0:
            end_game()
            return

        create_star()

    root.after(30, game_loop)


def end_game():

    global game_over
    game_over = True

    canvas.create_rectangle(
        150, 170,
        450, 330,
        fill="black",
        outline="white",
        width=3
    )

    canvas.create_text(
        WIDTH // 2,
        210,
        text="GAME OVER",
        fill="red",
        font=("Arial", 32, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        255,
        text=f"Final Score: {score}",
        fill="white",
        font=("Arial", 20)
    )

    canvas.create_text(
        WIDTH // 2,
        295,
        text="Press R to restart",
        fill="cyan",
        font=("Arial", 15)
    )


def restart(event):

    global score, lives, game_over, star_speed

    if not game_over:
        return

    score = 0
    lives = 3
    star_speed = 5
    game_over = False

    canvas.delete("all")

    # Recreate player
    global player

    player = canvas.create_rectangle(
        WIDTH // 2 - player_width // 2,
        HEIGHT - 50,
        WIDTH // 2 + player_width // 2,
        HEIGHT - 30,
        fill="cyan"
    )

    global score_text

    score_text = canvas.create_text(
        WIDTH // 2,
        20,
        text="Score: 0     Lives: ❤️❤️❤️",
        fill="white",
        font=("Arial", 16, "bold")
    )

    create_star()
    game_loop()


# Score display
score_text = canvas.create_text(
    WIDTH // 2,
    20,
    text="Score: 0     Lives: ❤️❤️❤️",
    fill="white",
    font=("Arial", 16, "bold")
)

# Controls
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<a>", move_left)
root.bind("<d>", move_right)
root.bind("<r>", restart)

# Start game
create_star()
game_loop()

root.mainloop()