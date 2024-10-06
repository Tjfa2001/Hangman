import Pictures as p
import Words as w
import Rules as r
import random as rand
import tkinter as tk
import keyboard as k

class HangGame:
    
    # Variables initialised
    word = ""
    incorrect_guess_count = 0
    guesses_to_win = 0
    letters_in_word_to_guess = []
    correct_guesses = []
    guessed_letters = []
    keyboard = ['Q','W','E','R','T','Y','U','I','O','P','.','A','S','D','F','G','H','J','K','L','.','Z','X','C','V','B','N','M','.']
    commands = ['A','R']

    root = "none"

    
    # Constructor for Hangman
    def __init__(self):
        self.createGUI()
        #root = tk.Tk()
        #root.geometry("500x500")
        #root.title("Hangman Game")
        #entry = tk.Entry()
        #entry.pack(padx=10,pady=10)
        button = tk.Button(self.root,text="Press to start the game",command=self.start_game)
        button.pack()

        """
        def get_entry_text(event):
        # Get the text from the Entry widget
            user_input = entry.get()
            print("User typed:", user_input)
            # Clear the entry after capturing the text (optional)
            entry.delete(0, tk.END)
        
        # Bind the Enter key (Return key) to the function
        entry.bind("<Return>", get_entry_text)

        # Run the Tkinter main loop
        root.mainloop()
        """

    def createGUI(self):
        root = tk.Tk()
        self.root = root
        root.geometry("500x500")
        root.title("Hangman Game")
        entry = tk.Entry(root)
        entry.pack(padx=50,pady=50)
        root.mainloop()
        """
        correctInput = False

        # Lets user decide if they want to start a game
        while not correctInput:
            answer = input("Would you like to start a game? [Y/N]\n").upper()
            if answer == 'Y':
                correctInput = True
                print("Game starting...")
                self.start_game()
            elif answer == 'N':
                correctInput = True
                print("Exiting...")
            else:
                print("Incorrect input")
        """

    # Refreshes and starts the game
    def start_game(self):
        self.reset_all()
        word = self.pick_word()
        self.analyse_word(word)
        self.print_rules()
        self.print_gallows()
        self.print_word()
        self.take_guess()

    # Resets any details associated with previous play
    def reset_all(self):
        self.incorrect_guess_count = 0
        self.letters_in_word_to_guess = []
        self.correct_guesses = []
        self.guessed_letters = []

    # Picks a random word for the player to guess    
    def pick_word(self):
        num_possible_words = len(w.words)
        random_number = rand.randrange(0,num_possible_words,1)
        self.word = w.words[random_number]
        return self.word
    
    # Gets the length and unique letters from the word
    def analyse_word(self, word):
        # Checks if the letters in the word are already in the correct letters list
        for letters in word:
            if letters.upper() in self.letters_in_word_to_guess:
                continue
            else:
                self.letters_in_word_to_guess.append(letters.upper())

        self.guesses_to_win = len(self.letters_in_word_to_guess)
    
    # Prints the rules to the user
    def print_rules(self):
        rules = r.rules
        for line in rules:
          print(line)

    # Prints the gallows for the player
    def print_gallows(self):
        print(p.hang_pics[self.incorrect_guess_count] + "\n")

    # Prints the letters to the player
    def print_word(self):
        string = ""
        for letter in self.word:
            if letter.upper() in self.correct_guesses:
                string = string + letter.upper() + " "
            else:
                string = string + "_ "
        print(string)

    # Takes the guess from the player
    def take_guess(self):
        valid = False

        while not valid:
            guess = input("Guess a letter. Type /a to show all the letters you have already guessed or /r to reshow the rules\n").upper()
            valid = self.check_valid_input(guess)

        if(guess[0]=='/'):
            
            if(guess[1]=='A'):
                self.show_letters()
            elif(guess[1]=='R'):
                self.print_rules()
                input("Press ENTER key to return to guessing")
                self.take_guess()
                
        else: self.try_guess(guess)
    
    # Sees whether the guess is correct or wrong
    def try_guess(self,guess):

        if guess in self.letters_in_word_to_guess and guess not in self.correct_guesses:
            self.correct_guesses.append(guess)
            self.guessed_letters.append(guess)
            self.check_win()
        elif guess in self.correct_guesses:
            pass
        else:
            self.incorrect_guess_count+=1
            self.guessed_letters.append(guess)
        
        self.redisplay()
    
    # Checks whether the player has inputted something valid
    def check_valid_input(self,guess):
        if len(guess) == 2 and guess[0] != '/':
            return False
        elif len(guess) == 2 and guess[0] == '/' and guess[1] in self.commands:
            return True
        elif len(guess) != 1:
            return False
        elif guess == '.':
            return False
        elif guess in self.keyboard:
            return True
        else:
            return False
    
    # Offers the player a chance to have another go
    def replay(self):
        replay = input("Would you like to play again? Press r to play again\n")
        if(replay == 'r'):
            self.start_game()
        else:
            return 0
    
    # Refreshes the gallows and word shown to the player
    def redisplay(self):
        self.print_gallows()

        if self.check_win():
            self.print_word()
            print("Well done! You won!")
            self.replay()
        elif self.incorrect_guess_count < 7:
            self.print_word() 
            self.take_guess()
        else:
            message = "Game Over! The correct word was {word}".format(word = self.word)
            print(message)
            self.replay()

    # Checks whether the player has correctly guessed the word or not
    def check_win(self):
        if self.guesses_to_win == len(self.correct_guesses):
            return True
        else:
            return False
    
    # Prints the word below the gallows
    def show_letters(self):
        string = ""
        for letter in self.keyboard:
            if letter in self.guessed_letters:
                string = string + "/ "
            elif letter == ".":
                print(string)
                string = ""
            else:
                string = string + letter + " "

        input("Press ENTER key to return to guessing")
        self.take_guess()
    
            
game = HangGame()