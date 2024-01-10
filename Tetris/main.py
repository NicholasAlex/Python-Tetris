import pygame, sys
from Game import Game
from Colors import Colors

pygame.init()

largeFont = pygame.Font(None, 70)
titleFont = pygame.Font(None, 40)
secondaryFont = pygame.Font(None, 30)
captionFont = pygame.Font(None, 25)
scoreSurface = titleFont.render("Score", True, Colors.white)
nextSurface = titleFont.render("Next", True, Colors.white)
gameOverSurface = titleFont.render("GAME OVER", True, Colors.white)
restartSurface = secondaryFont.render("PLAY AGAIN", True, Colors.white)
titleSurface = largeFont.render("PYTHON TETRIS", True, Colors.white)
descSurface = titleFont.render("Enjoy the classic game!", True, Colors.white)
selectModeSurface = secondaryFont.render("SELECT GAME MODE", True, Colors.white)
easyModeSurface = titleFont.render("EASY MODE", True, Colors.white)
hardModeSurface = titleFont.render("HARD MODE", True, Colors.white)

clock = pygame.time.Clock()

scoreRect = pygame.Rect(320, 55, 170, 60)
nextRect = pygame.Rect(320, 245, 170, 180)
restartRect = pygame.Rect(320, 515, 170, 40)
easyRect = pygame.Rect(150, 300, 200, 70)
hardRect = pygame.Rect(150, 400, 200, 70)
gameModeRect = pygame.Rect(50, 220, 400, 285)

screen = pygame.display.set_mode((500, 620))    # Create display object screen with the size of 300px x 600px
pygame.display.set_caption("Python Tetris") # Create the title for screen

clock = pygame.time.Clock()  # Controls the game frame rate

game = Game()
keyDownStart = 0
keyDownStop = 0

# Make the block go down each second
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, game.dropSpeed)


