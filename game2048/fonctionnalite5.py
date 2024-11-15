import grid_2048,fonc4

def is_grid_full(grid):
    n=len(grid)
    L=grid_2048.get_all_tiles(grid)
    for i in range(n):
        if L[i] == 0:
            return False
    return True
def move_possible_move(grid,d):
    if fonc4.move_grid(grid,d)!=grid:
        return True
    return False



def move_possible(grid):
    for d in {"left","right","up","down"}:
        if fonc4.move_grid(grid,d)!=grid:
            return True
    return False

def is_game_over(grid):#le jeu est il fini
    if not is_grid_full(grid):
        return False
    return not move_possible(grid)

def get_grid_tile_max(grid):
    max=0
    L=grid_2048.get_all_tiles(grid)
    for k in L:
        if k>max:
            max=k
    return max

def jeu_gagnant(grid):#jeu gagnant?
    if get_grid_tile_max(grid)>=2048:
        return True
    
    
    
    