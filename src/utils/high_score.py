import json
import os
from dataclasses import dataclass, asdict


@dataclass
class ScoreData:
    player_name: str = "Player"
    high_score: int = 0
    best_streak: int = 0
    total_plays: int = 0
    total_score: int = 0
    
    @property
    def average_score(self) -> float:
        if self.total_plays == 0:
            return 0
        return self.total_score / self.total_plays


class HighScoreManager:
    """Manages high score persistence"""
    
    def __init__(self, filepath: str = "highscores.json"):
        self.filepath = filepath
        self.data = self._load()
    
    def _load(self) -> ScoreData:
        """Load high score from file"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    raw_data = json.load(f)
                    return ScoreData(**raw_data)
            except Exception:
                return ScoreData()
        return ScoreData()
    
    def save(self) -> None:
        """Save high score to file"""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(asdict(self.data), f, indent=2)
        except Exception as e:
            print(f"Error saving high score: {e}")
    
    def update_score(self, score: int) -> bool:
        """Update high score. Returns True if new record"""
        is_new_record = score > self.data.high_score
        
        if is_new_record:
            self.data.high_score = score
        
        self.data.total_plays += 1
        self.data.total_score += score
        
        if score > self.data.best_streak:
            self.data.best_streak = score
        
        self.save()
        return is_new_record
    
    def get_stats(self) -> dict:
        """Get all statistics"""
        return {
            'player': self.data.player_name,
            'high_score': self.data.high_score,
            'best_streak': self.data.best_streak,
            'total_plays': self.data.total_plays,
            'average_score': round(self.data.average_score, 2)
        }
