import pygame
from Colors import Colors

class Grid:
    # Constructor
    def __init__(self):
        self.numRows = 20
        self.numCols = 10
        self.cellSize = 30
        self.grid = [[0 for j in range(self.numCols)] for i in range(self.numRows)]  # Initialize the grid to 0
        self.colors = Colors.getCellColors()

    # Function to print the grid
    def printGrid(self):
        for row in range(self.numRows):
            for column in range(self.numCols):
                print(self.grid[row][column], end=" ")
            print()

    # To check whether a block is still inside the grid or not
    def isInside(self, row, col):
        # If it is, return true
        if(row >= 0 and row< self.numRows and col >= 0 and col < self.numCols):
            return True
        return False    # If not, return false

    # To check whether the current grid is empty
    def isEmpty(self, row, col):
        if(self.grid[row][col] == 0):
            return True
        return False

    # To check whether a row is full or not
    def isRowFull(self, row):
        for col in range(self.numCols): # Iterates all the row's columns
            if(self.grid[row][col] == 0):   # If there is an empty column, return False
                return False    # If not, return True
        return True

    # To clear a row
    def clearRow(self, row):
        for col in range(self.numCols):
            self.grid[row][col] = 0

    # To move a row down
    def moveRowDown(self, row, numRows):
        # Iterates all the cols of the row and set the (row + numRows)'s col to row's col, then set the row's col to 0
        for col in range(self.numCols):
            self.grid[row + numRows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    # To clear the full rows
    def clearFullRows(self):
        completed = 0   # Set the counter var to 0
        for row in range(self.numRows - 1, 0 , -1): # Iterates all the row from the bottom
            if(self.isRowFull(row)):    # If the current row is ful
                self.clearRow(row)  # Clear the row
                completed += 1  # Increment completed
            elif(completed > 0):    # If completed > 0, move the current row down completed times
                self.moveRowDown(row, completed)
        return completed

    # To reset the grid
    def reset(self):
        for row in range(self.numRows):
            for col in range(self.numCols):
                self.grid[row][col] = 0 # Set all the tiles to 0

    def draw(self, screen):
        # Iterates the grid
        for row in range(self.numRows):
            for col in range(self.numCols):
                cellValue = self.grid[row][col] # Stor the cell value
                cellRect = pygame.Rect(col * self.cellSize + 11, row * self.cellSize + 11, self.cellSize - 1, self.cellSize - 1)  # Draw the grid 
                pygame.draw.rect(screen, self.colors[cellValue], cellRect)  # Draw the rect according to its value