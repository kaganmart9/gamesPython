import random  # Import the random module for making random selections
import PySimpleGUI as sg  # Import the PySimpleGUI module for creating the GUI

# List of words
words = ["apple", "banana", "cherry", "date", "elephant", "frog", "giraffe", "house", "island", "jungle", "kite", "lemon", "mountain", "notebook", "orange", "pencil", "queen", "river", "sun", "tiger"]

# Hangman drawing stages
hangman_stages = [
    "-----\n|   |\n    |\n    |\n    |\n    |\n--------",
    "-----\n|   |\nO   |\n    |\n    |\n    |\n--------",
    "-----\n|   |\nO   |\n|   |\n    |\n    |\n--------",
    "-----\n|   |\nO   |\n/|  |\n    |\n    |\n--------",
    "-----\n|   |\nO   |\n/|\\ |\n    |\n    |\n--------",
    "-----\n|   |\nO   |\n/|\\ |\n/   |\n    |\n--------",
    "-----\n|   |\nO   |\n/|\\ |\n/ \\ |\n    |\n--------"
]

# Function to start the game
def start_game():
    random_word = random.choice(words)  # Select a random word from the list
    lives = len(hangman_stages) - 1  # Set the number of lives based on hangman stages
    guessed_word = ['_'] * len(random_word)  # Create a list to store the guessed word state
    wrong_guesses = []  # List to store wrong guesses

    # Define the layout of the GUI
    layout = [
        [sg.Text(' '.join(guessed_word), key='-WORD-', font=('Helvetica', 40), justification='center', expand_x=True)],  # Display the guessed word
        [sg.Input(key='-INPUT-', do_not_clear=False, expand_x=True, justification='center', font=('Helvetica', 20), enable_events=True)],  # Input field for user guesses
        [sg.Button('Guess', bind_return_key=True, size=(10, 2))],  # Guess button
        [sg.Text(hangman_stages[0], key='-HANGMAN-', font=('Courier', 20), justification='center', expand_x=True)],  # Display the hangman drawing
        [sg.Text(f'Remaining Lives: {lives}', key='-LIVES-', font=('Helvetica', 12), justification='center', expand_x=True)],  # Display remaining lives
        [sg.Text('Wrong Guesses: ', key='-WRONG-', size=(40, 1), font=('Helvetica', 12), justification='center', expand_x=True)],  # Display wrong guesses
        [sg.Button('Exit', size=(10, 2), pad=((0, 0), (20, 0)))]  # Exit button at the bottom right
    ]

    window = sg.Window('Hangman Game', layout, resizable=True, finalize=True, return_keyboard_events=True)  # Create the window with the defined layout
    window.maximize()  # Maximize the window

    # Function to update the guessed word
    def update_guessed_word(user_guess, random_word, guessed_word):
        if user_guess in random_word:  # If the guessed letter is in the word
            for index, letter in enumerate(random_word):  # Iterate through the word
                if letter == user_guess:  # If the letter matches the guessed letter
                    guessed_word[index] = user_guess  # Update the guessed word
        return guessed_word

    # Event loop
    while True:
        event, values = window.read()  # Read events and values from the window
        if event == sg.WIN_CLOSED or event == 'Exit':  # If the window is closed or Exit button is clicked
            break
        if event == 'Guess' or event == 'Return:13':  # If the Guess button is clicked or Enter key is pressed
            user_input = values['-INPUT-'].lower()  # Get the user input and convert to lowercase
            window['-INPUT-'].update('')  # Clear the input field
            if len(user_input) == 1:  # If the user input is a single letter
                if user_input in random_word:  # If the guessed letter is in the word
                    guessed_word = update_guessed_word(user_input, random_word, guessed_word)  # Update the guessed word
                else:
                    lives -= 1  # Decrease the number of lives
                    wrong_guesses.append(user_input)  # Add the wrong guess to the list
                    window['-HANGMAN-'].update(hangman_stages[len(hangman_stages) - lives - 1])  # Update the hangman drawing
                    window['-WRONG-'].update(f'Wrong Guesses: {", ".join(wrong_guesses)}')  # Update the wrong guesses display
            elif user_input == random_word:  # If the user guesses the whole word correctly
                guessed_word = list(random_word)  # Update the guessed word to the correct word
                break
            else:  # If the user guesses the whole word incorrectly
                lives -= 1  # Decrease the number of lives
                window['-HANGMAN-'].update(hangman_stages[len(hangman_stages) - lives - 1])  # Update the hangman drawing
            window['-WORD-'].update(' '.join(guessed_word))  # Update the guessed word display
            window['-LIVES-'].update(f'Remaining Lives: {lives}')  # Update the remaining lives display
        if '_' not in guessed_word or lives == 0:  # If the game is over (word guessed or no lives left)
            result = 'Game Over!' if lives == 0 else 'You Win!'  # Determine the result message
            layout_end = [
                [sg.Text(result, font=('Helvetica', 20), justification='center')],  # Display the result message
                [sg.Button('Restart', size=(10, 2)), sg.Button('Exit', size=(10, 2))]  # Restart and Exit buttons
            ]
            window_end = sg.Window('Game Over', layout_end, modal=True)  # Create a modal window for the end game
            while True:
                event_end, _ = window_end.read()  # Read events from the end game window
                if event_end == 'Restart':  # If the Restart button is clicked
                    window_end.close()  # Close the end game window
                    random_word = random.choice(words)  # Select a new random word
                    lives = len(hangman_stages) - 1  # Reset the number of lives
                    guessed_word = ['_'] * len(random_word)  # Reset the guessed word
                    wrong_guesses = []  # Reset the wrong guesses
                    window['-WORD-'].update(' '.join(guessed_word))  # Update the guessed word display
                    window['-HANGMAN-'].update(hangman_stages[0])  # Reset the hangman drawing
                    window['-LIVES-'].update(f'Remaining Lives: {lives}')  # Update the remaining lives display
                    window['-WRONG-'].update('Wrong Guesses: ')  # Reset the wrong guesses display
                    break
                if event_end == sg.WIN_CLOSED or event_end == 'Exit':  # If the end game window is closed or Exit button is clicked
                    window_end.close()  # Close the end game window
                    window.close()  # Close the main game window
                    return  # Exit the function

start_game()  # Start the game