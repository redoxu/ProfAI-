import pygame
import sys
import fonc4 as fonctio4
import fonctionnalite5 as fonctio5
import fonctionnalite6 as fonctio6
import grid_2048 as fonctio1
from pygame.locals import *
import time


def update_grid():
    for row in range(n):
        for col in range(n):
            # Définir le rectangle
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Dessin du contour

            # Texte à afficher
            
            pygame.draw.rect(screen, TILE_COLORS[grid[row][col]][0], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            text = font.render(theme_dict[grid[row][col]], True, TILE_COLORS[grid[row][col]][1])

            # Calcul de la position pour centrer le texte dans le rectangle
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    # Mise à jour de l'affichage
    pygame.display.flip()
# Initialisation de Pygame
THEMES = {"0": {"name": "Default", 0: "", 2: "2", 4: "4", 8: "8", 16: "16", 32: "32", 64: "64", 128: "128", 256: "256", 512: "512", 1024: "1024", 2048: "2048", 4096: "4096", 8192: "8192"}, 
          "1": {"name": "Chemistry", 0: "", 2: "H", 4: "He", 8: "Li", 16: "Be", 32: "B", 64: "C", 128: "N", 256: "O", 512: "F", 1024: "Ne", 2048: "Na", 4096: "Mg", 8192: "Al"}, 
          "2": {"name": "Alphabet", 0: "", 2: "A", 4: "B", 8: "C", 16: "D", 32: "E", 64: "F", 128: "G", 256: "H", 512: "I", 1024: "J", 2048: "K", 4096: "L", 8192: "M"}
          }
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
GRAY=(200,200,200)
RED =(255,0,0)
GREEN=(0,255,0)


pygame.init()
screen_size =(400,300)
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 36)  # Police par défaut, taille 36

run = True
afficher=["Entrer la taille de votre grille","","choisir le thème","Théme par défault","Chimie","Alphabets"] #textes à afficher
colors=[GREEN,GRAY,GREEN,GRAY,GRAY,GRAY]  #coleurs des rectangles
liste_rect=[]

#afficher l'iterface dans l'etat initiale et initialisation de theme et la fonction d'entrée de text
for i in range(6):
    liste_rect += [pygame.Rect(0, 50*i, 400, 50)]
    pygame.draw.rect(screen, colors[i] , liste_rect[i])
    pygame.draw.rect(screen, BLACK, liste_rect[i], 1)
    text = font.render(afficher[i], True, BLACK)
    text_rect = text.get_rect(center=liste_rect[i].center)
    screen.blit(text, text_rect) 
text_entry_activated =False    
theme='0' 
#boucle des évenments  
while run :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            if liste_rect[1].collidepoint(event.pos) :
                text_entry_activated = True
            elif liste_rect[3].collidepoint(event.pos) :
                theme ='0'
                colors=[GREEN,GRAY,GREEN,RED,GRAY,GRAY]
            elif liste_rect[4].collidepoint(event.pos) :
                theme ='1'
                colors=[GREEN,GRAY,GREEN,GRAY,RED,GRAY]
            elif liste_rect[5].collidepoint(event.pos) :
                theme ='2'
                colors=[GREEN,GRAY,GREEN,GRAY,GRAY,RED]
                
        elif event.type == KEYDOWN :
            if text_entry_activated: 
                if event.key == K_BACKSPACE:
                    afficher[1] = afficher[1][:-1]
                elif event.key == K_RETURN:
                    text_entry_activated = False
                else :
                    afficher[1] += event.unicode
            else:
                if event.key == K_RETURN:
                    run = False
    if text_entry_activated: #changer la couleur de la case du text
        colors[1]=RED
    else:
         colors[1]=GRAY
    #affichages des changments            
    for i in range(6):
        pygame.draw.rect(screen, colors[i] , liste_rect[i])
        pygame.draw.rect(screen, BLACK, liste_rect[i], 1)
        text = font.render(afficher[i], True, BLACK)
        text_rect = text.get_rect(center=liste_rect[i].center)
        screen.blit(text, text_rect)                    
    pygame.display.flip()           
try:
    size = int(afficher[1])       
except:
    size =4

pygame.quit()


#on sort avec le thème et la taille de grille






#Le jeu commence ici

pygame.init()

# Dimensions de la fenêtre et de la grille
n = size # Nombre de lignes et de colonnes
cell_size = 100  # Taille d'une cellule (en pixels)
screen_size = n * cell_size  # Taille de la fenêtre (carrée)
theme_dict = THEMES[theme]


# Création de la fenêtre
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("2048")

# Police pour le texte
font = pygame.font.Font(None, 36)  # Police par défaut, taille 36


grid = fonctio1.init_game(n)
update_grid()
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
                    update_grid()
                    time.sleep(0.1)
                    grid = fonctio1.grid_add_new_tile(grid)
                    update_grid()
            elif event.key == K_RIGHT:
                if fonctio5.move_possible_move(grid,'right'):
                    grid = fonctio4.move_grid(grid,'right')
                    update_grid()
                    time.sleep(0.1)
                    grid = fonctio1.grid_add_new_tile(grid)
                    update_grid()
            elif event.key == K_UP:
                if fonctio5.move_possible_move(grid,'up'):
                    grid = fonctio4.move_grid(grid,'up')
                    update_grid()
                    time.sleep(0.1)
                    grid = fonctio1.grid_add_new_tile(grid)
                    update_grid()
            elif event.key == K_DOWN:
                if fonctio5.move_possible_move(grid,'down'):
                    grid = fonctio4.move_grid(grid,"down")
                    update_grid()
                    time.sleep(0.1)
                    grid = fonctio1.grid_add_new_tile(grid)
                    update_grid()
                
            

    

pygame.quit()
sys.exit()
