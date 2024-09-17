from __future__ import annotations

from Loxoc import Font, Text, Window, Vec4, Vec2, Vec3

from game_tools import Game

from typing import Callable

import math as m


class Dialogue:
    def __init__(self, game:Game, text:str, position:Vec2, font: Font | None = None, options:list[Dialogue] | None = None, callback:Callable[[], None] = lambda:None, _next:Dialogue | None = None, color: Vec4 | None = None, scale:Vec2 | None = None, rotation:float = 0.0, end_callback:Callable[[], None] = lambda:None, typing_speed = 10) -> None:
        self.game:Game = game
        self.text:str = text
        self.font:Font = font if font else self.game.globals["fonts"]["font_sofadi_one"]

        self.text_object = Text(self.text, color if color else Vec4(1,1,1,1), position, scale if scale else Vec2(1,1), rotation, self.font)
        self.options = options if options is not None else []
        self.callback = callback
        self.end_callback = end_callback
        self.next = _next
        self.progress = 0.0
        self.finished_typing = False
        self.running = False
        self.typing_speed = typing_speed

    def start(self):
        self.callback()
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
                self.finished_typing = True

    def end(self):
        self.end_callback()
        self.game.window.remove_text(self.text_object)
        self.running = False
        self.finished_typing = False

            
            
