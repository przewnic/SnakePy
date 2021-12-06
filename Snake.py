# Author: przewnic

class Snake():
    def __init__(self, start_point):
        self.coordinates = [start_point]
        self.direction = "DOWN"

    def eat(self, old_tail):
        """ If eats - one part is added. """
        self.coordinates.insert(0, old_tail)

    def _move_wrapping(self, board):
        """ Adds one more field at front of the snake. """
        if self.direction == "DOWN":
            y = self.coordinates[-1][1]+board.field_size
            if y > board.height-board.field_size:
                y = 0
            self.coordinates.append(
                (self.coordinates[-1][0],
                 y)
                )
        elif self.direction == "UP":
            y = self.coordinates[-1][1]-board.field_size
            if y < 0:
                y = board.height - board.field_size
            self.coordinates.append(
                (self.coordinates[-1][0],
                 y)
                )
        elif self.direction == "LEFT":
            x = self.coordinates[-1][0]-board.field_size
            if x < 0:
                x = board.width - board.field_size
            self.coordinates.append(
                (x,
                 self.coordinates[-1][1])
                )
        elif self.direction == "RIGHT":
            x = self.coordinates[-1][0]+board.field_size
            if x > board.width-board.field_size:
                x = 0
            self.coordinates.append(
                (x,
                 self.coordinates[-1][1])
                )
        return self.coordinates[-1]  # Returns head

    def _move(self, board):
        """ Adds one more field at front of the snake. """
        if self.direction == "DOWN":
            self.coordinates.append(
                (self.coordinates[-1][0],
                 self.coordinates[-1][1]+board.field_size)
                )
        elif self.direction == "UP":
            self.coordinates.append(
                (self.coordinates[-1][0],
                 self.coordinates[-1][1]-board.field_size)
                )
        elif self.direction == "LEFT":
            self.coordinates.append(
                (self.coordinates[-1][0]-board.field_size,
                 self.coordinates[-1][1])
                )
        elif self.direction == "RIGHT":
            self.coordinates.append(
                (self.coordinates[-1][0]+board.field_size,
                 self.coordinates[-1][1])
                )
        return self.coordinates[-1]  # Returns head

    def move(self, board, wrapping):
        """ Simulation of snake move. """
        if wrapping:
            new_head = self._move_wrapping(board)
        else:
            new_head = self._move(board)
        old_tail = self.coordinates.pop(0)
        return old_tail, new_head
