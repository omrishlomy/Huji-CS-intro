import ex11_utils
import boggle_board_randomizer
import random
Dict = ex11_utils.create_word_dic()

class BoggleGame:
    '''
    thit class is representing the logic game. it got all the qulities of the logic game,
     as we will see in the init func. the Gui is getting the logic info out of it.
    '''
    def __init__(self):
        #the game board - every new game got his own new board.
        self.board = boggle_board_randomizer.randomize_board()
        #list of all the words that had already found
        self.found_words = []
        self.score = 0
        #this is the main dict - if the found word is in it, it will excepted.
        self.dict = self.got_dict("boggle_dict.txt")
        #the currnet word that being found at the moment.
        self.current_word = ""
        #the path od the spesific word that being found at the moment.
        self.current_word_lst = []
        #a feedback that shown on the top of the screen
        self.feedback = "WELCOME"



    def word_chek(self, word):
        '''
        :param word: a string of letters that the user picked.
        :return: True if the word is real, False else
        '''
        return word in self.dict

    def word_not_found(self, word):
        '''
        :param word: the found word
        :return: True if the word haven't found yet, False if the word already had found.
        '''
        return word not in self.found_words

    def got_score(self, path):
        '''

        :param path: list of path that creating the word
        updating the scrore in len(path)^2
        :return: None
        '''
        self.score += len(path)**2
        return self.score

    def path_to_word(self, path):
        '''
        :param path: the path - list of coordinates that been chosen by the user
        :return: string - the letters that are in the places of the coords in the board
        '''
        the_word = ""
        the_board = self.board
        for cord in path:
            cord_x = cord[0]
            cord_y = cord[1]
            the_word += the_board[cord_x][cord_y]
        return the_word

    def change_feedback(self):
        '''
        every found word the user got a feedback - changeing by the length of the found word.
        this function is randomize a feedback acordding to the word length.
        '''
        set_3 = ["that's it?", "shhoooorrrtt", "ha,only 9 points", "NO RUSH"]
        set_4 = ["norm", "no special here", "take it easy"]
        set_5 = ["wow wow wow", "impressiveeeee", "yooohooooo!"]
        if self.found_words != []:
            n = len(self.found_words[-1])
            if n == 3:
                self.feedback = random.choice(set_3)
            if n == 4:
                self.feedback = random.choice(set_4)
            if n >= 5:
                self.feedback = random.choice(set_5)

    def print_found_words(self):
        '''
        :return: printing the word as we want them be shown in the found word list.
        '''
        found_words = ""
        if len(self.found_words) != 0:
            for word in self.found_words:
                found_words += word + "\n"
        return found_words

    def right_word(self, path):
        '''
        :param word: string - word
        :param path: list - path of the word
        if the word is right, updating the score and the list of found_words.
        :return: None
        '''
        word = self.path_to_word(path)
        if self.word_chek(self.current_word) and self.word_not_found(self.current_word):
            self.got_score(self.current_word_lst)
            self.found_words.append(self.current_word)
            self.current_word = ""
            self.current_word_lst = []
            self.change_feedback()
        else:
            self.current_word = ""
            self.current_word_lst = []





    def got_dict(self, path):
        '''
        :param url: path in the computer to the list of words
        :return: a dict of the words.
        '''
        words_dic = {}
        with open(path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            words_dic[line] = len(line)
        return words_dic


    def get_random_hint(self):
        '''
        here we creating a list the contain word path or part of a word path -
        that will be shown to the user as a hint.
        :return:the list - path of word or of part of a word - that will be shown to the user as an hint.
        '''
        n = random.choice([1,2,3,4,5,6])
        hints_lst = ex11_utils.find_length_n_paths(n, self.board, Dict)
        if len(hints_lst) != 0:
            random_list = random.choice(hints_lst)
            k = random.choice(range(len(random_list)))
            new_random = random_list[:k]
            return new_random
        else:
            new_random = self.get_random_hint()
            return new_random

    def del_letter(self): #related to the function that delete letter from string
        '''
        deleting a letter from the currnet word - in case of duble letters (QU for example) - deleted both.
        '''
        if self.current_word != "":
            last_tup = self.current_word_lst[-1]
            last_tup_x = last_tup[0]
            last_tup_y = last_tup[1]
            if len(self.board[last_tup_x][last_tup_y]) == 1:
                self.current_word = self.current_word[:-1]
                self.current_word_lst = self.current_word_lst[:-1]
            else:
                self.current_word = self.current_word[:-2]
                self.current_word_lst = self.current_word_lst[:-2]
















