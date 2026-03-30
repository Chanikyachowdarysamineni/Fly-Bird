from enum import Enum
from dataclasses import dataclass


class GameDifficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


@dataclass
class DifficultyConfig:
    """Difficulty-specific game parameters"""
    pipe_gap: int
    pipe_speed: int
    player_vel_y: int
    gravity: float
    max_vel_y: int
    name: str
    color: tuple  # RGB for display


# Define difficulty presets - Tuned for realistic, smooth gameplay
DIFFICULTY_CONFIGS = {
    GameDifficulty.EASY: DifficultyConfig(
        pipe_gap=170,           # Generous gap
        pipe_speed=4,           # Slow pipe movement
        player_vel_y=-9,        # Strong flap force
        gravity=0.55,           # Gentle gravity
        max_vel_y=11,           # Max fall speed
        name="EASY",
        color=(34, 197, 94)     # Green from professional palette
    ),
    GameDifficulty.MEDIUM: DifficultyConfig(
        pipe_gap=130,           # Standard gap
        pipe_speed=5,           # Normal speed
        player_vel_y=-9.5,      # Standard flap
        gravity=0.65,           # Balanced gravity
        max_vel_y=12,           # Standard max fall
        name="MEDIUM",
        color=(251, 146, 60)    # Orange from professional palette
    ),
    GameDifficulty.HARD: DifficultyConfig(
        pipe_gap=110,           # Tight gap
        pipe_speed=6.5,         # Fast pipes
        player_vel_y=-10.5,     # Strong flap needed
        gravity=0.8,            # Heavy gravity
        max_vel_y=13,           # Fast fall speed
        name="HARD",
        color=(239, 68, 68)     # Red from professional palette
    ),
}


class GameMode(Enum):
    NORMAL = 1
    SURVIVAL = 2  # Limited lives


@dataclass
class GameState:
    """Store current game state"""
    difficulty: GameDifficulty = GameDifficulty.MEDIUM
    mode: GameMode = GameMode.NORMAL
    score: int = 0
    lives: int = 3
    has_shield: bool = False
    slow_motion_active: bool = False
    slow_motion_timer: int = 0
    score_multiplier: float = 1.0
