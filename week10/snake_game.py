from typing import Optional
from game_display import GameDisplay

class SnakeGame:

    def __init__(self,gb: GameDisplay) -> None:
        self.__x = gd.width//2
        self.__y = gd.height//2
        self.__key_clicked = None
        # self.apples = gd.arg.apples

    def read_key(self, key_clicked: Optional[str])-> None:
        self.__key_clicked = key_clicked

    def update_objects(self)-> None:
        if (self.__key_clicked == 'Left') and (self.__x > 0):
            self.__x -= 1
        elif (self.__key_clicked == 'Right') and (self.__x < 39):
            self.__x += 1
        elif (self.__key_clicked == 'Up') and (self.__y < 29):
            self.__y += 1
        elif (self.__key_clicked == 'Down') and (self.__y > 0):
            self.__y -= 1
    def update_walls(self):
        pass
    def update_apples(self):
        pass

    def draw_board(self, gd: GameDisplay) -> None:
        gd.draw_cell(self.__x, self.__y, "blue")

    def end_round(self) -> None:
        pass

    def is_over(self) -> bool:
        return False