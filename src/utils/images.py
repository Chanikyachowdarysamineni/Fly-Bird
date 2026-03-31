import random
import sys
import os
from typing import List, Tuple

import pygame

from .constants import BACKGROUNDS, PIPES, PLAYERS


def get_asset_path(relative_path: str) -> str:
    """Get correct asset path for both development and PyInstaller builds."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    return os.path.join(base_path, relative_path)


class Images:
    numbers: List[pygame.Surface]
    game_over: pygame.Surface
    welcome_message: pygame.Surface
    base: pygame.Surface
    background: pygame.Surface
    player: Tuple[pygame.Surface]
    pipe: Tuple[pygame.Surface]

    def __init__(self) -> None:
        self.numbers = list(
            (
                pygame.image.load(get_asset_path(f"assets/sprites/{num}.png")).convert_alpha()
                for num in range(10)
            )
        )

        # game over sprite
        self.game_over = pygame.image.load(
            get_asset_path("assets/sprites/gameover.png")
        ).convert_alpha()
        # welcome_message sprite for welcome screen
        self.welcome_message = pygame.image.load(
            get_asset_path("assets/sprites/message.png")
        ).convert_alpha()
        # base (ground) sprite
        self.base = pygame.image.load(get_asset_path("assets/sprites/base.png")).convert_alpha()
        self.randomize()

    def randomize(self):
        # select random background sprites
        rand_bg = random.randint(0, len(BACKGROUNDS) - 1)
        # select random player sprites
        rand_player = random.randint(0, len(PLAYERS) - 1)
        # select random pipe sprites
        rand_pipe = random.randint(0, len(PIPES) - 1)

        self.background = pygame.image.load(get_asset_path(BACKGROUNDS[rand_bg])).convert()
        self.player = (
            pygame.image.load(get_asset_path(PLAYERS[rand_player][0])).convert_alpha(),
            pygame.image.load(get_asset_path(PLAYERS[rand_player][1])).convert_alpha(),
            pygame.image.load(get_asset_path(PLAYERS[rand_player][2])).convert_alpha(),
        )
        self.pipe = (
            pygame.transform.flip(
                pygame.image.load(get_asset_path(PIPES[rand_pipe])).convert_alpha(),
                False,
                True,
            ),
            pygame.image.load(get_asset_path(PIPES[rand_pipe])).convert_alpha(),
        )
    
    def set_player_color(self, color_index: int):
        """Set player color by index (0=Red, 1=Blue, 2=Yellow)"""
        if 0 <= color_index < len(PLAYERS):
            player_idx = color_index
            self.player = (
                pygame.image.load(get_asset_path(PLAYERS[player_idx][0])).convert_alpha(),
                pygame.image.load(get_asset_path(PLAYERS[player_idx][1])).convert_alpha(),
                pygame.image.load(get_asset_path(PLAYERS[player_idx][2])).convert_alpha(),
            )
