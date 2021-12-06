# Author: przewnic

class Board():
    def __init__(self, scene, field_size=25):
        self.scene = scene
        self.field_size = field_size
        self.width = 500
        self.height = 500

        self.create_fileds()

        self.obstacles = []

    def create_fileds(self):
        # Add horizontal lines
        for position in range(int(self.height/self.field_size)+1):
            self.scene.addLine(
                0, position*self.field_size,
                self.width, position*self.field_size
                )
        # Add vertical lines
        for position in range(int(self.width/self.field_size)+1):
            self.scene.addLine(
                position*self.field_size, 0,
                position*self.field_size, self.height
                )
