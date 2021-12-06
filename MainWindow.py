# Author: przewnic

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QBrush

from Game import Game
from Board import Board
from MyGraphicsScene import MyGraphicsScene


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Snake")
        self.restart.clicked.connect(self.on_restart)
        self.stop_resume.clicked.connect(self.on_stop_resume)
        self.wrapping.stateChanged.connect(self.on_wrapping)
        self.action_restart.triggered.connect(self.on_restart)
        self.action_clear_board.triggered.connect(self.on_clear_board)

        self.scene = MyGraphicsScene(None)
        self.scene.mouse_hover_pos.connect(self.mouse_moved)
        self.scene.mouse_clicked_pos.connect(self.mouse_clicked)

        self.graphics_view.setScene(self.scene)
        # Set the timer and initial interval
        self.timer = QTimer()
        self.dial.valueChanged.connect(self.on_dial)
        INIT_DIAL_VALUE = 10
        self.dial.setValue(INIT_DIAL_VALUE)
        self.on_dial()
        # Draw and set the board
        self.board = Board(self.scene)
        # Set the scene Rect
        self.scene.setSceneRect(
            0, 0,
            self.board.width,
            self.board.height
            )
        # Create game and connetct signals with slots
        self.game = Game(self.board, self.timer)
        self.game.draw_snake.connect(self.draw_rect)
        self.game.draw_fruit.connect(
            lambda x, y: self.draw_rect(x, y, color=Qt.green)
            )
        self.game.delete_item.connect(self.delte_item)
        self.game.update_score.connect(self.set_score)
        self.game.game_over.connect(self.game_over)
        # Connect timer to game
        self.timer.timeout.connect(self.game.play)
        self.game_end = None  # Simple text item holder, when game over
        self.on_restart()

    def _play(self):
        """ Start the game with timer. """
        self.timer.start()

    def on_restart(self):
        """
            Restart button handler.
            Deletes snake and fruits from the board
            and starts new game.
        """
        self.timer.stop()
        # Clear the board
        if self.game.snake:
            for part in self.game.snake.coordinates:
                self.delte_item(part[0], part[1])
        if self.game.fruit:
            self.delte_item(*self.game.fruit.position)
        if self.game_end:  # Remove 'Game over' info if existed
            self.scene.removeItem(self.game_end)
            self.game_end = None
        # Reset the menu
        self.score.setText("")
        self.stop_resume.setText("Stop")
        # Reset the game
        self.game.init_game()
        # Start new game
        if not self.game_end:
            self._play()

    def set_score(self, value):
        """ Set score label to value. """
        self.score.setText(str(value))

    def draw_rect(self, x, y, color=Qt.red):
        """ Draw red rectangle at given position. """
        item = self.scene.addRect(x, y, self.board.field_size-1,
                                  self.board.field_size-1,
                                  brush=QBrush(color, Qt.SolidPattern))
        return item

    def delte_item(self, x, y):
        """ Deletes Snake parts from given position. """
        items = self.scene.items(QPointF(float(x), float(y)))
        item = None
        if not items:
            return
        for _item in items:
            if _item in [o[1] for o in self.game.board.obstacles]:
                continue
            if isinstance(_item, QtWidgets.QGraphicsRectItem):
                item = _item
        if item:
            self.scene.removeItem(item)

    def keyPressEvent(self, event):
        """ Key pressed event handler. """
        if event.key() == Qt.Key_W:
            self.game.update_direction("UP")
        elif event.key() == Qt.Key_S:
            self.game.update_direction("DOWN")
        elif event.key() == Qt.Key_A:
            self.game.update_direction("LEFT")
        elif event.key() == Qt.Key_D:
            self.game.update_direction("RIGHT")
        elif event.key() == Qt.Key_Space:
            self.on_stop_resume()
        else:
            super(MainWindow, self).keyPressEvent(event)

    def on_dial(self):
        """ Reaction on change of dial. Sets speed of game. """
        BASE_SPEED = 1050
        speed = BASE_SPEED - self.dial.value()
        self.timer.setInterval(speed)
        self.speed.setText(str(BASE_SPEED-speed))

    def game_over(self):
        """ Signal handler - Stops the game and prints string on board. """
        self.timer.stop()
        self.game_end = self.scene.addSimpleText("GAME OVER")

    def mouse_moved(self, pos):
        x, y = pos.x(), pos.y()
        # Check if clicked beyond board
        if x > self.board.width-1 or y > self.board.height-1:
            return
        if x < 0 or y < 0:
            return
        # Get board coordinates
        x = (x // self.board.field_size)*self.board.field_size
        y = (y // self.board.field_size)*self.board.field_size
        # Check if snake is not in this place
        if self.game.snake and (int(x), int(y)) in self.game.snake.coordinates:
            return
        if self.game.fruit and (int(x), int(y)) == self.game.fruit.position:
            return
        # Check if not the same again:
        if (int(x), int(y)) in [o[0] for o in self.board.obstacles]:
            return
        # Draw obstacle
        item = self.draw_rect(x, y, color=Qt.gray)
        self.board.obstacles.append(((int(x), int(y)), item))

    def mouse_clicked(self, pos):
        x, y = pos.x(), pos.y()
        # Check if clicked beyond board
        if x > self.board.width-1 or y > self.board.height-1:
            return
        if x < 0 or y < 0:
            return
        # Get board coordinates
        x = (x // self.board.field_size)*self.board.field_size
        y = (y // self.board.field_size)*self.board.field_size
        # Check if snake is not in this place
        if self.game.snake and (int(x), int(y)) in self.game.snake.coordinates:
            return
        # Check if to delete obstacle
        for i, obstacle in enumerate(self.board.obstacles):
            if (int(x), int(y)) == obstacle[0]:
                _obstacle = self.board.obstacles.pop(i)
                self.scene.removeItem(_obstacle[1])
                return

    def on_stop_resume(self):
        # Check if game ended
        if self.game_end:
            return
        if self.timer.isActive():
            self.timer.stop()
            self.stop_resume.setText("Resume")
            return
        self.timer.start()
        self.stop_resume.setText("Stop")

    def on_wrapping(self):
        """
            Handler of Wrapping checkbox.
            If Wrapping is checked the Snake can go
            through the walls and come out on the other side.
        """
        if not self.game:
            return
        if self.wrapping.isChecked():
            self.game.wrapping = True
            return
        self.game.wrapping = False

    def on_clear_board(self):
        if not self.board.obstacles:
            return
        for o in self.board.obstacles:
            self.scene.removeItem(o[1])
        self.board.obstacles.clear()
