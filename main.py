import asyncio
import os

# Suppress pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from src.flappy import Flappy

if __name__ == "__main__":
    asyncio.run(Flappy().start())
