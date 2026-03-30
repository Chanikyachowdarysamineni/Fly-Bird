class Window:
    # Available window sizes
    SIZES = {
        'Small': (240, 427),
        'Medium': (288, 512),
        'Large': (360, 640),
        'XL': (432, 768),
    }
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ratio = width / height
        self.w = width
        self.h = height
        self.r = width / height
        self.viewport_width = width
        self.viewport_height = height * 0.79
        self.vw = width
        self.vh = height * 0.79
        self.viewport_ratio = self.vw / self.vh
        self.vr = self.vw / self.vh
    
    def resize(self, width, height):
        """Dynamically resize the window"""
        self.width = width
        self.height = height
        self.ratio = width / height
        self.w = width
        self.h = height
        self.r = width / height
        self.viewport_width = width
        self.viewport_height = height * 0.79
        self.vw = width
        self.vh = height * 0.79
        self.viewport_ratio = self.vw / self.vh
        self.vr = self.vw / self.vh
