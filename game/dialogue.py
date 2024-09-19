from __future__ import annotations

from Loxoc import Font, Text, Window, Vec4, Vec2, Vec3, Sprite, Object2D

from game_tools import Game
from game_tools.utility import is_clicking_sprite

from typing import Callable


import math as m

class DialogueOption:
    def __init__(self, game:Game, text:str, background_sprite: Sprite, position:Vec2, font: Font | None = None, start_callback:Callable[[], None] = lambda:None, chosen_callback:Callable[[], None] = lambda:None, end_callback:Callable[[], None] = lambda:None, finished_typing_callback:Callable[[], None] = lambda:None, _next:Dialogue | None = None, color: Vec4 | None = None, scale:Vec2 | None = None, rotation:float = 0.0, typing_speed = 10):
        self.game:Game = game
        self.text:str = text
        self.font:Font = font if font else self.game.globals["fonts"]["font_sofadi_one"]
        self.background = Object2D(background_sprite, game.camera, scale = Vec2(100,100))

        self.background.position = position + Vec2(self.background.width/2, self.background.height/2) - 30
        
        self.text_object = Text(self.text, color if color else Vec4(1,1,1,1), position, scale if scale else Vec2(1,1), rotation, self.font)
        self.start_callback = start_callback
        self.chosen_callback = chosen_callback
        self.end_callback = end_callback
        self.finished_typing_callback = finished_typing_callback
        self.next = _next

        # State
        self.progress = 0.0
        self.finished_typing = False
        self.running = False
        self.typing_speed = typing_speed

        # Transform
        self.position = position
        self.scale = scale

    def choose(self):
        self.chosen_callback()
        self.game.window.lock_mouse(True)

    def start(self):
        self.start_callback()
        self.game.window.add_text(self.text_object)
        self.game.window.add_object2d(self.background)
        self.progress = 0.0
        self.finished_typing = False
        self.running = True
        self.text_object.text = ""
        

    def update(self):
        if self.running:
            dt = self.game.window.dt
            self.progress += self.typing_speed * dt
            text_len = min(len(self.text), m.ceil(self.progress))
            self.text_object.text = self.text[:text_len]

            if text_len == len(self.text):
                if not self.finished_typing:
                    self.game.window.lock_mouse(False)
                    self.finished_typing_callback()
                self.finished_typing = True
                if is_clicking_sprite(self.background, self.game.window.event.mouse):
                    self.choose()

    def end(self):
        self.end_callback()
        self.game.window.remove_text(self.text_object)
        self.game.window.remove_object2d(self.background)
        self.running = False
        self.finished_typing = False
        self.game.window.lock_mouse(True)

class Dialogue:
    def __init__(self, game:Game, text:str, position:Vec2, font: Font | None = None, options:list[DialogueOption] | None = None, start_callback:Callable[[], None] = lambda:None, _next:Dialogue | None = None, color: Vec4 | None = None, scale:Vec2 | None = None, rotation:float = 0.0, end_callback:Callable[[], None] = lambda:None, typing_speed = 10) -> None:
        self.game:Game = game
        self.text:str = text
        self.font:Font = font if font else self.game.globals["fonts"]["font_sofadi_one"]

        self.text_object = Text(self.text, color if color else Vec4(1,1,1,1), position, scale if scale else Vec2(1,1), rotation, self.font)
        self.options:list[DialogueOption] = options if options is not None else []
        self.start_callback = start_callback
        self.end_callback = end_callback
        self.next = _next

        # State
        self.progress = 0.0
        self.finished_typing = False
        self.running = False
        self.typing_speed = typing_speed

        # Transform
        self.position = position
        self.scale = scale

    def start(self):
        self.start_callback()
        self.game.window.add_text(self.text_object)
        self.progress = 0.0
        self.finished_typing = False
        self.running = True
        self.text_object.text = ""

    def update(self):
        if self.running:
            dt = self.game.window.dt
            self.progress += self.typing_speed * dt
            text_len = min(len(self.text), m.ceil(self.progress))
            self.text_object.text = self.text[:text_len]
            
            
            if text_len == len(self.text):
                if not self.finished_typing:
                    for option in self.options:
                        option.start()
                self.finished_typing = True

            # render the options
            if self.finished_typing:
                for option in self.options:
                    option.update()

    def end(self):
        self.end_callback()
        self.game.window.remove_text(self.text_object)
        self.running = False
        self.finished_typing = False
        for option in self.options:
            if option.running or option.finished_typing:
                option.end()

            
            
