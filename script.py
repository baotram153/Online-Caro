import pygame
import time

pygame.init()
pygame.display.set_mode((100, 100))

# '''once the key is pressed, keys[pygame.K_UP] will be True until another key is pressed'''
# while True:
#     pygame.event.pump()  # Keeps pygame's event queue updated
#     keys = pygame.key.get_pressed()
#     if (keys[pygame.K_UP]):
#         print("UP")
#     if (keys[pygame.K_DOWN]):
#         print("Down")
#     # print(keys[pygame.K_UP])
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("UP")
            if event.key == pygame.K_DOWN:
                print("Down")
    