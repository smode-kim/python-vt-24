import json
import random
import sys

class Hangman:
    
    def __init__(self, start_level):
        """
        Initialize the game by setting some start value
        and importing some assets (from /assets/ folder)
        Shows an ascii art welcome message
        """

        # Set starting level
        self.level = start_level
        self.round_count = 0

        # Set base words dict
        with open("assets/words.json", 'r') as file:
            self.words = json.load(file)

        # Set winning message
        with open("assets/winner-message.txt", 'r') as file:
            self.winner_message = file.read()

        # Set welcome message
        with open("assets/welcome-message.txt", 'r') as file:
            welcome_message = file.read()

        # Print welcome message
        print(welcome_message)


    def play(self):
       """
       Main entry point for starting a new game
       Game will continue as long as there's tries left
       Current tries and Max tries will reset when user levels up
       """ 
       self.new_round()
       while self.current_tries < self.max_tries:
            guess = self.guess_character()
            self.validate_guess(guess)
       print("Game over")


    def new_round(self):
        """
        Initializes a new round of game play.
        It sets the max tries, the random word and shows the level status/info.
        """

        # Increase round counter
        self.round_count+=1
        self.max_tries = (2*self.level)+self.level
        self.current_tries = 0


        # Randomly get a word at current level dictionary
        self.hidden_word = self.get_random_word()
        self.guessed_word = self.obfuscate_word(self.hidden_word)

        print("--------------------------------------------------------------------------")
        print(" ")
        print(f"Welcome to round {self.round_count} of Hangman.")
        print(f"You are at level {self.level}, which gives you {self.max_tries} guesses.")
        print(" ")
        print(f"Try to guess this {len(self.hidden_word)} letter word: {self.guessed_word}")
        print(" ")
        print("--------------------------------------------------------------------------")
        print(" ")


    def guess_character(self):
        """
        Fetches a guess from the player.
        Shows some guess related instructions/info to the player.
        """

        print(" ")
        tries_left = self.max_tries-self.current_tries
        if tries_left == 1:
            print("Last try!")
        else:
            print(f"{self.max_tries-self.current_tries} tries left.")

        print(f"Current word {self.guessed_word}")
        self.new_guess = input("Type in your next guess: ")
        return self.new_guess
    


    def validate_guess(self, guessed_char):
        """
        The heart of the game!
        Validates user input/players guess against hidden word
        by iterating thru every character of the hidden word,
        comparing it to user input/players guess.
        """

        print(" ")
        
        # Make sure player has typed only 1 character
        if len(guessed_char) != 1:
            print("Please, write only one (1) character at each guess")
        else:    
            print(f"You guessed {guessed_char}")
            
            # Check for guessed character within hidden word
            found_in_hidden_word = False
            new_guessed_word = ""

            for i in range(len(self.hidden_word)):
                if self.hidden_word[i].lower() == guessed_char.lower():
                    new_guessed_word += guessed_char
                    found_in_hidden_word = True
                else:
                    new_guessed_word += self.guessed_word[i]
            
            # Update GUI to reveal correct guesses
            self.guessed_word = new_guessed_word

            # What's the overall outcome?
            # Guess again, next level or game complete
            if found_in_hidden_word:
                if self.guessed_word.lower() == self.hidden_word.lower():
                    print(self.winner_message)
                    if self.level == len(self.words):
                        print("CHAMP! You've completed the final level.")
                        sys.exit()
                    else:
                        self.level+=1
                        self.new_round()
                else:
                    print("Congrats! You've revealed one letter!")
            else:
                print("Sorry, not in the hidden word!")
                self.current_tries+=1



    def get_random_word(self):
        """
        Gets a random word from the word array of current level
        Using Python Random module
        """

        word_array = self.words["level"+str(self.level)]
        return random.choice(word_array)
    


    def obfuscate_word(self, word):
        """
        Obfuscates a word by replacing each charachter with an *
        """
        return_str = ""
        for char in word:
            return_str += "*"        
        return return_str
