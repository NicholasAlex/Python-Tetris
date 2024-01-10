from Colors import Colors
from Position import Position
import pygame

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cellSize = 30
        self.rowOffset = 0
        self.colOffset = 0
        self.rotationState = 0
        self.colors = Colors.getCellColors()

    # Move the block according the offset
    def move(self, rows, cols):
        self.rowOffset += rows
        self.colOffset += cols
    
    # Return the cell position
    def getCellPos(self):
        tiles = self.cells[self.rotationState]
        movedTiles = [] # List to store all the cell positions

        for position in tiles:  # Iterates all the cells, and appends it to the list
            position = Position(position.row + self.rowOffset, position.col + self.colOffset)
            movedTiles.append(position)
        return movedTiles   # Return the list

    # To rotate the block
    def rotate(self):
        self.rotationState += 1 # Increment the rotation state by 1
        if(self.rotationState == len(self.cells)):  # If it is the last rotation state, change it to 0
            self.rotationState = 0

    # To cancel a rotation
    def undoRotation(self):
        self.rotationState -= 1 # Decrement the rotation state by 1
        if(self.rotationState == -1):   # If the decrement resulting in -1, change it to 0
            self.rotationState = len(self.cells) - 1

    # To draw the block in the screen
    def draw(self, screen, offsetX, offsetY):
        tiles = self.getCellPos()
        for tile in tiles:
            tileRect = pygame.Rect(offsetX + tile.col * self.cellSize, offsetY + tile.row * self.cellSize, self.cellSize - 1, self.cellSize - 1)
            pygame.draw.rect(screen, self.colors[self.id], tileRect)