from Grid import Grid
from Blocks import *
import random
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.currentBlock = self.getRandomBlock()
        self.nextBlock = self.getRandomBlock()
        self.gameState = False
        self.gameOver = False
        self.hardMode = False
        self.score = 0
        self.highScore = 0
        self.volume = 1
        self.sliderPosition = 475
        self.dropSpeed = 500
        self.rotateSound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clearSound = pygame.mixer.Sound("Sounds/clear.ogg")
        self.moveSound = pygame.mixer.Sound("Sounds/lateralmove.ogg")
        self.gameOverSound = pygame.mixer.Sound("Sounds/game-over.ogg")
        self.dropSound = pygame.mixer.Sound("Sounds/drop.ogg")
        self.selectSound = pygame.mixer.Sound("Sounds/select.ogg")
        self.mainThemeSound = "Sounds/theme.ogg"
        self.hardThemeSound = "Sounds/hardmode.ogg"
        
        # play music
        pygame.mixer.music.load(self.mainThemeSound)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume)

    # Update score based on cleared lines
    def updateScore(self, linesCleared, moveDownPoints):
        if(linesCleared == 1):
            self.score += 100
        elif(linesCleared == 2):
            self.score += 300
        elif(linesCleared == 3):
            self.score += 500
        elif(linesCleared == 4):
            self.score += 800
        elif(linesCleared == 5):
            self.score += 1000
        self.score += moveDownPoints

    # Function to get a random block
    def getRandomBlock(self):
        # If the list is empty, refill it
        if(len(self.blocks) == 0):
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]

        # Remove the random block from the list, so it doesn't appear more than once in one cycle
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        
        return block    # Return the block
    
    # To move the block to the left
    def moveLeft(self):
        self.currentBlock.move(0, -1)   

        # If after the move the block is outside the grid or collides with other block, undo the move
        if(not self.blockInside() or not self.blockFits()): 
            self.currentBlock.move(0, 1)
        else:   # If the move is valid, play the sound
            self.moveSound.play()
    
    # To move the block to the right
    def moveRight(self):
        self.currentBlock.move(0, 1)

        # If after the move the block is outside the grid or collides with other block, undo the move
        if(not self.blockInside() or not self.blockFits()):
            self.currentBlock.move(0, -1)
        else:   # If the move is valid, play the sound
            self.moveSound.play()

    # To move the block to the bottom
    def moveDown(self, auto):
        self.currentBlock.move(1, 0)

        # If after the move the block is outside the grid or collides with other block, undo the move and lock the block position
        if(not self.blockInside() or not self.blockFits()):
            self.currentBlock.move(-1, 0)
            self.lock_block()
            self.dropSound.set_volume(self.volume)
            self.dropSound.play()   # Play the drop sound
        else:   # If the move is valid and it is the user who moves the block down (not the system), play the sound
            if(not auto):
                self.dropSound.set_volume(self.volume)
                self.moveSound.play()

    # Lock the block
    def lock_block(self):
        tiles = self.currentBlock.getCellPos()

        # Mark every grid of the cells of the block on the screen 
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.currentBlock.id
        self.currentBlock = self.nextBlock  # Set the current block to the next block
        self.nextBlock = self.getRandomBlock()  # Generates new block for the next block
        rowsCleared = self.grid.clearFullRows()   # Clear the rows that are full and store the numbers of rows that are cleared

        if(rowsCleared > 0):
            self.clearSound.play()  # Play the cleared sound when there is at least 1 row can be cleeared
            self.updateScore(rowsCleared, 0)    # Update the score

        # If right after spawning new block, the block cant fit to the screen, game over
        if(not self.blockFits()):   
            self.gameOver = True
            self.gameOverSound.play()
            pygame.mixer.music.stop()


    # To reset the game
    def reset(self):
        self.grid.reset()   # Reset the grid
        
        # Update the blocks list, and set the current block and the next block to a random block, and set the score to 0
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.currentBlock = self.getRandomBlock()
        self.nextBlock = self.getRandomBlock()
        self.score = 0

       # Adjust drop speed and music based on game mode
        if (self.hardMode):
            pygame.mixer.music.load(self.hardThemeSound)
            self.dropSpeed = 150
        else:
            pygame.mixer.music.load(self.mainThemeSound)
            self.dropSpeed = 500

        # Replay the theme song infinitely
        pygame.mixer.music.play(-1)

    # Check for collisions
    def blockFits(self):
        tiles = self.currentBlock.getCellPos()
        for tile in tiles:  # Iterates all the cells position
            if(not self.grid.isEmpty(tile.row, tile.col)):  # If the current tile is not empty return false
                return False
        return True # If all the tiles are empty return true

    # To rotate the block
    def rotate(self):
        self.currentBlock.rotate()

        # If after the rotation the block will be out of range and collides with other blocks, undo it
        if(not self.blockInside() or not self.blockFits()): 
            self.currentBlock.undoRotation()
        else:
            self.rotateSound.play()

    # To check whether the block is outside the screen or not
    def blockInside(self):
        tiles = self.currentBlock.getCellPos()
        for tile in tiles:  # Iterates all the tiles 
            if(not self.grid.isInside(tile.row, tile.col)): # If the current cell is outside of the screen, return false 
                return False
        return True # If all the cells are inside the screen, return true

    # Function to draw the game
    def draw(self, screen):
        self.grid.draw(screen)
        self.currentBlock.draw(screen, 11, 11)

        if(self.nextBlock.id == 3): # If the next block is IBlock, give its own offset
            self.nextBlock.draw(screen, 255, 290)
        elif(self.nextBlock.id == 4): # If the next block is OBlock, give its own offset
            self.nextBlock.draw(screen, 255, 280)
        else:   # If it is other block, set the offset to the default offset
            self.nextBlock.draw(screen, 270, 270)