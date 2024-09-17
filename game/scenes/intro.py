from __future__ import annotations
from game_tools import Game
from game_tools.scene import Scene
from game_tools.utility import is_clicking_sprite
from game.dialogue import Dialogue

from game.player import Player

from Loxoc import (
    Sprite, Object2D, Vec2, EVENT_STATE, Model, Object3D, Vec3, EVENT_FLAG, BoxCollider
)

import math

class SceneIntro(Scene):
    def load(self, game: Game):
        super().load(game)

        self.player = Player(self.game)

        self.cube_model = Model.from_file("./models/cube/cube.gltf")

        self.cube = Object3D(self.cube_model, Vec3(0,0,10))
        self.cube_collider = BoxCollider(self.cube)
        self.cube.add_collider(self.cube_collider)
        self.game.window.add_object(self.cube)

        self.floor = Object3D(self.cube_model, Vec3(0,-5,10), scale=Vec3(100,1,100))
        self.floor_collider = BoxCollider(self.floor)
        self.floor.add_collider(self.floor_collider)
        self.game.window.add_object(self.floor)
        
        dialogue_position = Vec2(30, 30)

        self.test_dialogue = Dialogue(game, "Hello how are you?", dialogue_position, _next = Dialogue(game, "Ah, thats right you cant respond yet!", dialogue_position, _next = Dialogue(game, "Bye then.", dialogue_position)))
    
    def unload(self):
        self.game.window.remove_object(self.cube)
        self.game.window.remove_object(self.floor)

    def update(self):
        dt = self.game.window.deltatime
        event = self.game.window.event
        mouse = event.mouse

        if event.get_flag(EVENT_FLAG.KEY_ESCAPE) == EVENT_STATE.PRESSED:
            self.game.quit_game = True

        self.cube.rotation.rotate_yaw(2 * dt)
        self.cube.rotation.rotate_pitch(2 * dt)
        self.cube.rotation.rotate_roll(2 * dt)

        self.player.update(self.player_falling_collision_check, self.player_movement_collision_check)

        self.test_dialogue.update()

        if self.test_dialogue.running and self.player.position.distance(self.cube.position) > 10:
            self.test_dialogue.end()

        self.player_on_interact()

        self.game.window.update()

    def player_on_interact(self):
        event = self.game.window.event
        mouse = event.mouse
        if mouse.state == EVENT_STATE.PRESSED:
            cube_hit = self.player.center_ray_collision(self.cube)
            if cube_hit.hit:
                if not self.test_dialogue.finished_typing:
                    print("CUBE START")
                    self.test_dialogue.start()
                elif self.test_dialogue.next:
                    self.test_dialogue.end()
                    self.test_dialogue = self.test_dialogue.next
                    self.test_dialogue.start()
                else:
                    print("CUBE END")
                    self.test_dialogue.end()
                



    def player_falling_collision_check(self):
        if all(self.player.check_collision_future(col) for col in [self.floor]):
            self.player.velocity.y = 0
            self.player.can_jump = True

    def player_movement_collision_check(self):
        if all(self.player.check_collision_future(col) for col in [self.cube]):
            self.player.velocity = Vec3(0,0,0)
            self.player.can_jump = True

    def start(self):
        self.player.start()

