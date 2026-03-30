"""
Game Progression System - Realistic and adaptive gameplay
Handles:
- Progressive difficulty scaling
- Adaptive score checkpoints
- Dynamic lives system
- Game ending conditions
- Realistic game pacing
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class GameProgressionMode(Enum):
    """Different game progression strategies"""
    ARCADE = "arcade"      # Traditional endless mode
    STORY = "story"        # Story-driven with chapters
    SURVIVAL = "survival"  # Lives-based mode
    SANDBOX = "sandbox"    # Player-defined goals


@dataclass
class ProgressionConfig:
    """Configuration for games with different goals"""
    mode: GameProgressionMode
    starting_lives: int
    base_score_multiplier: float
    pipe_speed_progression: float  # Speed increase per level
    pipe_gap_reduction: float  # Gap decrease per level
    checkpoint_interval: int  # Points between checkpoints
    max_score_goal: Optional[int]  # Target score to beat (None = endless)
    max_lives_goal: Optional[int]  # "Lives Challenge": try to keep all lives
    time_based_scaling: bool  # Does difficulty scale with time?
    description: str


# Pre-configured game progression styles
PROGRESSION_CONFIGS = {
    GameProgressionMode.ARCADE: ProgressionConfig(
        mode=GameProgressionMode.ARCADE,
        starting_lives=3,
        base_score_multiplier=1.0,
        pipe_speed_progression=0.08,  # 8% speed increase per checkpoint
        pipe_gap_reduction=0.02,  # 2% gap reduction per checkpoint
        checkpoint_interval=10,  # Checkpoint every 10 points
        max_score_goal=None,  # Endless
        max_lives_goal=None,
        time_based_scaling=True,
        description="Classic endless arcade mode. Score as high as you can!"
    ),
    GameProgressionMode.STORY: ProgressionConfig(
        mode=GameProgressionMode.STORY,
        starting_lives=5,
        base_score_multiplier=1.2,
        pipe_speed_progression=0.05,  # Slower progression for story
        pipe_gap_reduction=0.01,
        checkpoint_interval=15,  # Longer checkpoints
        max_score_goal=200,  # Complete story at 200 points
        max_lives_goal=None,
        time_based_scaling=False,
        description="Story mode: Reach 200 points while enjoying the journey."
    ),
    GameProgressionMode.SURVIVAL: ProgressionConfig(
        mode=GameProgressionMode.SURVIVAL,
        starting_lives=1,
        base_score_multiplier=2.0,  # Double points for hardcore
        pipe_speed_progression=0.12,  # Faster progression
        pipe_gap_reduction=0.04,  # Tighter gaps
        checkpoint_interval=5,  # Frequent checkpoints (intense!)
        max_score_goal=150,  # Win at 150 points with 1 life
        max_lives_goal=None,
        time_based_scaling=True,
        description="Hardcore survival: One life, no room for mistakes."
    ),
    GameProgressionMode.SANDBOX: ProgressionConfig(
        mode=GameProgressionMode.SANDBOX,
        starting_lives=10,
        base_score_multiplier=1.0,
        pipe_speed_progression=0.04,  # Very slow for exploration
        pipe_gap_reduction=0.005,
        checkpoint_interval=20,
        max_score_goal=None,  # Player-defined in-game
        max_lives_goal=None,
        time_based_scaling=False,
        description="Sandbox mode: Relax and explore at your own pace."
    ),
}


class GameProgressionSystem:
    """Manages game progression, difficulty scaling, and game ending"""
    
    def __init__(self, config: ProgressionConfig):
        self.config = config
        self.starting_lives = config.starting_lives
        self.current_level = 1
        self.score_checkpoints_passed = 0
        self.time_elapsed_frames = 0
        self.peak_score = 0
        
        # Difficulty scaling factors (start at 1.0)
        self.pipe_speed_multiplier = 1.0
        self.pipe_gap_multiplier = 1.0
        self.score_multiplier = config.base_score_multiplier
        
        # Dynamic difficulty based on performance
        self.performance_factor = 1.0  # Scales from 0.8 to 1.2 based on player skill
        
    def update(self, current_score: int, lives: int, frame_count: int):
        """Update progression based on game state"""
        self.time_elapsed_frames = frame_count
        self.peak_score = max(self.peak_score, current_score)
        
        # Calculate progression level based on score
        new_level = 1 + (current_score // self.config.checkpoint_interval)
        
        if new_level > self.current_level:
            self.current_level = new_level
            self.score_checkpoints_passed += 1
            return True  # Level up occurred
        return False
    
    def should_increase_difficulty(self, current_score: int, lives: int) -> bool:
        """Determine if difficulty should increase"""
        if self.config.mode == GameProgressionMode.SANDBOX:
            return False  # Sandbox doesn't scale
        
        # Time-based scaling
        if self.config.time_based_scaling and self.time_elapsed_frames > 0:
            time_minutes = self.time_elapsed_frames / (30 * 60)  # Convert frames to minutes
            if time_minutes > self.current_level * 0.5:
                return True
        
        # Score-based scaling
        expected_checkpoint = (current_score // self.config.checkpoint_interval)
        if expected_checkpoint > self.current_level:
            return True
        
        return False
    
    def get_current_difficulty_multiplier(self) -> tuple[float, float]:
        """Get current pipe speed and gap multipliers"""
        progression = self.score_checkpoints_passed
        
        speed_mult = 1.0 + (progression * self.config.pipe_speed_progression)
        gap_mult = max(0.6, 1.0 - (progression * self.config.pipe_gap_reduction))  # Min 60% gap
        
        # Apply performance factor
        speed_mult *= self.performance_factor
        
        return speed_mult, gap_mult
    
    def get_score_points(self, base_points: int = 1) -> int:
        """Get actual points based on multipliers and difficulty"""
        level_bonus = 1 + (self.score_checkpoints_passed * 0.05)  # 5% per level
        return int(base_points * self.score_multiplier * level_bonus)
    
    def check_game_ending_condition(self, current_score: int, lives: int) -> Optional[str]:
        """Check if game should end and return reason"""
        # Endless mode - only ends on 0 lives
        if self.config.mode == GameProgressionMode.ARCADE:
            if lives <= 0:
                return "arcade_endless"
            return None
        
        # Story mode - reach goal score while alive
        if self.config.mode == GameProgressionMode.STORY:
            if current_score >= self.config.max_score_goal:
                return "story_complete"
            if lives <= 0:
                return "story_failed"
            return None
        
        # Survival mode - reach goal with 1 life
        if self.config.mode == GameProgressionMode.SURVIVAL:
            if current_score >= self.config.max_score_goal:
                return "survival_victory"
            if lives <= 0:
                return "survival_failed"
            return None
        
        # Sandbox - player controls the goal
        if self.config.mode == GameProgressionMode.SANDBOX:
            if lives <= 0:
                return "sandbox_ended"
            return None
        
        return None
    
    def get_game_end_message(self, end_reason: str) -> tuple[str, str]:
        """Get end screen message and description"""
        messages = {
            "arcade_endless": ("GAME OVER", "You played well! Try again to beat your score."),
            "story_complete": ("STORY COMPLETE", "You conquered the journey! Well done!"),
            "story_failed": ("STORY FAILED", "Try again to complete the story."),
            "survival_victory": ("SURVIVAL VICTORY!", "You survived the odds! True champion!"),
            "survival_failed": ("SURVIVAL FAILED", "One chance, one mistake. Try again."),
            "sandbox_ended": ("SESSION ENDED", "Thank you for playing in sandbox mode!"),
        }
        return messages.get(end_reason, ("GAME OVER", "Game ended."))
    
    def get_progression_stats(self) -> dict:
        """Get detailed progression statistics"""
        speed_mult, gap_mult = self.get_current_difficulty_multiplier()
        
        return {
            "mode": self.config.mode.value,
            "current_level": self.current_level,
            "score_checkpoints": self.score_checkpoints_passed,
            "speed_multiplier": round(speed_mult, 2),
            "gap_multiplier": round(gap_mult, 2),
            "performance_factor": round(self.performance_factor, 2),
            "time_elapsed_seconds": self.time_elapsed_frames / 30,
            "goal_score": self.config.max_score_goal or "∞",
            "starting_lives": self.starting_lives,
        }
    
    def adapt_to_player_skill(self, current_score: int, lives: int):
        """dynamically adjust difficulty based on player performance"""
        if self.time_elapsed_frames < 600:  # First 20 seconds - assess player
            return
        
        # Calculate player skill: score per minute
        minutes_played = self.time_elapsed_frames / (30 * 60)
        score_per_minute = current_score / max(minutes_played, 0.1)
        
        # Adjust difficulty based on performance
        if score_per_minute > 5:  # Player is doing great
            self.performance_factor = min(1.2, self.performance_factor + 0.01)  # Increase difficulty
        elif score_per_minute < 1:  # Player is struggling
            self.performance_factor = max(0.8, self.performance_factor - 0.01)  # Decrease difficulty
        else:
            # Reset to normal
            self.performance_factor = max(0.8, min(1.2, self.performance_factor * 0.98))
