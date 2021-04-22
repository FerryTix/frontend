import pygame
import pathlib

base_path = (pathlib.Path(__file__).parent / "resources").absolute()
oxygen96 = pygame.font.Font(base_path / "Oxygen-Sans-Book.otf", 96)
oxygen72 = pygame.font.Font(base_path / "Oxygen-Sans-Book.otf", 72)
oxygen64 = pygame.font.Font(base_path / "Oxygen-Sans-Book.otf", 64)
oxygen54 = pygame.font.Font(base_path / "Oxygen-Sans-Book.otf", 54)  # Bold font has sizing problems
oxygen48 = pygame.font.Font(base_path / "Oxygen-Sans-Book.otf", 48)
oxygen36 = pygame.font.Font(base_path / "Oxygen-Sans-Book.otf", 36)
oxygen24 = pygame.font.Font(base_path / "Oxygen-Sans-Book.otf", 24)
