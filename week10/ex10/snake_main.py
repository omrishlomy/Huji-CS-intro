import argparse
import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay

def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:

    # INIT OBJECTS
    game = SnakeGame(args)
    gd.show_score(0)
    round_num = 0
    # DRAW BOARD
    game.update_objects(round_num)
    if args.debug == True:
        game.__snake_coordinates = []
    game.draw_board(gd)
    # END OF ROUND 0
    gd.end_round()
    while not game.is_over(gd,round_num,args):
        round_num += 1
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        game.change_direction()

        # UPDATE OBJECTS
        game.update_objects(round_num)
        game.reach_edges()
        # DRAW BOARD
        game.draw_board(gd)
        # WAIT FOR NEXT ROUND:
        # round_num += 1
        game.end_round()
        gd.show_score(game.score)
        gd.end_round()
    # one_round(gd,args,round_num)

def one_round(gd: GameDisplay, args: argparse.Namespace,rounds):
    game.update_objects(rounds)
    game.draw_board(gd)
    rounds+=1
    game.end_round()
    gd.show_score(game.score)
    gd.end_round()

if __name__ == "__main__":
    print("You should run:\n"
          "> python game_display.py")
