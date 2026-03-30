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
        pipe_gap=180,           # Very generous gap for learners
        pipe_speed=3.5,         # Slow pace
        player_vel_y=-8.5,      # Lighter flap for control
        gravity=0.50,           # Very gentle gravity
        max_vel_y=10,           # Slower max fall
        name="EASY",
        color=(34, 197, 94)     # Green
    ),
    GameDifficulty.MEDIUM: DifficultyConfig(
        pipe_gap=140,           # Standard gap
        pipe_speed=4.8,         # Moderate speed
        player_vel_y=-9.2,      # Standard flap
        gravity=0.60,           # Balanced gravity - smooth feeling
        max_vel_y=11.5,         # Moderate max fall
        name="MEDIUM",
        color=(251, 146, 60)    # Orange
    ),
    GameDifficulty.HARD: DifficultyConfig(
        pipe_gap=115,           # Tight gap for challenge
        pipe_speed=6.2,         # Fast pipes
        player_vel_y=-10,       # Strong flap needed
        gravity=0.75,           # Heavy gravity
        max_vel_y=13,           # Fast fall speed
        name="HARD",
        color=(239, 68, 68)     # Red
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
