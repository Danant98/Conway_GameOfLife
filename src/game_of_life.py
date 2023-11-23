#!/usr/bin/env python

__author__ = 'Daniel Elisabethsønn Antonsen'

# Import libraries and 
import pygame, sys, random

# Game of Life class object
class GL:

    # FPS and update frequency
    FPS = 60
    UPDATE_FREQ = 60

    # Width and height of screen
    WIDTH, HEIGHT = 800, 600

    # Tile size
    TILE_SIZE = 20

    # Grid width and height
    GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE

    # Colors as rgb values
    GREY, BLACK, GOLDEN = (128, 128, 128), (0, 0, 0), (255, 185, 15)

    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Defining variables 
        self.running = True
        self.pause = False
        self.positions = set()

        # Defining screeen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.count = 0
    
    def random_position(self, num_of_cells:int):
        """
        Initialize random position for alive cells
        """
        return set([
                    (random.randrange(0, self.GRID_WIDTH), 
                     random.randrange(0, self.GRID_HEIGHT)) for _ in range(num_of_cells)
                ])

    def event_handler(self, events:list):
        """
        Event handler
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                col = m_pos[0] // self.TILE_SIZE
                row = m_pos[1] // self.TILE_SIZE
                pos = (col, row)

                # Checking if pos in set of positions
                if pos in self.positions:
                    self.positions.remove(pos)
                else:
                    self.positions.add(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                
                if event.key == pygame.K_c:
                    # Resetting grid
                    self.positions = set()
                    self.pause = True
                    self.count = 0
                
                if event.key == pygame.K_g:
                    self.positions = self.random_position(random.randrange(4, 10) * self.GRID_WIDTH)
                
    def draw_grid(self, positions:set):
        """
        Drawing grid-cells and alive cells
        """
        for pos in positions:
            col, row = pos
            tl = (col * self.TILE_SIZE, row * self.TILE_SIZE)
            pygame.draw.rect(self.screen, self.GOLDEN, (*tl, self.TILE_SIZE, self.TILE_SIZE))
        
        for row in range(self.GRID_HEIGHT):
            pygame.draw.line(self.screen, self.BLACK, (0, row * self.TILE_SIZE), 
                             (self.WIDTH, row * self.TILE_SIZE))
        for col in range(self.GRID_WIDTH):
            pygame.draw.line(self.screen, self.BLACK, (col * self.TILE_SIZE, 0), 
                             (col * self.TILE_SIZE, self.HEIGHT))


    def adjust_grid(self, positions:set):
        """
        Finding neighbors of alive grid-cells
        """
        set_neighbors = set()
        new_pos = set()

        for pos in positions:
            neighbors = self.get_neighbors(pos)
            set_neighbors.update(neighbors)

            neighbors = list(filter(lambda x: x in self.positions,  neighbors))

            if len(neighbors) in [2, 3]:
                new_pos.add(pos)
        
        for pos in set_neighbors:
            neighbors = self.get_neighbors(pos)
            neighbors = list(filter(lambda x: x in self.positions, neighbors))

            if len(neighbors) == 3:
                new_pos.add(pos)
        
        return new_pos


    def get_neighbors(self, positions:set):
        """
        Adjusting the grid based on alive cells
        """
        x, y = positions
        neighbors = []
        for dx in [-1, 0, 1]:
            if x + dx < 0 or x + dx > self.GRID_WIDTH:
                continue
            for dy in [-1, 0, 1]:
                if y + dy < 0 or y + dy > self.GRID_WIDTH:
                    continue
                if dx == 0 and dy == 0:
                    continue
                neighbors.append((x + dx, y + dy))
        
        return neighbors


    def run(self):
        """
        Method for running Conway's Game of Life
        """
        clock = pygame.time.Clock()
        
        while self.running:
            # Setting max fps 
            clock.tick(self.FPS)

            if not self.pause:
                self.count += 1
            
            if self.count >= self.UPDATE_FREQ:
                self.count = 0
                self.positions = self.adjust_grid(self.positions)
                
            # Handeling events
            self.event_handler(pygame.event.get())

            # Setting caption
            pygame.display.set_caption('Playing' if not self.pause else 'Paused')
            
            # Background color
            self.screen.fill(self.GREY)
            self.draw_grid(self.positions)

            # Updating screen
            pygame.display.update()
        
        # Close pygame and system
        pygame.quit()
        sys.exit()