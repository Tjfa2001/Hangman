import Pictures as p
import Words as w
import Rules as r
import random as rand
import tkinter as tk
import keyboard as k

class HangGame:
    
    # Word Variables
    word = ""
    letters_in_word_to_guess = []

    # Guessing variables
    incorrect_guess_count = 0
    guesses_to_win = 0
    correct_guesses = []
    guessed_letters = []

    # GUI variables
    root = ""
    gallows = ""
    word_with_gaps = ""
    end_game = ""

    # Auxiliary variables
    keyboard = ['Q','W','E','R','T','Y','U','I','O','P','.','A','S','D','F','G','H','J','K','L','.','Z','X','C','V','B','N','M','.']
    started = False

    # Constructor for Hangman
    def __init__(self):
        self.createGUI()
        
    # Crates the GUI to interact with the hangman game
    def createGUI(self):
        # Sets root pane to 500 x 500 px frame with pale turquoise background
        root = tk.Tk()
        self.root = root
        root.config(background="pale turquoise")
        root.geometry("500x500")
        root.title("Hangman Game")

        # Box for player to input letters
        entry = tk.Entry(root)
        entry.pack(padx=50,pady=20)

        # Box displaying the gallows for the game
        self.gallows = tk.Label(root,text=p.hang_pics[0],background="pale turquoise",foreground="DodgerBlue2")
        self.gallows.pack()

        # Displaying the word in its current guess state
        self.word_with_gaps = tk.Label(root,text="",font=(50),background="pale turquoise",foreground="DodgerBlue2")
        self.word_with_gaps.pack()

        # Button to start the game
        start_button = tk.Button(root,text="Press to start or restart the game",command=self.start_game)
        start_button.pack(pady=10)
        
        # Putting the rules onto the frame
        self.print_rules()

        # Text for when the game has ended
        end_game = tk.Label(root,text="",background="pale turquoise",foreground="DodgerBlue2")
        end_game.pack()
        self.end_game = end_game

        # Get the text from the entry widget
        def get_entry_text(event):
            # Converts it to uppercase 
            user_input = entry.get().upper()
            entry.delete(0, tk.END)
            
            valid = False
            valid = self.check_valid_input(user_input)
            
            if valid and self.started:
                #print("guess was {a}".format(a=user_input))
                self.try_guess(user_input)
            else:
                pass
             
        entry.bind("<Return>", get_entry_text)
        root.mainloop()

    # Refreshes and starts the game
    def start_game(self):
        self.started = True
        self.reset_all()
        word = self.pick_word()
        self.analyse_word(word)
        self.print_gallows()
        self.print_word()
        
    # Resets any details associated with previous play
    def reset_all(self):
        # Reinitializes all the variables back to starting values
        self.incorrect_guess_count = 0
        self.letters_in_word_to_guess = []
        self.correct_guesses = []
        self.guessed_letters = []

    # Picks a random word for the player to guess    
    def pick_word(self):
        # Counts possible words
        num_possible_words = len(w.words)
        # Picks a random index
        random_number = rand.randrange(0,num_possible_words,1)
        # Selects the random word from the import 'w'
        self.word = w.words[random_number]
        return self.word
    
    # Gets the length and unique letters from the word
    def analyse_word(self, word):
        # Goes through the word letter by letter
        for letters in word:
            # Checks if the letters in the word are already in the correct letters list
            if letters.upper() in self.letters_in_word_to_guess:
                continue
            else:
                # Adds distinct letters to the letters to guess list
                self.letters_in_word_to_guess.append(letters.upper())

        # Number of guesses to win is the number of distinct letters in the word
        self.guesses_to_win = len(self.letters_in_word_to_guess)
    
    # Prints the rules to the user
    def print_rules(self):
        # Rules are stored in the import 'r'
        rules = r.rules
        rule_label = tk.Label(self.root,text=rules,font=("Ariel",10))
        rule_label.pack(pady=20)

    # Prints the gallows for the player
    def print_gallows(self):
        self.gallows.config(text=p.hang_pics[self.incorrect_guess_count])

    # Prints the letters to the player
    def print_word(self):
        string = ""
        for letter in self.word:
            if letter.upper() in self.correct_guesses:
                string = string + letter.upper() + " "
            else:
                string = string + "_ "

        self.word_with_gaps.config(text = string)
        #print(string)

    # Sees whether the guess is correct or wrong
    def try_guess(self,guess):

        # Checks if the letter guessed is correct and not guessed before
        if guess in self.letters_in_word_to_guess and guess not in self.correct_guesses:
            # Adds the letter to the list of correct guesses and guessed letters
            self.correct_guesses.append(guess)
            self.guessed_letters.append(guess)
        
        # Checks if the letter has already been guessed
        elif guess in self.guessed_letters:
            pass
        else:
            # Otherwise, the guess must be wrong
            self.incorrect_guess_count+=1
            # Adds the letter to the guessed letters list
            self.guessed_letters.append(guess)
        
        # Updates the GUI display
        self.redisplay()
    
    # Checks whether the player has inputted something valid
    def check_valid_input(self,guess):
    
        if len(guess) != 1:
            return False
        elif guess == '.':
            return False
        elif guess in self.keyboard:
            return True
        else:
            return False
    
    # Refreshes the gallows and word shown to the player
    def redisplay(self):

        # Updates the gallows
        self.print_gallows()

        if self.check_win():
            # Prints the complete word
            self.print_word()
            # Tells the player that they have won
            self.end_game.config(text="Well done! You won!")
            # Stops the game from accepting guesses
            self.started = False
        elif self.incorrect_guess_count < 7:
            # Prints the updated word if the game is still going
            self.print_word() 
        else:
            # Reveals the correct word to the player if the game is over
            self.end_game.config(text = "Game Over! The correct word was {word}".format(word = self.word.upper()))
            # Stops the game from accepting guesses
            self.started = False

    # Checks whether the player has correctly guessed the word or not
    def check_win(self):
        # Sees whether the number of correct guesses by the player is the same as the number needed to win
        if self.guesses_to_win == len(self.correct_guesses):
            return True
        else:
            return False
            
game = HangGame()