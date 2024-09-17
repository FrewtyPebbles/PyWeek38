from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_tools import Game

class Scene:
    def __init__(self, game: Game | None = None) -> None:
        self.loaded: bool = False
        self.game: Game | None = game
    
    def load(self, game: Game):
        # This function should only be called once and loads all of the data from the scene into ram.
        self.loaded = True
        self.game = game

    def unload(self):
        pass

    def update(self):
        pass

    def start(self):
        pass