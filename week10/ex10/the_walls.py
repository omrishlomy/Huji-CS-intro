
class Wall:
    def __init__(self, direction,center_coordinates, length=3):
        self.length = length
        self.direction = direction
        self.center = center_coordinates
        self.coordinates = self.wall_coordinates()


    def wall_coordinates(self):
        column, row = self.center
        if self.direction in ['Left', 'Right']:
            coordinates_lst = [(x, row) for x in range(column-1, column+2)]

        elif self.direction in ['Up', 'Down']:
            coordinates_lst = [(column, y) for y in range(row - 1, row + 2)]

        return coordinates_lst

    def move(self):
        if self.direction == "Left":
            self.center = self.center[0]-1, self.center[1]
            self.coordinates = self.wall_coordinates()
            return self.coordinates[-1]

        elif self.direction == "Right":
            self.center = self.center[0] + 1, self.center[1]
            self.coordinates = self.wall_coordinates()
            return self.coordinates[-1]

        elif self.direction == "Up":
            self.center = self.center[0], self.center[1] + 1
            self.coordinates = self.wall_coordinates()
            return self.coordinates[-1]

        elif self.direction == "Down":
            self.center = self.center[0], self.center[1] - 1
            self.coordinates = self.wall_coordinates()
            return self.coordinates[-1]





