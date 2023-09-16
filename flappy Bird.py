import pygame
import sys
import random
import pygame.mixer
from bird import Bird

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()

# window size
windowWidth = 600
windowHeight = 900

# images
bottomPipeImage = pygame.image.load('images/bottom_pipe.png')
bottomPipeImage = pygame.transform.scale(bottomPipeImage, (70, 1000))
upperPipeImage  = pygame.image.load('images/upper_pipe.png')
upperPipeImage  = pygame.transform.scale(upperPipeImage, (70, 1000))
backgroundImage = pygame.image.load('images/background.jpg')


# background list
imgWidth = 1715
backgroundX = 0

# sound effects
scoreSound = pygame.mixer.Sound('sounds/point.wav')
wingSound = pygame.mixer.Sound('sounds/wing.wav')
hitSound = pygame.mixer.Sound('sounds/hit.wav')

# colors
grassColor = (0, 255 , 50)
skyColor = (0, 150, 255)
pipeColor = (0, 128, 0)
cloudColor = (240,240,240)

# window initialize
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Flappy Bird")

# bird
bird = Bird(windowHeight/2,50,0)
rotationAngle = 0
rotationSpeed = 2

# pipe
pipeWidth = 100
pipeGap = 200
pipeList = []

# score
score = 0
font = pygame.font.Font(None, 36)
bestScore = -1

# flags
pipeFlag = False
hitFlag = False

# game settings
run = True
gameVelocity = 4
alive = True
intro = True
def startScreen():
    global score
    startText = font.render("press space to jump" , True, (0, 0, 0))
    screen.blit(startText, (windowWidth/2 - windowWidth/6 - 50,windowHeight/2-100))


def drawScore():
    global score
    scoreText = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(scoreText, (windowWidth / 2 - 50, 10), )

def checkPipeCollision():
    global bird, pipeList
    for pipe in pipeList:
        if bird.birdWidth + 40 > pipe[0] and bird.birdWidth < pipe[0] + pipeWidth:
            if bird.birdHeight < pipe[1] or bird.birdHeight + 40 > pipe[1] + pipeGap:
                return True
    return False

def gameOverScreen():
    global score
    gameOverText = font.render("Game Over" , True, (0, 0, 0),(180,180,180))
    scoreText = font.render("Your Score is "+str(score), True,(0,0,0),(180,180,180))
    bestScoreText = font.render("Your Best Score is "+str(bestScore), True,(0,0,0),(180,180,180))

    screen.blit(gameOverText, (windowWidth/2 - windowWidth/6,windowHeight/2-100))
    screen.blit(scoreText, (windowWidth/2 - windowWidth/6 - 20,windowHeight/2-50))
    screen.blit(bestScoreText, (windowWidth/2 - windowWidth/6 - 50,windowHeight/2))

# reset all variables
def resetGame():
    global alive, score,gameVelocity,pipeList,hitFlag,backgroundX,rotationAngle
    rotationAngle = 0
    backgroundX = 0
    alive = True
    score = 0
    gameVelocity = 4
    bird.birdHeight = windowHeight / 2
    pipeList = []
    hitFlag = False

# introduction for game
while intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                intro = False
    screen.blit(backgroundImage, (backgroundX, 0))
    screen.blit(backgroundImage, (backgroundX + imgWidth, 0))

    backgroundSpeed = gameVelocity * 0.1
    backgroundX -= backgroundSpeed
    if backgroundX <= -imgWidth:
        backgroundX = 0
    bird.drawBird(screen, rotationAngle)
    startScreen()

    pygame.display.update()
    clock.tick(60)


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                wingSound.play()
                rotationAngle += rotationSpeed * 40  # for rotate bird while jump
                bird.fallVelocity = -10
                if not alive:
                    resetGame()

    bird.fallVelocity += 0.5
    bird.birdHeight += bird.fallVelocity

    # bird rotation
    rotationAngle -= rotationSpeed
    rotationAngle = max(-30, min(rotationAngle, 45))    # limit rotation Angle

    # draw background
    screen.blit(backgroundImage, (backgroundX, 0))
    screen.blit(backgroundImage, (backgroundX + imgWidth, 0))

    backgroundSpeed = gameVelocity*0.1
    backgroundX -= backgroundSpeed
    if backgroundX <= -imgWidth:
        backgroundX = 0


    # creating pipes
    if len(pipeList) < 1:
        pipeY = random.randint(100, windowHeight - 100 - pipeGap)
        pipeList.append([windowWidth, pipeY])
        pipeFlag = False

    # pipe move and draw
    for pipe in pipeList:
        upper_pipe_image = pygame.transform.scale(upperPipeImage, (pipeWidth, pipe[1]))
        bottomPipeImage = pygame.transform.scale(bottomPipeImage, (pipeWidth, windowHeight -pipe[1]))

        screen.blit(upper_pipe_image, (pipe[0], 0))  # bottom pipe
        screen.blit(bottomPipeImage, (pipe[0], pipe[1] + pipeGap))  # upper pipe

        pipe[0] -= gameVelocity

        if pipe[0] < -pipeWidth:
            pipeList.remove(pipe)

        if pipe[0] < -bird.birdWidth + 150:
            if not pipeFlag:
                score += 1
                scoreSound.play()
                pipeFlag = True

    # draw the bird
    bird.drawBird(screen, rotationAngle)


    # check pipe collision
    if checkPipeCollision():
        alive = False
        if hitFlag == False:
            hitSound.play()
            hitFlag = True


    # check ground collision
    if bird.birdHeight > windowHeight - 40:
        alive = False
        if hitFlag == False:
            hitSound.play()
            hitFlag = True

    # check alive or dead
    if alive == False:
        # check bestscore
        if score > bestScore:
            bestScore = score
        gameVelocity = 0
        gameOverScreen()

    # draw the score
    else:
        drawScore()

    pygame.display.update()
    clock.tick(60)
