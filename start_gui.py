from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as font
from hangman import Ans, Player, Game

class Hangman_App:
    def __init__(self):
        self.game = Game()
        self.player = Player()
        self.app_x = 850
        self.app_y = 500

    def start_app(self):
        global root
        root = Tk()
        start = Start_frame()
        start.display()

        #set app title, icon and window size
        root.title('Hangman')
        icon_img = ImageTk.PhotoImage(Image.open('assets/player.png')) 
        #root.iconbitmap('assets/logo.gif')
        root.iconphoto(False, icon_img)
        root.geometry(f'{self.app_x}x{self.app_y}')

        root.mainloop()
        
#starting frame is where user inputs the word for the player to guess
class Start_frame(Hangman_App):
    def __init__(self):
        super().__init__()
        self.font = font.Font(size=35)

        #create input box        
        ans_img = Image.open('assets/input_ans.png').resize((382, 98))
        ans_img = ImageTk.PhotoImage(ans_img)
        self.ans_label = Label(root, image=ans_img)
        self.ans_label.image = ans_img

        #create logo
        start_img = Image.open('assets/start.png').resize((690, 227))
        start_img = ImageTk.PhotoImage(start_img)
        self.start_label = Label(root, image=start_img)
        self.start_label.image = start_img

        #create entry form
        self.ans_entry = Entry(root, width=15, bd=0, highlightthickness=0, font=self.font)
        self.ans_entry.focus()

        #create start button
        self.start_button = Button(root, text="S t a r t", font=self.font, width=8, height=2, command=self.start_game)

        #create error message label
        self.e_label = Label(root, text='', fg='grey')

    #function called when start button is pressed
    def start_game(self):
        in_ans = self.ans_entry.get()
        #validate the input and provide error message
        vali, e_msg = self.game.vali_ans(in_ans)
        self.e_label['text'] = e_msg
        #if the input is valid destroy all widget on the start frame and lauch game frame
        if vali:
            self.ans = Ans(in_ans) if in_ans != '' else Ans(self.game.get_word())
            self.start_label.destroy()
            self.start_button.destroy()
            self.ans_label.destroy()
            self.ans_entry.destroy()
            self.e_label.destroy()
            main = Main_frame(self.ans)
            main.display()
            
    #display all the widgets
    def display(self):
        self.ans_label.place(x=100, y=340)
        self.start_label.place(x=80, y=50)
        self.ans_entry.place(x=127, y=370)
        self.start_button.place(x=540, y=350)
        self.e_label.place(x=122, y=435)
        
