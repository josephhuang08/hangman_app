import random

class Ans:
    def __init__(self, word):
        self.word = word
        self.len = len(self.word)
        self.letters = set(self.word)

class Player:
    def __init__(self, lives=8):
        self.lives = lives
        self.guesses = ''

    def guess(self, letter):
        letter = letter.strip()
        if not letter.isalpha():
            return False, 'Enter only letters'
        elif len(letter) != 1:
            return False, 'Enter only 1 letter'
        elif letter in self.guesses:
            return False, 'This letter has already been gussed'
        else:
            self.guesses = self.guesses + letter + ' '
            if len(self.guesses) == 14:
                self.guesses += '\n'
            return True, 'Take your guess'

class Game:
    def __init__(self):
        pass

    def update_status(self, guess, ans, player):
        if guess in ans.letters: #correct
            ans.letters.remove(guess)
        else: #wrong guess
            player.lives -= 1

    def vali_ans(self, in_ans):
        if in_ans == '':
            return True, ''
        elif ' ' in in_ans:
            return False, 'No spaces allowed'
        elif not in_ans.isalpha():
            return False, 'Enter only letters'
        elif len(in_ans) > 15:
            return False, 'Maximum 15 letters'
        elif len(in_ans) < 4:
            return False, 'Minimum 4 letters'
        else:
            return True, ''

    def get_word(self):
        with open('1-1000.txt', 'r') as f:
            contents = f.readlines()
            word = ''
            while len(word) < 4 or len(word) > 15:
                word = random.choice(contents).strip()
            
        return word