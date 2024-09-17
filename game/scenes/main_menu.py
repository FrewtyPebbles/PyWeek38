from __future__ import annotations
from game_tools import Game
from game_tools.scene import Scene
from game_tools.utility import is_clicking_sprite

from game.scenes.intro import SceneIntro

from Loxoc import (Sprite, Object2D, Vec2, EVENT_STATE)
import math

class SceneMainMenu(Scene):
    def load(self, game: Game):
        super().load(game)
        self.start_button_sprite = Sprite("./sprites/placeholder_start_button.png")
        self.start_button = Object2D(self.start_button_sprite, self.game.camera, Vec2(self.game.camera.view_width/2, self.game.camera.view_height/2), scale=Vec2(100,100))
        self.game.window.add_object2d(self.start_button)

        self.fullscreen_button_sprite = Sprite("./sprites/placeholder_fullscreen_button.png")
        self.fullscreen_button = Object2D(self.fullscreen_button_sprite, self.game.camera, Vec2(self.game.camera.view_width/2, self.game.camera.view_height/2 - 100), scale=Vec2(100,100))
        self.game.window.add_object2d(self.fullscreen_button)

    def unload(self):
        self.game.window.remove_object2d(self.start_button)
        self.game.window.remove_object2d(self.fullscreen_button)

    
    def update(self):
        mouse = self.game.window.event.mouse
        
        if is_clicking_sprite(self.start_button, mouse):
                self.game.current_scene = SceneIntro()

        if is_clicking_sprite(self.fullscreen_button, mouse):
                self.game.window.fullscreen = not self.game.window.fullscreen

        self.game.window.update()
        
    
    def start(self):
        pass