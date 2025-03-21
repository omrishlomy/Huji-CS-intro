import copy
from typing import List, Tuple, Iterable, Optional
from boggle_board_randomizer import randomize_board
Board = List[List[str]]
Path = List[Tuple[int, int]]


def create_word_dic():
    words_dic = {}
    with open("boggle_dict.txt", "r") as file:
        lines=file.readlines()
    for line in lines:
        line = line.strip()
        words_dic[line] = len(line)
    return words_dic

#creating words dict as a global argument
# WORD_DICT = create_word_dic()


def get_partly_words():
    partly_words = set()
    for key in WORD_DICT.keys():
        for i in range(1, len(key)+1):
            word = key[:i]
            partly_words.add(word)
    with open("check_dict", "w") as f:
        f.write("\n".join(partly_words ))
    return partly_words
# PARTLY_WORD_DICT = get_partly_words()



def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    '''input: the board game, the list that discribing a ward path, and a dict of words.
    return: None if word in the dict, None else'''
    word_to_check = ""
    for cord in path:
        letter_x = cord[0]
        letter_y = cord[1]
        word_to_check += board[letter_x][letter_y]
    if word_to_check in words:
        return word_to_check

def corddinate_around(cordd, board,path):
    '''
    :param cordd: tuple of the corddinate that we want to check
    :param board: the board that the coordinate in it
    :return: list of the coordinates around that are option for the next step
    '''
    x = cordd[0]
    y = cordd[1]
    corddinates_around =[(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
    width = len(board)
    height = len(board[0])
    possible_moves = []
    # now we checking if all the coordinates around are in the board limits
    for item in corddinates_around:
        item_x = item[0]
        item_y = item[1]
        if not (item_x < 0 or item_x >= width or item_y < 0 or item_y >= height or item in path):
            possible_moves.append(item)
    return possible_moves

def helper_find_n_paths(n: int, board: Board, words: Iterable[str], cordinate, path, path_lst) -> List[Path]:
    if len(path) == n:
        if is_valid_path(board, path, words) and path not in path_lst:
            path_lst.append(path.copy())
        return
    possible_moves = corddinate_around(cordinate,board,path)
    for tup in possible_moves:
        path.append(tup)
        helper_find_n_paths(n, board, words, tup, path,path_lst)
        path.pop(-1)

def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    '''
    input: number - length of the words that we want to get.
    the current board of the game, and the dict of the right words.
    '''
    path_lst = []
    for index in range(len(board)*len(board[0])):
        row = index//len(board)
        col = index % len(board[0])
        helper_find_n_paths(n,board,words,(row,col),[],path_lst)
    return path_lst
# print(find_length_n_paths(8, randomize_board(),create_word_dic()))

def helper_find_words(n: int, board: Board, words: Iterable[str], cordinate, word,path, path_lst) -> List[Path]:
    if len(word) == n:
        if word in words and path not in path_lst:
            path_lst.append(path.copy())
        return
    possible_moves = corddinate_around(cordinate, board, path)
    for tup in possible_moves:
        char = board[tup[0]][tup[1]]
        new_word = word + char
        path.append(tup)
        helper_find_words(n, board, words, tup,new_word,path,path_lst)
        path.pop()


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    path_lst = []
    for index in range(len(board)*len(board[0])):
        row = index//len(board)
        col = index % len(board[0])
        helper_find_words(n,board,words,(row,col),"",[],path_lst)
    return path_lst
# print(find_length_n_words(3,randomize_board(),create_word_dic()))
def sort_path_by_word(board,lst,words):
    """
    input : list ot lists with all the valid paths
    output: a dictionary with words as keys and list of paths as values
    """
    word_dic = {}
    for path in range(len(lst)):
        word = is_valid_path(board,lst[path],words)
        if word in word_dic.keys():
            word_dic[word].append(lst[path])
        else:
            word_dic[word] = [lst[path]]
    return word_dic

def maximize_score_path(dic):
    """
    input: dictionary fromsort_path_by_word
    output: list with longest paths for every word in the dictionary
    """
    max_lst = []
    for key in dic.keys():
        longest_path = max(dic[key],key=len)
        max_lst.append(longest_path)
    return max_lst

def get_longest_word(words):
    """
    gets the value of the longest word in words
    """
    longest_word = 0
    for word in words:
        if len(word) > longest_word:
            longest_word = len(word)
    return longest_word

def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    path_lst = []
    for length in range(get_longest_word(words)+1): #can be modify to the highest value at the original dictionary(longest word)
        possibles_paths = find_length_n_paths(length,board,words)
        dic_word = sort_path_by_word(board,possibles_paths,words)
        max_lst = maximize_score_path(dic_word)
        for path in range(len(max_lst)):
            path_lst.append(max_lst[path])
    return path_lst





