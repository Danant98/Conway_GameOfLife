#!/usr/bin/env python

__author__ = 'Daniel Elisabethsønn Antonsen'

# Import libraries and 
import pygame
import numpy as np

# Game of Life class object
class GL:

    # FPS
    FPS = 60

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

    def event_handler(self, events:list):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                col = m_pos[0] // self.TILE_SIZE
                row = m_pos[1] // self.TILE_SIZE
                pos = (col, row)

                # Checking if pos in pos
                if pos in self.positions:
                    self.positions.remove(pos)
                else:
                    self.positions.add(pos)

    def draw_grid(self, positions:set):
        """
        Drawing grid-cells and alive cells
        """
        for pos in positions:
            col, row = pos
            tl = (col * self.TILE_SIZE, row * self.TILE_SIZE)
            pygame.draw.rect(self.screen, self.GOLDEN, (*tl, self.TILE_SIZE, self.TILE_SIZE))
        
        for row in range(self.GRID_HEIGHT):
            pygame.draw.line(self.screen, self.BLACK, (0, row * self.TILE_SIZE), (self.WIDTH, row * self.TILE_SIZE))
        for col in range(self.GRID_WIDTH):
            pygame.draw.line(self.screen, self.BLACK, (col * self.TILE_SIZE, 0), (col * self.TILE_SIZE, self.HEIGHT))


    def get_neighbors(self, positions:set):
        pass

    def run(self):
        """
        Method for running Conway's Game of Life
        """
        clock = pygame.time.Clock()
        
        while self.running:
            # Setting max fps 
            clock.tick(self.FPS)
            
            # Handeling events
            self.event_handler(pygame.event.get())
            
            # Background color
            self.screen.fill(self.GREY)
            self.draw_grid(self.positions)

            # Updating screen
            pygame.display.update()
            
            


