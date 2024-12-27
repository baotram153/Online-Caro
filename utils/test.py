'''Test KeyboardInterrupt'''
import time

try:
    while True:
        print("Hello, world!")
        time.sleep(1)
except KeyboardInterrupt:
    print("Goodbye!")
    

'''Test Pygame keyboard
- to use pygame.event.get() to get the keys pressed, we have to start a pygame window first
''' 
import pygame

pygame.init()
pygame.display.set_mode((100, 100))

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("UP")
                if event.key == pygame.K_DOWN:
                    print("Down")
except KeyboardInterrupt:
    print("Goodbye!")
    
