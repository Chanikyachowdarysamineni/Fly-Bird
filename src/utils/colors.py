# 🎨 Advanced Color Palette System for FlapPyBird

"""
Professional color palette with modern design principles
"""

class ColorTheme:
    """Modern, professional color scheme"""
    
    # Primary Colors (Brand)
    PRIMARY_CYAN = (0, 219, 255)      # Bright cyan/electric blue
    PRIMARY_DARK = (10, 25, 50)       # Deep dark blue
    PRIMARY_ACCENT = (255, 107, 53)   # Vibrant coral/orange
    
    # Secondary Colors (Feedback)
    SUCCESS_GREEN = (34, 197, 94)     # Bright green for success
    WARNING_AMBER = (252, 191, 73)    # Warm amber for warnings
    ERROR_RED = (239, 68, 68)         # Bright red for errors
    INFO_PURPLE = (168, 85, 247)      # Purple for info/power-ups
    
    # Grayscale (UI/Background)
    BG_DARK = (15, 23, 42)            # Nearly black background
    BG_MEDIUM = (51, 65, 85)          # Medium dark gray
    BG_LIGHT = (203, 213, 225)        # Light gray
    TEXT_PRIMARY = (248, 250, 252)    # Nearly white text
    TEXT_SECONDARY = (148, 163, 184)  # Muted gray text
    TEXT_DARK = (75, 85, 99)          # Dark text on light
    
    # Transparency variants
    OVERLAY_DARK = (15, 23, 42, 200)  # Semi-transparent dark
    OVERLAY_LIGHT = (248, 250, 252, 180)
    
    # Difficulty Colors (Enhanced)
    DIFFICULTY_EASY = (34, 197, 94)      # Fresh green
    DIFFICULTY_MEDIUM = (251, 146, 60)   # Warm orange
    DIFFICULTY_HARD = (239, 68, 68)      # Vibrant red
    
    # Power-Up Colors
    POWERUP_SHIELD = (59, 130, 246)      # Bright blue
    POWERUP_SLOWMO = (168, 85, 247)      # Purple
    POWERUP_BOOST = (251, 191, 36)       # Golden yellow
    
    # Highlight & Borders
    BORDER_ACCENT = (0, 219, 255)        # Cyan borders
    BORDER_SUBTLE = (100, 116, 139)      # Subtle borders
    HIGHLIGHT = (255, 215, 0)            # Gold highlight
    SHADOW = (0, 0, 0, 100)              # Shadow


class UIColorScheme:
    """UI-specific color configurations"""
    
    @staticmethod
    def get_difficulty_color(difficulty_name):
        """Get color for difficulty level"""
        colors = {
            "EASY": ColorTheme.DIFFICULTY_EASY,
            "MEDIUM": ColorTheme.DIFFICULTY_MEDIUM,
            "HARD": ColorTheme.DIFFICULTY_HARD,
        }
        return colors.get(difficulty_name, ColorTheme.PRIMARY_CYAN)
    
    @staticmethod
    def get_powerup_color(powerup_type):
        """Get color for power-up type"""
        colors = {
            "SHIELD": ColorTheme.POWERUP_SHIELD,
            "SLOW_MO": ColorTheme.POWERUP_SLOWMO,
            "SCORE_BOOST": ColorTheme.POWERUP_BOOST,
        }
        return colors.get(str(powerup_type), ColorTheme.PRIMARY_ACCENT)
    
    @staticmethod
    def get_status_color(status):
        """Get color for status messages"""
        status_colors = {
            "success": ColorTheme.SUCCESS_GREEN,
            "warning": ColorTheme.WARNING_AMBER,
            "error": ColorTheme.ERROR_RED,
            "info": ColorTheme.INFO_PURPLE,
        }
        return status_colors.get(status, ColorTheme.PRIMARY_CYAN)
    
    @staticmethod
    def gradient_menu_bg():
        """Background gradient for menus (RGB tuples)"""
        return [
            ColorTheme.BG_DARK,
            ColorTheme.PRIMARY_DARK,
            ColorTheme.BG_DARK,
        ]


