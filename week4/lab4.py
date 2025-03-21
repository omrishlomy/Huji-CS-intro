player_1 = True
plater_2 = False
def init_board():
    board = [4,4,4]
    return board
def get_next_player():
    player_turn = 0
    if player_turn % 2 ==0:
        player_1 = True
        player_2 = False
        print("player 1 turn")
    else:
        player_2 = True
        player_1 = False
        print("player 2 turn")
    player_turn+=1
def print_board(board):
    print(update_board(board))
def is_board_empty(board):
    if board == [0, 0, 0]:
        print("game over")
        if player_1 == True:
            print("the winner is player 1")
        if player_2 == True:
            print("the winner is player 2")
            return True
    else:
        return False
def get_input():
    heap = input("insert number of heap")
    number_to_take = input("insert number to take")
    return (heap, number_to_take)

def check_row_number_valadility(int):
    if int <= len(update_board()) and update_board()[int] != 0:
        return True
    else:
        return False
def check_amount_taken(int):
    if int <= update_board()[int]:
        return True
    else:
        print("not enough matches in the heap")
        return False
def update_board(board):

    heap, amount = get_input()
    board[int(heap)] = board[int(heap)] - int(amount)
    return board
def run_game():
    board = init_board()
    while is_board_empty(board) == False:
        print_board(board)
        get_next_player()
    if player1_turn == True:
        print("The winner is player 1")
    else:
        print("The winner is player 2")
run_game()