# The Game Loop
while(True):
    for event in pygame.event.get():    # Iterates all the event that recognized by the pygame library
        if(event.type == pygame.QUIT):  # If the event is quit event, stop
                pygame.quit()
                sys.exit()
        
        # Events in menu page
        if (not game.gameState):
            # Check for click event
            if (event.type == pygame.MOUSEBUTTONDOWN):
                mousePos = pygame.mouse.get_pos()

                # If easy mode button was clicked
                if easyRect.collidepoint(mousePos):
                    game.gameState = True
                    game.hardMode = False
                    game.dropSpeed = 500
                    game.selectSound.play()
                    game.reset()
                    pygame.time.set_timer(GAME_UPDATE, game.dropSpeed)

                # If hard mode button was clicked
                if hardRect.collidepoint(mousePos):
                    game.gameState = True
                    game.hardMode = True
                    game.dropSpeed = 150
                    game.selectSound.play()
                    game.reset()
                    pygame.time.set_timer(GAME_UPDATE, game.dropSpeed)
        else:   # Events in game page
            if(event.type == pygame.KEYDOWN): 
                if(game.gameOver):
                    game.gameOver = False
                    game.reset()

                if(event.key == pygame.K_LEFT and not game.gameOver):  # If the user click the left arrow, move to left
                    game.moveLeft()
                elif(event.key == pygame.K_RIGHT and not game.gameOver):  # If the user click the right arrow, move to the right
                    game.moveRight()
                elif(event.key == pygame.K_DOWN and not game.gameOver):   # If the user click the down arrow, move to the bottom
                    game.moveDown(0)
                    game.updateScore(0, 1) # Update the score when the user presses the down key
                elif(event.key == pygame.K_UP) and not game.gameOver: # If the user click the up arrow, rotate the block
                    game.rotate()
            
            if(event.type == GAME_UPDATE and not game.gameOver):  # The block constantly goes down every 1 second
                game.moveDown(1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and not game.gameOver:
                    keyDownStart = pygame.time.get_ticks()
                    pygame.time.set_timer(GAME_UPDATE, 50)  # Decrease time interval when down key is pressed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN and not game.gameOver:
                    keyDownStop = pygame.time.get_ticks()
                    duration = keyDownStop - keyDownStart
                    score = duration // 50 - 1
                    game.updateScore(0, score)
                    pygame.time.set_timer(GAME_UPDATE, game.dropSpeed) # Reset time interval when down key is released

            if (event.type == pygame.MOUSEBUTTONDOWN and game.gameOver): # Restart game functionality
                mousePos = pygame.mouse.get_pos()
                if restartRect.collidepoint(mousePos):
                    game.gameOver = False
                    game.selectSound.play()

                    game.reset()
                    pygame.time.set_timer(GAME_UPDATE, game.dropSpeed)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Check left mouse button click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check if the mouse click is within the slider range
                    if 320 <= mouse_x <= 475 and 585 <= mouse_y <= 605:
                        game.sliderPosition = mouse_x
                        game.volume = (game.sliderPosition - 320) / 170
                        pygame.mixer.music.set_volume(game.volume)

    # Drawing in menu page
    if (not game.gameState):
        screen.fill(Colors.darkBlue)
        pygame.draw.rect(screen, Colors.lightBlue, gameModeRect, 0, 10)
        screen.blit(titleSurface, (50, 90, 50, 50))
        screen.blit(descSurface, (100, 160, 50, 50))
        screen.blit(selectModeSurface, (145, 255, 50, 50))

        # Easy button drawing
        easyText = easyModeSurface.get_rect(center=easyRect.center)
        pygame.draw.rect(screen, (65, 105, 225), easyRect, 0, 10)
        screen.blit(easyModeSurface, easyText.topleft)

        # Hard button drawing
        hardText = hardModeSurface.get_rect(center=hardRect.center)
        pygame.draw.rect(screen, (65, 105, 225), hardRect, 0, 10)
        screen.blit(hardModeSurface, hardText.topleft)
    else: # Drawing in game page
        # Render text
        scoreValueSurface = titleFont.render(str(game.score), True, Colors.white)
        highScoreValueSurface = captionFont.render(f"Highscore: {str(game.highScore)}", True, Colors.white)

        # Draw final result
        screen.fill(Colors.darkBlue)   
        screen.blit(scoreSurface, (365, 20, 50, 50))
        screen.blit(nextSurface, (375, 210, 50, 50))
        screen.blit(highScoreValueSurface, (350, 135, 50, 50))
        
        # Handle cases for game over
        if(game.gameOver):
            # Saving highscore
            if (game.highScore < game.score):
                game.highScore = game.score
                highScoreValueSurface = captionFont.render(f"Highscore: {str(game.highScore)}", True, Colors.white)

            # Draw high score value and game over text
            screen.blit(highScoreValueSurface, (350, 135, 50, 50))        
            screen.blit(gameOverSurface, (320, 470, 50, 50))

            # Show play again
            text_rect = restartSurface.get_rect(center=restartRect.center)
            
            pygame.draw.rect(screen, Colors.lightBlue, restartRect, 0, 10)
            screen.blit(restartSurface, text_rect.topleft)
        
        # Draw score value
        pygame.draw.rect(screen, Colors.lightBlue, scoreRect, 0, 10)
        screen.blit(scoreValueSurface, scoreValueSurface.get_rect(centerx = scoreRect.centerx, centery = scoreRect.centery))
        pygame.draw.rect(screen,Colors.lightBlue, nextRect, 0, 10)
        game.draw(screen)

        # Draw audio slider
        pygame.draw.rect(screen, Colors.white, pygame.Rect(320, 590, 170, 10))  # Example bar
        pygame.draw.rect(screen, Colors.lightBlue, pygame.Rect(game.sliderPosition, 585, 10, 20))  # Example slider

    pygame.display.update() # Update the display
    clock.tick(60)  # Set the frame rate to 60 fps