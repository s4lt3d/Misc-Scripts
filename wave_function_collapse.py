import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import random
from PIL import Image


# Define the grid
grid_size = (40,40)
tile_size = 3

# init basic tiles


def create_tiles(tile, rotations=4):
    tiles = []
    for _ in range(rotations):
        tiles.append(tile)
        tile = np.rot90(tile)
    return tiles

tile_size = 3

tile_variants = [
    (np.array([[0, 0, 0], [1, 1, 1], [0, 1, 0]]), 4),
    (np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]]), 2),
    (np.array([[0, 0, 0], [0, 1, 1], [0, 1, 0]]), 4),
    (np.array([[0, 1, 0], [2, 2, 2], [0, 1, 0]]), 2),
    (np.array([[0, 0, 0], [2, 2, 2], [0, 0, 0]]), 2),
    (np.array([[0, 0, 0], [0, 2, 2], [0, 2, 0]]), 4),
    (np.array([[0, 2, 0], [1, 1, 1], [0, 2, 0]]), 2),
]

tiles = []
blank = np.zeros((tile_size, tile_size))
tiles.append(blank)

for tile_variant, rotations in tile_variants:
    tiles.extend(create_tiles(tile_variant, rotations))
    
    

# init the image grid
grid = np.zeros((grid_size[1]*tile_size, grid_size[0]*tile_size))

# init the valid tiles
grid_tiles = [[[x for x in range(len(tiles))] for i in range(grid_size[1])] for j in range(grid_size[0])]
   

finished = False

frame = 0
 
while not finished:
    frame += 1
    finished = True
    reduced = False
    grid_next = [[[] for i in range(grid_size[1])] for j in range(grid_size[0])]
        
    lowest_i = 0
    lowest_j = 0
    lowest_entropy = 999

    
    for i in range(len(grid_tiles)):
        for j in range(len(grid_tiles[i])):
            
            if len(grid_tiles[i][j]) == 1:
                grid_next[i][j] = grid_tiles[i][j]
                continue
            
            
            # check top
            
            top_compatible = set()
            if i-1 >= 0:
                top_tiles = grid_tiles[i-1][j]
            else:
                top_tiles = [0]

            if len(top_tiles) == len(tiles):
                top_compatible.update(grid_tiles[i][j])
            elif len(grid_tiles) == len(tiles):
                top_compatible.update(top_tiles)
            else:
                for t in top_tiles:
                    for g in grid_tiles[i][j]:
                        if np.array_equal(tiles[t][-1], tiles[g][0]):
                            top_compatible.add(g)
                  
            # check bottom        
            
            bottom_compatible = set()
            if i+1 < len(grid_tiles):
                bottom_tiles = grid_tiles[i+1][j]
            else:
                bottom_tiles = [0]
                
            
            if len(bottom_tiles) == len(tiles):
                bottom_compatible.update(grid_tiles[i][j])
            elif len(grid_tiles) == len(tiles):
                bottom_compatible.update(bottom_tiles)
            else:
                for t in bottom_tiles:
                    for g in grid_tiles[i][j]:
                        if np.array_equal(tiles[t][0], tiles[g][-1]):
                            bottom_compatible.add(g)
            
            # check left
            
            left_compatible = set()
            if j-1 >= 0:
                left_tiles = grid_tiles[i][j-1]
            else:
                left_tiles = [0]
                
            
            if len(left_tiles) == len(tiles):
                left_compatible.update(grid_tiles[i][j])
            elif len(grid_tiles) == len(tiles):
                left_compatible.update(left_tiles)
            else:
                for t in left_tiles:
                    for g in grid_tiles[i][j]:
                        if np.array_equal(tiles[t][:,-1], tiles[g][:, 0]):
                            left_compatible.add(g)
            
            # check right
            
            right_compatible = set()
            if j+1 < len(grid_tiles[i]):
                right_tiles = grid_tiles[i][j+1]
            else:
                right_tiles = [0]
            
            if len(right_tiles) == len(tiles):
                right_compatible.update(grid_tiles[i][j])
            elif len(grid_tiles) == len(tiles):
                right_compatible.update(right_tiles)
            else:
                for t in right_tiles:
                    for g in grid_tiles[i][j]:
                        if np.array_equal(tiles[t][:,0], tiles[g][:,-1]):
                            right_compatible.add(g)
        
                
            result = top_compatible & bottom_compatible & left_compatible & right_compatible
            
            grid_next[i][j] = list(result)
            
            if np.array_equal(grid_next[i][j], grid_tiles[i][j]) == False:
                reduced = True
            
            
            if len(result) > 1:
                finished = False
            

            
    grid_tiles = grid_next.copy()
    
    
    for i in range(len(grid_tiles)):
        for j in range(len(grid_tiles[i])):
            if len(grid_tiles[i][j]) == 1:
                continue
            if lowest_entropy >= len(grid_tiles[i][j]):
                lowest_entropy = len(grid_tiles[i][j])
                lowest_i = i
                lowest_j = j
    
    if len( grid_tiles[lowest_i][lowest_j]) > 1 and reduced == False:
        grid_tiles[lowest_i][lowest_j] = [random.choice(grid_tiles[lowest_i][lowest_j])]
 
    
    
    # Plot! 
    if frame %30 == 0:
        for i in range(len(grid_tiles)):
            for j in range(len(grid_tiles[i])):
                ti, tj = i * tile_size, j * tile_size
                if len(grid_tiles[i][j]) == 1: 
                    grid[ti:ti+tile_size, tj:tj+tile_size] = tiles[grid_tiles[i][j][0]]
                else:
                    grid[ti:ti+tile_size, tj:tj+tile_size] = blank
        
        
        # Define the color map
        colors = ['blue', 'green', 'red']
        cmap = mcolors.ListedColormap(colors)
        
        # Plot the grid
        plt.imshow(grid, cmap=cmap, interpolation='nearest')
        plt.colorbar(ticks=[0, 1, 2])
        plt.show()
        


for i in range(len(grid_tiles)):
    for j in range(len(grid_tiles[i])):
        ti, tj = i * tile_size, j * tile_size
        if len(grid_tiles[i][j]) == 1: 
            grid[ti:ti+tile_size, tj:tj+tile_size] = tiles[grid_tiles[i][j][0]]
        else:
            grid[ti:ti+tile_size, tj:tj+tile_size] = blank


# Define the color map
colors = ['blue', 'green', 'red']
cmap = mcolors.ListedColormap(colors)

# Plot the grid
plt.imshow(grid, cmap=cmap, interpolation='nearest')
plt.colorbar(ticks=[0, 1, 2])
plt.show()


