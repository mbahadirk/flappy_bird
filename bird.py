import pygame
class Bird:
    def __init__(self,birdHeight,birdWidth,fallVelocity):
        self.birdHeight = birdHeight
        self.birdWidth = birdWidth
        self.fallVelocity = fallVelocity
        self.bird_image = pygame.image.load('images/bird.png')
        self.bird_image = pygame.transform.scale(self.bird_image, (60, 60))  # transform your img
    def drawBird(self,screen,rotationAngle):
        rotatedBird = pygame.transform.rotate(self.bird_image, rotationAngle)
        screen.blit(rotatedBird, (self.birdWidth, self.birdHeight))

