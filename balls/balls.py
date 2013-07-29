import pygame
from lumino import Lumino

resolution = (1024, 768)
pygame.init()
screen = pygame.display.set_mode(resolution)


while True:
    screen.fill((0, 0, 0))
    l = Lumino('/dev/ttyUSB0') 
    ra, rb = l.get()
    pygame.draw.circle(screen, (255, 0, 0), (300, 300), ra/2, 0)
    pygame.draw.circle(screen, (0, 255, 0), (700, 300), rb/2, 0)
    pygame.display.update()
