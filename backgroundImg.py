from loaders import load_level
from Application import create_window
from EventHandler import EventHandler

def main():
    create_window()
    level = load_level(input("-> "), EventHandler())
    drag = float(input("-> "))
    
    grid = level.compositor.layers["BackgroundLayer"].grid
    
    tile_size = level.compositor.layers["BackgroundLayer"].spritesheet.tile_size
    
    x = len(grid.grid)
    y = -1
    
    for col in grid.grid:
        if len(col) > y:
            y = len(col)
            
    print(f"x: {x * tile_size/drag}, y: {y * tile_size/drag}")
            
    
     
    
    
if __name__ == "__main__":
    main()
    