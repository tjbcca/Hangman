# Hangman Game
import random
from typing import List
from dataclasses import dataclass
from word_bank import *
from time import sleep


@dataclass
class stage_hangman:

    stage: int
    word: str
    game_difficulty: bool


# Global variables
letters_used = []

hangman0 = """
   _______
   |     |
   |
   |  
   |
   |
   | 
   |  
___|___
"""
hangman1 = """
   _______
   |  ___|___
   |  |     |
   |  |_____|
   |  
   |
   | 
   |  
___|___
"""
hangman2 = """
    _______
   |  ___|___
   |  |      |
   |  |______|
   |     |  
   |     |
   |     |
   |  
___|___ 

"""
hangman3 = """
   _______
   |  ___|___
   |  |      |
   |  |______|
   |     |  
   |   --|
   |     |
   |  
___|___  
  
"""
hangman4 = """
   _______
   |  ___|___
   |  |      |
   |  |______|
   |     |  
   |   --|--
   |     |
   |  
___|___   
"""
hangman5 = """
   _______
   |  ___|___
   |  |      |
   |  |______|
   |     |  
   |   --|--
   |     |
   |    /
___|___   
"""
hangman6 = """
   _______
   |  ___|___
   |  |      |
   |  |______|
   |     |  
   |   --|--
   |     |
   |    / \ 
___|___   
"""
highscore_counter = 0
game_round = 1
category = randomCat()
picked_word = randomWord(category)
currentgame = stage_hangman(0, str("_" * len(picked_word)), False)


# Function for starting a new game after completing the first round.
def newGame():
    global category
    global picked_word
    global currentgame
    global game_round
    global letters_used
    # ------------------------------------
    game_round += 1
    category = randomCat()
    picked_word = randomWord(category)
    letters_used = []
    if currentgame.game_difficulty == True:
        if currentgame.stage < 3:
            currentgame = stage_hangman(
                0, str("_" * len(picked_word)), currentgame.game_difficulty
            )
        else:
            currentgame = stage_hangman(
                (currentgame.stage - 3),
                str("_" * len(picked_word)),
                currentgame.game_difficulty,
            )
    else:
        currentgame = stage_hangman(
            0, str("_" * len(picked_word)), currentgame.game_difficulty
        )
    print(f"Round : {game_round}")
    print(f"Your word category is {category} {currentgame.word}")


# how to user will geuss the word
def wordguess(game_round) -> None:
    wordchosen = input("What is the word ").lower()
    if wordchosen == picked_word:
        print("You have have won this round\n")
        global highscore_counter
        if currentgame.game_difficulty == False:
            highscore_counter += 10
        else:
            highscore_counter += 20

        newGame()
    elif wordchosen != picked_word:
        print("You have chosen incorrectly")
        if currentgame.game_difficulty == False:
            currentgame.stage += 2
        else:
            currentgame.stage += 6
    else:
        print("Invalid answer")


# How the user will pick the letter of the word
def letterpick() -> None:
    print(f"Letters used {letters_used}")
    letter = input("Guess a letter ").lower()

    if len(letter) > 1:
        print("That is not a valid letter")
    else:
        if letter in letters_used:
            print("You have used this letter before")
        else:
            currentgame.word = ""
            letters_used.append(letter)
            for char in picked_word:
                if char in letters_used:
                    currentgame.word += char
                else:
                    currentgame.word += "_"
            if letter in currentgame.word:
                print(f"{letter} was part of the solution. ")
            else:
                print(f"{letter} was not part of the solution.")
                if currentgame.game_difficulty == False:
                    currentgame.stage += 1
                else:
                    currentgame.stage += 2


# The function for displaying the hangman visual
def hangman_vis(stage):
    if stage == 0:
        return hangman0
    elif stage == 1:
        return hangman1
    elif stage == 2:
        return hangman2
    elif stage == 3:
        return hangman3
    elif stage == 4:
        return hangman4
    elif stage == 5:
        return hangman5
    elif stage >= 6:
        print(hangman6)
        print("You have lost the game.")
        print(f"The word was {picked_word}")
        print(f"Your score was {highscore_counter}")
        highscore()
        exit()


def highscore():

    with open("project files/project 1/Highscore.txt", "r") as f:
        score = int(f.read())
    f.close()
    if highscore_counter > score:
        print(f"New High Score {highscore_counter}")
        with open("project files/project 1/Highscore.txt", "w") as x:
            x.write(str(highscore_counter))
            x.close()
    else:
        print(f"Highscore: {score}")


# This is to  make navigating code easier
def main() -> None:
    #print("Help you must save the prisoner from a false execution")
    #sleep(2.5)

    print("Welcome to Hangman")
    difficult = ""
    while True:
        difficult = str(input("Would you like to play [Normal] or [Hard] ")).lower()
        if difficult == "normal":
            currentgame.game_difficulty = False
            break
        elif difficult == "hard":
            currentgame.game_difficulty = True
            break
        else:
            print("Please enter either Normal or Hard.")
    print(f"Your word category is {category} {currentgame.word}")

    while True:
        if currentgame.stage < 0:
            currentgame.stage = 0

        print(hangman_vis(currentgame.stage))
        print(f"{currentgame.word} ({category})")

        select = str(input("Guess [l]etter, Guess [word], [quit]>  ")).lower()

        if select == "l":
            letterpick()
        elif select == "word":
            wordguess(game_round)
        elif select == "quit":
            print("")
            break
        else:
            print("Invalid Input")


if __name__ == "__main__":

    main()
