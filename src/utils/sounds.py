import sys
import os

import pygame


def get_asset_path(relative_path: str) -> str:
    """Get correct asset path for both development and PyInstaller builds."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    return os.path.join(base_path, relative_path)


class Sounds:
    die: pygame.mixer.Sound
    hit: pygame.mixer.Sound
    point: pygame.mixer.Sound
    swoosh: pygame.mixer.Sound
    wing: pygame.mixer.Sound

    def __init__(self) -> None:
        if "win" in sys.platform:
            ext = "wav"
        else:
            ext = "ogg"

        self.die = pygame.mixer.Sound(get_asset_path(f"assets/audio/die.{ext}"))
        self.hit = pygame.mixer.Sound(get_asset_path(f"assets/audio/hit.{ext}"))
        self.point = pygame.mixer.Sound(get_asset_path(f"assets/audio/point.{ext}"))
        self.swoosh = pygame.mixer.Sound(get_asset_path(f"assets/audio/swoosh.{ext}"))
        self.wing = pygame.mixer.Sound(get_asset_path(f"assets/audio/wing.{ext}"))