#Main_frame is the main frame where the player guesses the word
class Main_frame(Hangman_App):
    def __init__(self, ans):
        super().__init__()
        self.ans = ans
        self.padtop = 20
        self.gap = 70 - (4 * self.ans.len)
        self.dash_w = (750 - (self.gap * (self.ans.len-1))) / self.ans.len
        self.dash_x = lambda i: i * (self.dash_w + self.gap) + 50
        #letter_height
        ltr_img = self.resize_img(Image.open('assets/empty_letter.png'))
        ltr_img = self.resize_ratio(ltr_img, 0.8)
        _, self.ltr_height = ltr_img.size

        #dash_img
        dash_img = self.resize_img(Image.open('assets/dash.png'))
        dash_img = ImageTk.PhotoImage(dash_img)
        self.dash_label = lambda: Label(root, image=dash_img)
        self.dash_label().image = dash_img

        #player_img
        player_img = self.resize_ratio(Image.open('assets/player.png'), 0.8)
        player_img = ImageTk.PhotoImage(player_img)
        self.player_label = Label(root, image=player_img)
        self.player_label.image = player_img
            
        #guess_entry
        self.guess_entry = Entry(root, width=3, bd=0, highlightthickness=0)
        self.guess_entry.focus()
            
        #guess_button
        self.guess_button = Button(root, text='submit', command=self.check_input)
        
        #error message
        self.e_msg = Label(root, text='Take your guess')

        #player's guesses and board image
        board_img = self.resize_ratio(Image.open('assets/board.png'), 0.8)
        board_img = ImageTk.PhotoImage(board_img)
        self.board_label = Label(root, image=board_img)
        self.board_label.image = board_img
        self.guesses_label = Label(root, text='')

    #resize image using ratio
    def resize_ratio(self, img, ratio):
        width, height = img.size
        width, height = int(width * ratio), int(height * ratio)
        return img.resize((width, height))
    
    def resize_img(self, img):
        width, height = img.size
        ratio = self.dash_w / width 
        #max height of image is 125
        if int(height * ratio) <= 125:
            new_height = int(height * ratio) 
        else:
            new_height = 125
            ratio = 125 / height
        new_width = int(width * ratio)

        return img.resize((new_width, new_height))

    #update the playerself's guesses
    def update_guesses(self):
        self.guesses_label['text'] = self.player.guesses
    
    def display_letter(self, char, i):
        ltr_img = self.resize_img(Image.open(f'assets/{char}.png'))
        ltr_img = self.resize_ratio(ltr_img, 0.8)
        ltr_img = ImageTk.PhotoImage(ltr_img)
        self.ltr_label = lambda: Label(root, image=ltr_img)
        self.ltr_label().image = ltr_img
        self.ltr_label().place(x = self.dash_x(i) + (self.dash_w * 0.1), y = self.padtop)
    
    #update how many letters have the playered guessed and display the progress
    def update_stat(self, guess):
        self.game.update_status(guess, self.ans, self.player)
        for i, char in enumerate(self.ans.word):
            if guess == char and guess not in self.ans.letters:
                self.display_letter(char, i)
                

    #update hang man image
    def update_hang(self):
        hang_img = self.resize_ratio(Image.open(f'assets/{self.player.lives}.png'), 0.72)
        hang_img = ImageTk.PhotoImage(hang_img)
        self.hang_label = Label(root, image=hang_img)
        self.hang_label.image = hang_img
        self.hang_label.place(x = 520, y = self.app_y - 320) 
    
    def restart(self):
        root.destroy()
        self.start_app()

    #check if player won or lost and display the correct image with a restart button and the correct answer
    def check_win(self):
        def win_or_lose():
            if self.ans.letters == set():
                return 'win'
            elif self.player.lives == 0:
                return 'lose'
            else:
                return 'go'

        game_res = win_or_lose()
        if game_res == 'win' or game_res == 'lose':
            self.e_msg.destroy()
            self.player_label.destroy()
            self.board_label.destroy()
            self.guess_button.destroy()
            self.guesses_label.destroy()
            restart_button = Button(root, text='restart', command=self.restart)
           
            over_img = ImageTk.PhotoImage(Image.open(f'assets/{game_res}.png'))
            over_label = Label(root, image=over_img)
            over_label.image = over_img
            over_label.place(x=60, y=200)
            restart_button.place(x=230, y=430)
            #display answer
            for i, char in enumerate(self.ans.word):
                self.display_letter(char, i)
            
    #check if player entered a valid guess and display an error message
    def check_input(self):
        guess = self.guess_entry.get()
        self.guess_entry.delete(0, END)
        check, self.e = self.player.guess(guess)
        self.e_msg['text'] = self.e
        if check:
            self.update_guesses()
            self.update_stat(guess)
            self.update_hang()
            self.check_win()

    #displaying
    def display(self):
        for i in range(self.ans.len):
            self.dash_label().place(x=self.dash_x(i), y=self.ltr_height + self.padtop + 5)
        self.player_label.place(x=90, y=250)
        self.board_label.place(x=330, y=300)
        self.guess_entry.place(x=190, y=275)
        self.guess_button.place(x=168, y=363)
        self.e_msg.place(x=50, y=220)
        self.guesses_label.place(x=360, y=330)

if __name__ == "__main__":
    hangman_app = Hangman_App()
    hangman_app.start_app()