class AdvancedUIEffects:
    """Color effects and advanced UI styling"""
    
    @staticmethod
    def get_hover_color(base_color, intensity=1.2):
        """Get brightened color for hover effects"""
        return tuple(min(int(c * intensity), 255) for c in base_color)
    
    @staticmethod
    def get_disabled_color(base_color, opacity=0.5):
        """Get faded color for disabled states"""
        return tuple(int(c * opacity) for c in base_color)
    
    @staticmethod
    def pulse_color(base_color, pulse_intensity):
        """Get pulsed color for animations"""
        r, g, b = base_color
        intensity = 0.7 + 0.3 * pulse_intensity  # Animate between 0.7 and 1.0
        return (int(r * intensity), int(g * intensity), int(b * intensity))
    
    @staticmethod
    def get_gradient_color(start_color, end_color, progress):
        """Interpolate between two colors (0.0 to 1.0)"""
        r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)
        return (r, g, b)


class MenuTheme:
    """Theme for menu screens"""
    
    # Menu backgrounds
    MENU_BG = ColorTheme.BG_DARK
    MENU_ACCENT = ColorTheme.PRIMARY_CYAN
    
    # Text colors
    TITLE_COLOR = ColorTheme.PRIMARY_CYAN
    SUBTITLE_COLOR = ColorTheme.TEXT_SECONDARY
    OPTION_COLOR = ColorTheme.TEXT_PRIMARY
    OPTION_HOVER_COLOR = ColorTheme.PRIMARY_ACCENT
    
    # Statistics display
    STAT_LABEL_COLOR = ColorTheme.TEXT_SECONDARY
    STAT_VALUE_COLOR = ColorTheme.TEXT_PRIMARY
    STAT_HIGHLIGHT_COLOR = ColorTheme.PRIMARY_CYAN
    
    # Button styling
    BUTTON_BG = ColorTheme.PRIMARY_ACCENT
    BUTTON_BG_HOVER = ColorTheme.WARNING_AMBER
    BUTTON_TEXT = ColorTheme.BG_DARK
    BUTTON_BORDER = ColorTheme.PRIMARY_ACCENT


class GameplayTheme:
    """Theme for in-game display"""
    
    # HUD colors
    HUD_BG = ColorTheme.BG_DARK
    HUD_TEXT = ColorTheme.TEXT_PRIMARY
    HUD_ACCENT = ColorTheme.PRIMARY_CYAN
    
    # Score display
    SCORE_COLOR = ColorTheme.TEXT_PRIMARY
    SCORE_MULTIPLIER_COLOR = ColorTheme.POWERUP_BOOST
    COMBO_COLOR = ColorTheme.WARNING_AMBER
    
    # Status indicators
    LIVES_FULL = ColorTheme.SUCCESS_GREEN
    LIVES_WARNING = ColorTheme.WARNING_AMBER
    LIVES_CRITICAL = ColorTheme.ERROR_RED
    
    # Notifications
    NOTIFICATION_BG = ColorTheme.BG_MEDIUM
    NOTIFICATION_TEXT = ColorTheme.TEXT_PRIMARY
    NOTIFICATION_SUCCESS = ColorTheme.SUCCESS_GREEN
    NOTIFICATION_WARNING = ColorTheme.WARNING_AMBER


class ParticleColors:
    """Colors for particle effects"""
    
    EXPLOSION_PRIMARY = ColorTheme.PRIMARY_ACCENT
    EXPLOSION_SECONDARY = ColorTheme.WARNING_AMBER
    
    SCORE_POPUP = ColorTheme.POWERUP_BOOST
    SCORE_POPUP_GLOW = ColorTheme.WARNING_AMBER
    
    SHIELD_ACTIVATION = ColorTheme.POWERUP_SHIELD
    SHIELD_BURST = ColorTheme.PRIMARY_CYAN
    
    COMBO_BURST = ColorTheme.POWERUP_BOOST


# Export for easy access
COLORS = ColorTheme()
UI = UIColorScheme()
EFFECTS = AdvancedUIEffects()
