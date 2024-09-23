# hangmanWithGUI

Hangman Game in Python with PySimpleGUI

This repository contains a Python implementation of the classic Hangman game using the PySimpleGUI library for a graphical user interface (GUI).

Features:

Random word selection from a built-in word list
Visual hangman representation with stages based on remaining lives
Guess input with case-insensitive matching
Live updates for guessed letters, hangman image, remaining lives, and wrong guesses
End-game screen with win/lose message and restart/exit options
Getting Started

Prerequisites:

Python 3.x (https://www.python.org/downloads/)
PySimpleGUI (install using pip install PySimpleGUI)
Run the Game:

Clone or download this repository.
Open a terminal or command prompt and navigate to the repository directory.
Run the script using python hangman.py (replace hangman.py with the actual file name if different).
How to Play:

The game will choose a random word from the provided list.
You'll see an empty word representation with underscores for each letter.
Guess a letter using the input field.
If the letter is in the word, it will be revealed in the corresponding positions.
If the letter is not in the word, a body part is added to the hangman image, and one life is deducted.
Continue guessing letters until you either:
Win: Guess all the letters correctly before running out of lives.
Lose: Run out of lives by guessing incorrect letters.
Restarting the Game:

After the game ends (win or lose), a window will appear with "Restart" and "Exit" buttons.
Click "Restart" to start a new game with a new word and full lives.
Customization (Optional):

You can modify the words list in hangman.py to include your own set of words.
Feel free to experiment with different visual styles for the hangman stages and text elements.
Additional Notes:

The hangman_stages list defines the sequence of images for the hangman visualization.
The update_guessed_word function handles updating the displayed word with correctly guessed letters.
Contributing:

We welcome contributions to improve this game. Feel free to fork this repository and submit pull requests with your enhancements.

I hope this README provides a clear and informative overview of the game. Enjoy playing Hangman!
