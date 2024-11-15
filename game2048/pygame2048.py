import pygame
import sys
import fonc4 as fonctio4
import fonctionnalite5 as fonctio5
import fonctionnalite6 as fonctio6
import grid_2048 as fonctio1
from pygame.locals import *
# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre et de la grille
n = 4 # Nombre de lignes et de colonnes
cell_size = 100  # Taille d'une cellule (en pixels)
screen_size = n * cell_size  # Taille de la fenêtre (carrée)

# Couleurs
TILE_COLORS = {
    0: ((205, 193, 180), (119, 110, 101)),  # #cdc1b4, #776e65
    2: ((238, 228, 218), (119, 110, 101)),  # #eee4da, #776e65
    4: ((237, 224, 200), (119, 110, 101)),  # #ede0c8, #776e65
    8: ((242, 177, 121), (249, 246, 242)),  # #f2b179, #f9f6f2
    16: ((245, 149, 99), (249, 246, 242)),  # #f59563, #f9f6f2
    32: ((246, 124, 95), (249, 246, 242)),  # #f67c5f, #f9f6f2
    64: ((246, 94, 59), (249, 246, 242)),  # #f65e3b, #f9f6f2
    128: ((237, 207, 114), (249, 246, 242)),  # #edcf72, #f9f6f2
    256: ((237, 204, 97), (249, 246, 242)),  # #edcc61, #f9f6f2
    512: ((237, 200, 80), (249, 246, 242)),  # #edc850, #f9f6f2
    1024: ((237, 197, 63), (249, 246, 242)),  # #edc53f, #f9f6f2
    2048: ((237, 194, 46), (249, 246, 242)),  # #edc22e, #f9f6f2
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("2048")

# Police pour le texte
font = pygame.font.Font(None, 36)  # Police par défaut, taille 36
grid = fonctio1.init_game(n)
# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN :
            if event.key == K_LEFT:
                if fonctio5.move_possible_move(grid,'left'):
                    grid = fonctio4.move_grid(grid,'left')
                    grid = fonctio1.grid_add_new_tile(grid)
            elif event.key == K_RIGHT:
                if fonctio5.move_possible_move(grid,'right'):
                    grid = fonctio4.move_grid(grid,'right')
                    grid = fonctio1.grid_add_new_tile(grid)
            elif event.key == K_UP:
                if fonctio5.move_possible_move(grid,'up'):
                    grid = fonctio4.move_grid(grid,'up')
                    grid = fonctio1.grid_add_new_tile(grid)
            elif event.key == K_DOWN:
                if fonctio5.move_possible_move(grid,'down'):
                    grid = fonctio4.move_grid(grid,"down")
                    grid = fonctio1.grid_add_new_tile(grid)
                
            

    # Remplissage de l'écran
    screen.fill(WHITE)

    # Dessin de la grille avec texte
    for row in range(n):
        for col in range(n):
            # Définir le rectangle
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Dessin du contour

            # Texte à afficher
            if grid[row][col] == 0:
                a = ''
            else:
                a = str(grid[row][col])
            pygame.draw.rect(screen, TILE_COLORS[grid[row][col]][0], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            text = font.render(a, True, TILE_COLORS[grid[row][col]][1])

            # Calcul de la position pour centrer le texte dans le rectangle
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    # Mise à jour de l'affichage
    pygame.display.flip()

pygame.quit()
sys.exit()
