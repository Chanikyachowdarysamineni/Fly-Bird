"""Tutorial and help system for better user onboarding"""
import pygame
from typing import Tuple


class TutorialScreen:
    """Interactive tutorial showing game controls and tips"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_slide = 0
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.slides = [
            {
                "title": "WELCOME TO FLAPPY BIRD",
                "content": [
                    "This is an enhanced version",
                    "with Tier 1 features!",
                    "",
                    "Complete the tutorial to learn",
                    "how to play.",
                ],
                "color": (100, 200, 255),
            },
            {
                "title": "GOAL",
                "content": [
                    "Pass through pipes without hitting them",
                    "",
                    "Score 1 point for each pipe passed",
                    "",
                    "Survive as long as possible!",
                    "",
                    "You have 3 lives - use them wisely",
                ],
                "color": (100, 255, 150),
            },
            {
                "title": "CONTROLS",
                "content": [
                    "SPACE or CLICK to flap",
                    "TAP screen to jump",
                    "",
                    "P to pause/resume",
                    "S to toggle sound",
                    "ESC to return to menu",
                ],
                "color": (255, 200, 100),
            },
            {
                "title": "GAME FEATURES",
                "content": [
                    "⚙ Customize your game:",
                    "  • Adjust window size",
                    "  • Choose bird color",
                    "  • Set difficulty level",
                    "",
                    "🛡️ Invincibility after collision",
                    "   (4 seconds to recover)",
                ],
                "color": (255, 150, 200),
            },
            {
                "title": "DIFFICULTY LEVELS",
                "content": [
                    "🟢 EASY: Large gaps, slow pipes",
                    "   Perfect for learning",
                    "",
                    "🟠 MEDIUM: Standard difficulty",
                    "   Balanced gameplay",
                    "",
                    "🔴 HARD: Tight gaps, fast pipes",
                    "   For experienced players",
                ],
                "color": (200, 200, 100),
            },
            {
                "title": "ACHIEVEMENTS SYSTEM",
                "content": [
                    "Unlock 11 unique achievements:",
                    "",
                    "🏆 Score milestones (10, 50, 100+)",
                    "🏆 Difficulty achievements",
                    "🏆 Bonus challenge unlocks",
                    "",
                    "Track your progress!",
                ],
                "color": (255, 200, 100),
            },
            {
                "title": "PRO TIPS",
                "content": [
                    "• Tap early to maintain altitude",
                    "• Don't tap too fast",
                    "• Watch bird rotation for speed hints",
                    "• Harder difficulty = faster leveling",
                    "",
                    "Practice makes perfect!",
                ],
                "color": (150, 255, 150),
            },
            {
                "title": "READY TO PLAY?",
                "content": [
                    "You now know the basics!",
                    "",
                    "Choose your difficulty",
                    "and start playing.",
                    "",
                    "Good luck! Have fun!",
                ],
                "color": (100, 200, 255),
            },
        ]
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw current tutorial slide"""
        slide = self.slides[self.current_slide]
        
        # Draw title
        title = self.font_large.render(slide["title"], True, slide["color"])
        title_x = (self.screen_width - title.get_width()) // 2
        screen.blit(title, (title_x, 60))
        
        # Draw content
        y = 150
        for line in slide["content"]:
            if line:
                text = self.font_medium.render(line, True, (200, 200, 200))
                text_x = (self.screen_width - text.get_width()) // 2
                screen.blit(text, (text_x, y))
            y += 50
        
        # Draw slide indicator
        indicator = self.font_small.render(
            f"Slide {self.current_slide + 1} / {len(self.slides)}", 
            True, (150, 150, 150)
        )
        indicator_x = (self.screen_width - indicator.get_width()) // 2
        screen.blit(indicator, (indicator_x, self.screen_height - 80))
        
        # Draw navigation hints
        nav_text = self.font_small.render(
            "← / → to navigate, SPACE to skip", 
            True, (100, 150, 200)
        )
        nav_x = (self.screen_width - nav_text.get_width()) // 2
        screen.blit(nav_text, (nav_x, self.screen_height - 40))
    
    def next_slide(self) -> bool:
        """Move to next slide. Returns False if at end."""
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            return True
        return False
    
    def prev_slide(self) -> bool:
        """Move to previous slide"""
        if self.current_slide > 0:
            self.current_slide -= 1
            return True
        return False
    
    def is_finished(self) -> bool:
        """Check if at last slide"""
        return self.current_slide >= len(self.slides) - 1


class GameStats:
    """Display game statistics and performance metrics"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
    
    def draw_game_over_stats(
        self, 
        screen: pygame.Surface,
        score: int,
        high_score: int,
        player_name: str,
        difficulty: str,
        lives_used: int = 3,
    ) -> None:
        """Draw detailed game over statistics"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw GAME OVER title
        game_over_text = self.font_large.render("GAME OVER", True, (255, 100, 100))
        x = (self.screen_width - game_over_text.get_width()) // 2
        screen.blit(game_over_text, (x, 40))
        
        # Draw player name
        name_text = self.font_medium.render(f"Player: {player_name}", True, (200, 200, 255))
        x = (self.screen_width - name_text.get_width()) // 2
        screen.blit(name_text, (x, 120))
        
        # Draw difficulty
        diff_text = self.font_medium.render(f"Difficulty: {difficulty}", True, (200, 255, 200))
        x = (self.screen_width - diff_text.get_width()) // 2
        screen.blit(diff_text, (x, 170))
        
        # Draw score
        y = 240
        score_label = self.font_medium.render("FINAL SCORE", True, (255, 255, 100))
        x = (self.screen_width - score_label.get_width()) // 2
        screen.blit(score_label, (x, y))
        
        score_value = self.font_large.render(str(score), True, (255, 255, 100))
        x = (self.screen_width - score_value.get_width()) // 2
        screen.blit(score_value, (x, y + 50))
        
        # Draw high score if new record
        y += 120
        if score == high_score:
            record_text = self.font_medium.render("🏆 NEW HIGH SCORE! 🏆", True, (255, 200, 0))
            x = (self.screen_width - record_text.get_width()) // 2
            screen.blit(record_text, (x, y))
        else:
            high_score_text = self.font_small.render(
                f"Best Score: {high_score}", 
                True, (150, 150, 150)
            )
            x = (self.screen_width - high_score_text.get_width()) // 2
            screen.blit(high_score_text, (x, y))
        
        # Draw performance rating
        y += 60
        rating = self._get_rating(score)
        rating_text = self.font_medium.render(rating, True, self._get_rating_color(score))
        x = (self.screen_width - rating_text.get_width()) // 2
        screen.blit(rating_text, (x, y))
    
    def _get_rating(self, score: int) -> str:
        """Get performance rating based on score"""
        if score >= 100:
            return "★★★★★ LEGENDARY ★★★★★"
        elif score >= 50:
            return "★★★★ EXCELLENT ★★★★"
        elif score >= 30:
            return "★★★ GOOD ★★★"
        elif score >= 10:
            return "★★ NICE ★★"
        elif score >= 5:
            return "★ TRY AGAIN ★"
        else:
            return "KEEP PRACTICING"
    
    def _get_rating_color(self, score: int) -> Tuple[int, int, int]:
        """Get color for rating"""
        if score >= 100:
            return (255, 215, 0)  # Gold
        elif score >= 50:
            return (200, 200, 200)  # Silver
        elif score >= 30:
            return (205, 127, 50)  # Bronze
        else:
            return (150, 150, 150)  # Gray
