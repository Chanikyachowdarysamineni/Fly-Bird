"""Achievement system for FlapPyBird"""
import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class Achievement:
    """Represents a single achievement"""
    id: str
    name: str
    description: str
    unlocked: bool = False
    unlock_date: str = ""


class AchievementManager:
    """Manages achievements and progress"""
    
    ACHIEVEMENTS = {
        "first_point": Achievement(
            id="first_point",
            name="First Score",
            description="Score your first point"
        ),
        "ten_points": Achievement(
            id="ten_points",
            name="Getting Started",
            description="Score 10 points in a single game"
        ),
        "fifty_points": Achievement(
            id="fifty_points",
            name="Bird Master",
            description="Score 50 points in a single game"
        ),
        "hundred_points": Achievement(
            id="hundred_points",
            name="Century!",
            description="Score 100 points in a single game"
        ),
        "ten_games": Achievement(
            id="ten_games",
            name="Dedicated Player",
            description="Play 10 games"
        ),
        "easy_clear": Achievement(
            id="easy_clear",
            name="Easy Mode",
            description="Score 20 points on Easy difficulty"
        ),
        "medium_clear": Achievement(
            id="medium_clear",
            name="Medium Challenge",
            description="Score 30 points on Medium difficulty"
        ),
        "hard_clear": Achievement(
            id="hard_clear",
            name="Hard Mode Master",
            description="Score 50 points on Hard difficulty"
        ),
        "shield_collector": Achievement(
            id="shield_collector",
            name="Shield Collector",
            description="Use 5 Shield power-ups"
        ),
        "slow_mo_user": Achievement(
            id="slow_mo_user",
            name="Slow Motion Expert",
            description="Use 5 Slow Motion power-ups"
        ),
        "powerup_master": Achievement(
            id="powerup_master",
            name="Power-Up Master",
            description="Collect 20 power-ups total"
        ),
    }
    
    def __init__(self, filepath: str = "achievements.json"):
        self.filepath = filepath
        self.achievements: Dict[str, Achievement] = self._load()
        self._init_missing()
    
    def _init_missing(self):
        """Initialize missing achievements"""
        for ach_id, ach in self.ACHIEVEMENTS.items():
            if ach_id not in self.achievements:
                self.achievements[ach_id] = Achievement(
                    id=ach_id,
                    name=ach.name,
                    description=ach.description,
                    unlocked=False
                )
    
    def _load(self) -> Dict[str, Achievement]:
        """Load achievements from file"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    data = json.load(f)
                    return {
                        ach_id: Achievement(**ach_data)
                        for ach_id, ach_data in data.items()
                    }
            except Exception:
                return {}
        return {}
    
    def save(self) -> None:
        """Save achievements to file"""
        try:
            data = {
                ach_id: asdict(ach)
                for ach_id, ach in self.achievements.items()
            }
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving achievements: {e}")
    
    def unlock(self, achievement_id: str) -> bool:
        """Unlock an achievement. Returns True if newly unlocked"""
        if achievement_id in self.achievements:
            ach = self.achievements[achievement_id]
            if not ach.unlocked:
                ach.unlocked = True
                from datetime import datetime
                ach.unlock_date = datetime.now().isoformat()
                self.save()
                return True
        return False
    
    def is_unlocked(self, achievement_id: str) -> bool:
        """Check if achievement is unlocked"""
        return (achievement_id in self.achievements and 
                self.achievements[achievement_id].unlocked)
    
    def get_unlocked_list(self) -> List[Achievement]:
        """Get list of unlocked achievements"""
        return [ach for ach in self.achievements.values() if ach.unlocked]
    
    def get_total_unlocked(self) -> int:
        """Get count of unlocked achievements"""
        return len(self.get_unlocked_list())
    
    def get_total_achievements(self) -> int:
        """Get total achievement count"""
        return len(self.achievements)
