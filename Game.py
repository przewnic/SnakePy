# Author: przewnic

from PyQt5.QtCore import QObject, pyqtSignal
from random import randint

from Snake import Snake
from Fruit import Fruit


class Game(QObject):
    draw_snake = pyqtSignal(int, int)
    draw_fruit = pyqtSignal(int, int)
    delete_item = pyqtSignal(int, int)
    update_score = pyqtSignal(int)
    game_over = pyqtSignal()

    def __init__(self, board, timer):
        super().__init__()
        self.board = board
        self.timer = timer
        self.snake = None
        self.fruit = None
        self.wrapping = False

    def init_game(self):
        self.snake = self.create_snake()
        self.fruit = self.create_fruit()

    def create_snake(self):
        """ Create the initial snake at (0,0). """
        position = self.random_position()
        while position in [o[0] for o in self.board.obstacles]:
            position = self.random_position()
        snake = Snake(position)
        self.draw_snake.emit(*position)
        return snake

    def create_fruit(self):
        """
            Create the fruit on board in place where
            there is no snake.
        """
        position = self.random_position()
        while position in self.snake.coordinates or\
                position in [o[0] for o in self.board.obstacles]:
            position = self.random_position()
        self.draw_fruit.emit(*position)
        return Fruit(position)

    def random_position(self):
        """ Find random position on board. """
        rows = int(self.board.height/self.board.field_size)
        columns = int(self.board.width/self.board.field_size)
        x = randint(0, columns-1)
        y = randint(0, rows-1)
        return (x*self.board.field_size, y*self.board.field_size)

    def check_no_space(self):
        """ Check if all field are taken by the snake and obstacles. """
        fields_taken_by_snake = 0
        if self.snake:
            fields_taken_by_snake = len(self.snake.coordinates)
        obstacle_number = len(self.board.obstacles)
        board_fields = self.board.height/self.board.field_size * self.board.width/self.board.field_size
        if (fields_taken_by_snake + obstacle_number) >= board_fields:
            return True
        return False

    def play(self):
        """
            Move the snake and check if collided with walls.
            Snake can eat the fruit and then gets longer.
        """
        old_tail, head = self.snake.move(self.board, self.wrapping)
        # Draw new head after moving the snake
        self.draw_snake.emit(*head)
        # Check if head is on fruit position
        self.check_eating(head, old_tail)
        self.update_score.emit(len(self.snake.coordinates))
        # End game if snake collided
        if self.check_collision(head):
            self.game_over.emit()
            return
        # Check all fields taken by snake + obstacles
        if self.check_no_space():
            self.game_over.emit()
        return

    def update_direction(self, new_direction):
        self.snake.direction = new_direction

    def check_eating(self, head, old_tail):
        if head == self.fruit.position:
            self.delete_item.emit(*self.fruit.position)
            self.fruit = self.create_fruit()
            self.snake.eat(old_tail)
        else:
            self.delete_item.emit(*old_tail)

    def check_collision(self, head):
        return self.check_borders(head) or self.check_obstacles(head)

    def check_borders(self, head):
        # Checks if head if beyond board
        if head[0] > self.board.width - self.board.field_size or head[0] < 0:
            return True
        if head[1] > self.board.height - self.board.field_size or head[1] < 0:
            return True
        return False

    def check_obstacles(self, head):
        if head in [o[0] for o in self.board.obstacles]:
            return True
        return False
