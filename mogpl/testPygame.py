#!/usr/bin/env python
# coding: utf-8

import pygame
from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((640, 480))


#Chargement et collage du personnage
perso = pygame.image.load("perso.png").convert()
fenetre.blit(perso, (200,300))

#Rafraîchissement de l'écran
pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
while continuer:
	continuer = int(input())
