import argparse
import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay
import game_display

def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:

    # INIT OBJECTS
    gb = game_display.GameDisplay(30, 40, 1000, 10,None)
    game = SnakeGame(gb)
    snake1 = Snake(3,"Up",[(5,5),(4,5),(4,5)],gd,"black",None)
    gd.show_score(0)
    # DRAW BOARD
    game.draw_board(gd)
    # END OF ROUND 0
    while not game.is_over():
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        # UPDATE OBJECTS
        game.update_objects()
        # DRAW BOARD
        game.draw_board(gd)
        # WAIT FOR NEXT ROUND:
        game.end_round()
        gd.end_round()

if __name__ == "__main__":
    print("You should run:\n"
          "> python game_display.py")