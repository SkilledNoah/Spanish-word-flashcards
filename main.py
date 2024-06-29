"""
---------------------------------------
    * Course: 100 Days of Code - Dra. Angela Yu
    * Author: Noah Louvet
    * Day: 31 - Password Manager
    * Subject: Tkinter GUI  - exception handling - csv data
---------------------------------------
"""

from tkinter import *
import pandas
from random import choice, randint

BACKGROUND_COLOR = "#B1DDC6"
COUNTDOWN_TIME = 3
current_card = {}
current_timer = COUNTDOWN_TIME
timer = None

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("spanish-english-flashcard-data.csv")
    word_dict = original_data.to_dict(orient="records")
else:
    word_dict = data.to_dict(orient="records")


# ------------------------------------- #
# tackle problem when there are no cards left
# ------------------------------------- #


def count_down(count):

    canvas.itemconfig(counter_text, text=str(count))
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        turn_card()


def is_known():
    word_dict.remove(current_card)
    data = pandas.DataFrame(word_dict)
    data.to_csv("words_to_learn.csv", index=False)
    next_card()


def next_card():
    global current_timer, current_card, timer
    if timer is not None:
        window.after_cancel(timer)

    canvas.itemconfig(card_image, image=front_img)
    current_timer = COUNTDOWN_TIME
    current_card = choice(word_dict)
    spanish_word = current_card["spanish"]

    canvas.itemconfig(language_text, text="Spanish", fill="black")
    canvas.itemconfig(word_text, text=spanish_word, fill="black")
    count_down(current_timer)


def turn_card():
    english_word = current_card["english"]
    canvas.itemconfig(card_image, image=back_img)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=english_word, fill="white")
    canvas.itemconfig(counter_text, text="")


window = Tk()
window.title("Flashcard Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="card_front.png")
back_img = PhotoImage(file="card_back.png")
card_image = canvas.create_image(400, 263, image=front_img)
canvas.grid(column=0, row=0, columnspan=2)
language_text = canvas.create_text(400, 150, text="Language", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
counter_text = canvas.create_text(700, 50, text="", font=("Ariel", 20, "bold"))

right_img = PhotoImage(file="right.png")
known_button = Button(image=right_img, highlightthickness=0, command=is_known, bd=0)
known_button.grid(column=1, row=1)
wrong_img = PhotoImage(file="wrong.png")
unknown_button = Button(image=wrong_img, highlightthickness=0, command=next_card, bd=0)
unknown_button.grid(column=0, row=1)

next_card()

window.mainloop()
