import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
from boggle import BoggleGame
import ex11_utils
import boggle_board_randomizer


GAME_TIME = 180
SHINE_GREEN = "#253342"
BLACK = "#B3B6F7"

'''
this class - BoggleGui - is in charge for:
1. the visual display of the game.
all the qualities of the BoggleGui classs have a part in the shown game.
2. the run of the game "mainloop".
the mainloop() is running in the Gui, and as a result the game itself running here. 
this class also response for the comunication with the user - as a result of the gui qualities.

the class getting all the game information from the object Boggle, and giving it the visual quality.
it calls "logic_game" here. 

'''

class BoggleGui:
    def __init__(self,board): #getting a board - from the logic.game
        root = tk.Tk()
        self.main_game = root
        self.main_game.title("Boggle Game")
        self.board = board
        self.show_board = tk.Frame(self.main_game)
        self.font = Font(root,family="Calibri", size=10)
        self.main_game.geometry("500x500")
        self.found_words = ""
        self.current_word = ""
        self.current_word_lst = []
        self.buttons = []
        #scrollbar
        self.scroll_bar = tk.Scrollbar(self.main_game)
        #score
        self.score = logic_game.score
        #time - the time is a quality of the Gui
        self.time = GAME_TIME
        self.minutes = GAME_TIME // 60
        self.seconds = GAME_TIME % 60
        self.timer = tk.Label(self.main_game, text ="Time: " + "{:02d}:{:02d}".format(self.minutes, self.seconds),
                        bg=BLACK, fg= SHINE_GREEN, font=self.font,height=2,width=10)
        #self feedback - with initial feedback
        self.feedback = "welcomeee"
        #background
        self._bg = tk.PhotoImage(file='background.png')

    def set_background(self): #setting the background
        background = tk.Label(self.main_game, image=self._bg)
        background.place(x=0, y=0, relwidth=1, relheight=1)
        background.lower()

    def show_found_words_head(self):
        #creating the label that reprasenting the "found words" above the found words list
        found_words = tk.Label(self.main_game,
                               text="Found Words",
                               bg=BLACK,fg=SHINE_GREEN,
                               font=self.font, height=2,width=22)
        found_words.place(x=310, y=190)

    def initiate_scrollbar(self):
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.BOTH)
    def show_found_words(self):
        '''
        this function is response of show the found words list.
        '''
        printing_words = logic_game.print_found_words()
        found_words = tk.Text(self.main_game,height=15,width = 20,bg=BLACK,fg=SHINE_GREEN)
        found_words.place(x= 310, y=235)
        found_words.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=found_words.yview)
        content = printing_words
        found_words.insert(tk.END,content)
        game.main_game.after(1000, self.show_found_words)
    def show_score(self): #showing the score and updating it.
        score_head = tk.Label(self.main_game, text="Score: " + str(logic_game.score), bg=BLACK,fg=SHINE_GREEN, font=self.font,height=2,width=8)
        score_head.place(x=310, y=135)
        game.main_game.after(1000, self.show_score)
    def show_time(self): #showing time
        self.timer.place(x=390, y=135)

    def time_is_up(self): #when time is up - showing the score, waiting for the user choise in the massagebox.
        if self.time <= 0:
            result = tk.messagebox.askyesno(title="Game Over", message="your score is:" + str(logic_game.score)
                                                                       + "\n" + "Would you like to play again?")
            if result == True:
                #if the user clicked "yes" - play another game.
                self.time = GAME_TIME
                logic_game.current_word = ""
                self.show_current_string()
                logic_game.board = boggle_board_randomizer.randomize_board()
                self.board = logic_game.board
                #
                self.run()
            elif result == False:
                #if the user clicked "no" - stop the game.
                self.main_game.destroy()
    def update_timer_label(self): #this function making the timer to blink when there is 30 seceonds left.
        if 0 < self.time <= 30:
            if self.timer['bg'] == 'red':
                self.timer['bg'] = BLACK
            else:
                self.timer['bg'] = 'red'
            self.main_game.after(50,self.update_timer_label)

    def run_time(self):#this function is making the time running.
        self.minutes = self.time // 60
        self.seconds = self.time % 60
        self.timer.config(text="Time: " + "{:02d}:{:02d}".format(self.minutes, self.seconds))
        if self.time > 0:
            self.update_timer_label()
            self.timer.after(1000, self.run_time)
            self.time -= 1
        else:
            self.time_is_up()

    def show_current_string(self): #shown the current string.
        word = tk.Label(self.main_game, text=logic_game.current_word, bg=BLACK,
                        fg=SHINE_GREEN,
                        font=Font(family="Calibri", size=20) ,height=1,width=15)
        word.place(x=30, y=100)
        game.main_game.after(1000, self.show_current_string)


    def show_feedback(self): #creating the feedback label - that getting the text from the logic_game
        feedback = tk.Label(self.main_game,text=logic_game.feedback,
                            bg= BLACK, font=Font(family="Calibri", size=30),
                            fg=SHINE_GREEN, height=1, width=15)
        feedback.place(x=30, y=20)
        game.main_game.after(1000, self.show_feedback)
    #hint
    def show_hint(self):# button that show a hint
        hint = logic_game.get_random_hint()
        if hint != []:
            for cor in hint:
                self.buttons[cor[0]][cor[1]].flash()

    def hint_button(self): #creating the hint button
        hint = tk.Button(self.main_game, text="Hint", command=self.show_hint, font=self.font, height=1, width=5,
                          bg=BLACK, fg=SHINE_GREEN)
        hint.place(x=420, y=50)
    #end of hint


    def show_del(self): #button that delete letter from the current string
        delete = tk.Button(self.main_game, text = "del", command=logic_game.del_letter, font=self.font, height=1, width=3,bg = BLACK, fg=SHINE_GREEN)
        delete.place(x=355, y=90)

    def show_start(self):#button that shows start\pause the start or pause the game
        start = tk.Button(self.main_game,text = "Start", command = self.start_game,font = self.font,height=1, width =3,bg = BLACK, fg=SHINE_GREEN)
        start.place(x= 395,y =90)
    def exit_mainloop(self): #function that stop the game and exiting.
        self.main_game.destroy()
    def show_stop(self): #button that terminates the game
        stop = tk.Button(self.main_game, text="Stop", command=self.exit_mainloop, font=self.font, height=1, width=3,bg = BLACK, fg=SHINE_GREEN)
        stop.place(x=435, y=90)

    def show_add(self): #button that trying to add a word to the found word list
        add = tk.Button(self.main_game, text="add",
                        command=lambda path=logic_game.current_word_lst: logic_game.right_word(path),
                        font=self.font, height=1, width=3,bg = BLACK, fg=SHINE_GREEN)
        add.place(x=315, y=90)


    def show_game(self):
        '''
        here all the functions, labels, buttons located on the board.
        '''
        self.set_background()
        self.show_time()
        self.show_score()
        self.show_current_string()
        self.initiate_scrollbar()
        # self.show_hint()
        self.show_start()
        self.show_stop()
        self.show_found_words()
        self.show_found_words_head()
        self.show_add()
        self.show_del()
        self.show_feedback()

    def run(self): #running the game - in the first opening
        self.show_game()
        self.blank_board()
        game.main_game.mainloop()
         # need to be written
    def start_game(self): #when the user is clicking the "start game" button - all the game is starting.
        self.create_board()
        self.run_time()
        self.hint_button()
        self.update_timer_label()

    def create_button(self, i, j): #this function is creating a button of a letter - for the game board.
         return tk.Button(self.show_board,
                          text=self.board[i][j],
                          command=lambda tup=(i,j): self.selected_letter(tup),
                          font=("Calibri", 24), height=1, width=3,
                          bg=BLACK, fg=SHINE_GREEN)

    def com_blank_button(self): #creating blank blacnk space for the initial buttons.
        return ""
    def create_blank_button(self): #creating blank button for the initial board.
        return tk.Button(self.show_board,
                         text="Start the game",
                         command=self.com_blank_button(),
                         font=("Comic Sans MS", 5), height=7, width=14,
                         bg=BLACK,fg= SHINE_GREEN)

    def selected_letter(self, tup): #when the user picked a letter - this function adding it to the cur word.
        x = tup[0]
        y = tup[1]
        letter = self.board[x][y]
        if self.possible_clicks(tup):
            logic_game.current_word += letter
            logic_game.current_word_lst.append(tup)
            self.show_current_string()

    def create_board(self): #creating a shown board of buttons - a board with the letters, after start game.
        board = self.show_board
        self.buttons = []
        for i in range(len(self.board)):
            row = []
            for j in range(len(self.board[0])):
                cur_button = self.create_button(i, j)
                cur_button.grid(row=i, column=j)
                row.append(cur_button)
            self.buttons.append(row)
        board.place(x=20, y=170)
    def blank_board(self): #creating blank board for the initial state of the game.
        board = self.show_board
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                cur_button = self.create_blank_button()
                cur_button.grid(row=i, column=j)
        board.place(x=20, y=170)

    def possible_clicks(self, tup):
        #this function is cheking if the click of the user is possible -
        #means next to the last chosen letter.
        if logic_game.current_word_lst == []:
            return True
        if tup in ex11_utils.corddinate_around(logic_game.current_word_lst[-1], logic_game.board, logic_game.current_word_lst):
            return True
        else:
            return False

if __name__ == '__main__':
    logic_game = BoggleGame()
    game = BoggleGui(logic_game.board)
    game.run()


