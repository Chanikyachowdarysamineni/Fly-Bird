import random
from enum import Enum
from dataclasses import dataclass

import pygame


class PowerUpType(Enum):
    SHIELD = 1
    SLOW_MO = 2
    SCORE_BOOST = 3


@dataclass
class PowerUp:
    """Power-up item"""
    type: PowerUpType
    duration: int  # frames
    x: float = 0
    y: float = 0
    vx: float = -4
    visible: bool = False
    timer: int = 0
    
    # Visual properties
    @property
    def color(self) -> tuple:
        """Get power-up color"""
        colors = {
            PowerUpType.SHIELD: (0, 150, 255),
            PowerUpType.SLOW_MO: (150, 0, 255),
            PowerUpType.SCORE_BOOST: (255, 200, 0),
        }
        return colors.get(self.type, (255, 255, 255))
    
    @property
    def icon(self) -> str:
        """Get power-up icon text"""
        icons = {
            PowerUpType.SHIELD: "⚔",
            PowerUpType.SLOW_MO: "⏱",
            PowerUpType.SCORE_BOOST: "⭐",
        }
        return icons.get(self.type, "✨")
    
    def update(self):
        """Update power-up position"""
        if self.visible:
            self.x += self.vx
            self.timer += 1
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw power-up"""
        if self.visible:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 12)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 10, 2)


class PowerUpManager:
    """Manages power-ups in the game"""
    
    def __init__(self):
        self.active_powerups = {}  # {type: (frames_remaining)}
        self.spawned_powerups = []
    
    def spawn_random_powerup(self, x: float, y: float, chance: float = 0.15):
        """Randomly spawn a power-up"""
        if random.random() < chance:
            putype = random.choice(list(PowerUpType))
            durations = {
                PowerUpType.SHIELD: 300,
                PowerUpType.SLOW_MO: 180,
                PowerUpType.SCORE_BOOST: 240,
            }
            
            pu = PowerUp(
                type=putype,
                duration=durations[putype],
                x=x,
                y=y,
                visible=True
            )
            self.spawned_powerups.append(pu)
    
    def check_collision(self, player_rect) -> list:
        """Check if player collides with any power-ups"""
        collected = []
        for pu in self.spawned_powerups[:]:
            pu_rect = pygame.Rect(pu.x - 12, pu.y - 12, 24, 24)
            if player_rect.colliderect(pu_rect):
                self.activate_powerup(pu.type)
                collected.append(pu.type)
                self.spawned_powerups.remove(pu)
        return collected
    
    def activate_powerup(self, putype: PowerUpType):
        """Activate a power-up effect"""
        durations = {
            PowerUpType.SHIELD: 300,
            PowerUpType.SLOW_MO: 180,
            PowerUpType.SCORE_BOOST: 240,
        }
        self.active_powerups[putype] = durations[putype]
    
    def deactivate_powerup(self, putype: PowerUpType):
        """Deactivate a power-up"""
        if putype in self.active_powerups:
            del self.active_powerups[putype]
    
    def update(self):
        """Update all power-ups"""
        # Update spawned power-ups
        for pu in self.spawned_powerups[:]:
            pu.update()
            # Remove if off-screen
            if pu.x < -50:
                self.spawned_powerups.remove(pu)
        
        # Decrement active power-up timers
        for putype in list(self.active_powerups.keys()):
            self.active_powerups[putype] -= 1
            if self.active_powerups[putype] <= 0:
                self.deactivate_powerup(putype)
    
    def is_active(self, putype: PowerUpType) -> bool:
        """Check if a power-up is active"""
        return putype in self.active_powerups
    
    def get_remaining_time(self, putype: PowerUpType) -> int:
        """Get remaining time for a power-up in frames"""
        return self.active_powerups.get(putype, 0)
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw all power-ups"""
        for pu in self.spawned_powerups:
            pu.draw(screen, font)
    
    def clear(self):
        """Clear all power-ups"""
        self.active_powerups.clear()
        self.spawned_powerups.clear()
