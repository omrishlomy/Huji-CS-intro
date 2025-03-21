import helper


def init_board(rows, columns):
    game_board = []
    for i in range(rows):
        game_board.append([])
        for j in range(columns):
            game_board[i].append(helper.WATER)
    return game_board


def cell_loc(name):
    ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if 3 >= len(name) >= 2 and name[0] in ABC and helper.is_int(name[1:]):
        row_num = int((name.split(name[0])[1])) - 1
        column_num = ord(name[0].upper()) - 65
        return (row_num, column_num)
    else:
        return


def valid_ship(board, size, loc):
    if loc != '\n':
        while 0 <= loc[0] <= helper.NUM_ROWS and 0 <= loc[1] <= helper.NUM_COLUMNS:
            if loc[0] + size <= len(board):
                for j in range(size):
                    if board[j][loc[1]] != helper.WATER:
                        return False
                return True
            return False
    return False
def valid_ship_computer(board,locations, size):
    valid_location = []
    for j in range(len(locations)):
            if locations[j][0] + size <= len(board):
                        valid_location.append(locations[j])
    return valid_location





def create_player_board(rows, columns, ship_sizes):
    new_board = init_board(helper.NUM_ROWS, helper.NUM_COLUMNS)
    helper.print_board(new_board)
    ship = 0
    while ship in range(len(ship_sizes)):
        ship_loc = cell_loc(helper.get_input("Enter ship location placement"))
        while ship_loc is None:
            ship_loc = cell_loc(helper.get_input("Enter ship location placement"))
        if ship_sizes[ship] > len(new_board):
            ship_sizes.discard(ship)
        if valid_ship(new_board, helper.SHIP_SIZES[ship], ship_loc):
            for j in range(ship_sizes[ship]):
                new_board[ship_loc[0] + j][ship_loc[1]] = helper.SHIP
            if ship < len(ship_sizes) - 1:
                helper.print_board(new_board)
            ship += 1
    return new_board


def sum_of_hits(ship_sizes):
    hits = 0
    for i in range(len(ship_sizes)):
        hits += ship_sizes[i]
    return hits


def board_is_empty(board):
    board_empty = 0
    for rows in range(len(board)):
        for columns in range(len(board[rows])):
            if board[rows][columns] == helper.HIT_SHIP:
                board_empty += 1
    if board_empty == sum_of_hits(helper.SHIP_SIZES):
        return True
    else:
        return False


def computer_ship_locations(board, rows, columns):
    locations = []
    for r in range(rows):
        for c in range(columns):
            if board[r][c] == helper.WATER:
                locations.append((r, c))
    return locations
def computer_fire_location(board, rows, columns):
    locations = []
    for r in range(rows):
        for c in range(columns):
            if board[r][c] != helper.HIT_SHIP and board[r][c] != helper.HIT_WATER:
                locations.append((r, c))
    return locations




def create_computer_board(rows, columns, ship_sizes):
    computer_board = init_board(helper.NUM_ROWS, helper.NUM_COLUMNS)
    ship = 0
    while ship in range(len(ship_sizes)):
        valid_locations = valid_ship_computer(computer_board,computer_ship_locations(computer_board, helper.NUM_ROWS, helper.NUM_COLUMNS),ship_sizes[ship])
        ship_loc = helper.choose_ship_location(computer_board, helper.SHIP_SIZES[ship],valid_locations)
        if valid_ship(computer_board, helper.SHIP_SIZES[ship], ship_loc):
            for j in range(ship_sizes[ship]):
                computer_board[ship_loc[0] + j][ship_loc[1]] = helper.SHIP
            ship += 1
    return computer_board


def fire_torpedo(board, loc):
    if board[loc[0]][loc[1]] == helper.SHIP:
        board[loc[0]][loc[1]] = helper.HIT_SHIP
    if board[loc[0]][loc[1]] == helper.WATER:
        board[loc[0]][loc[1]] = helper.HIT_WATER
    return board


def update_board(expose_board, hidden_board, loc):
    if hidden_board[loc[0]][loc[1]] == helper.SHIP:
        hidden_board[loc[0]][loc[1]] = helper.HIT_SHIP
        expose_board[loc[0]][loc[1]] = helper.HIT_SHIP
    else:
        hidden_board[loc[0]][loc[1]] = helper.HIT_WATER
        expose_board[loc[0]][loc[1]] = helper.HIT_WATER
    return hidden_board



def play_again(player_board, computer_board_hidden):
    helper.print_board(player_board, computer_board_hidden)
    yes_no_list = ['Y', 'N']
    if board_is_empty(computer_board_hidden) and board_is_empty(player_board):
        want_to_play = (helper.get_input("Game over, it's a tie, would you like to play again ?"))
        while len(want_to_play) != 1 or want_to_play not in yes_no_list:
            want_to_play = helper.get_input("only Y or N chars ,would you like to play again ?")
    elif board_is_empty(player_board):
        want_to_play = (helper.get_input("Game over. the winner is the computer. would you like to play again ?"))
        while len(want_to_play) != 1 or want_to_play not in yes_no_list:
            want_to_play = helper.get_input("only Y or N chars ,would you like to play again ?")
    else:
        board_is_empty(computer_board_hidden)
        want_to_play = (helper.get_input("Game over, the winner is the player, would you like to play again ?"))
        while len(want_to_play) != 1 or want_to_play not in yes_no_list:
            want_to_play = helper.get_input("only Y or N chars ,would you like to play again ?")
    if want_to_play == 'Y':
        main()
    else:
        return


def valid_location(board, loc):
    if loc:
        if loc[0] < helper.NUM_ROWS and loc[1] < helper.NUM_COLUMNS and board[loc[0]][loc[1]] not in [helper.HIT_WATER,helper.HIT_SHIP]:
            return loc
    else:
        good_fire = False
        while not good_fire:
            loc = cell_loc(helper.get_input("location unvalid, choose another location"))
            if loc:
                if loc[0] < helper.NUM_ROWS and loc[1] < helper.NUM_COLUMNS and board[loc[0]][loc[1]] not in [helper.HIT_WATER, helper.HIT_SHIP]:
                    return loc



def main():
    player_board = create_player_board(helper.NUM_ROWS, helper.NUM_COLUMNS, helper.SHIP_SIZES)
    player_blank_board = init_board(helper.NUM_ROWS, helper.NUM_COLUMNS)
    computer_board_hidden = create_computer_board(helper.NUM_ROWS, helper.NUM_COLUMNS, helper.SHIP_SIZES)
    computer_board_expose = init_board(helper.NUM_ROWS, helper.NUM_COLUMNS)
    helper.print_board(player_board, computer_board_expose)
    while not (board_is_empty(player_board)) and not (board_is_empty(computer_board_expose)):
        loc = valid_location(computer_board_expose,cell_loc(helper.get_input("player's turn, choose location to fire")))
        fire_torpedo(computer_board_expose, loc)
        update_board(computer_board_expose, computer_board_hidden,loc)
        fire_computer_loc = helper.choose_torpedo_target(player_blank_board, computer_fire_location(player_board, helper.NUM_ROWS, helper.NUM_COLUMNS))
        fire_torpedo(player_blank_board, fire_computer_loc)
        update_board(player_blank_board, player_board,fire_computer_loc)
        if not board_is_empty(computer_board_hidden) and not board_is_empty(player_board):
            helper.print_board(player_board, computer_board_expose)
    play_again(player_board, computer_board_hidden)

if __name__ == "__main__":
    main()

