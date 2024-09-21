from __future__ import annotations
from game_tools import Game
from game_tools.scene import Scene
from game_tools.utility import is_clicking_sprite
from game.dialogue import Dialogue, DialogueOption

from game.player import Player
from game.item import Item

from Loxoc import (
    Sprite, Object2D, Vec2, EVENT_STATE, Model, Object3D, Vec3, EVENT_FLAG, BoxCollider,
    Quaternion as Quat, Texture, Material, TextureFiltering, Shader, ShaderType, Text, Vec4
)

import math

class SceneIntro(Scene):
    def load(self, game: Game):
        super().load(game)

        self.player = Player(self.game)
        
        self.character_plane_model = Model.from_file("./models/character_plane/character_plane.gltf")

        self.cube_model = Model.from_file("./models/cube/cube.gltf")

        self.stick_figure_sprite = Texture.from_file("./sprites/Bilboard Sprite Man.png", filtering=TextureFiltering.NEAREST)
        self.concrete_texture = Texture.from_file("./sprites/concrete.jpg")

        self.character = Object3D(self.character_plane_model, Vec3(0,-2,10), scale=Vec3(1,1,1),
            material=Material(fragment=Shader.from_file("./shaders/character_fragment.glsl", ShaderType.FRAGMENT)))
        self.character.material.diffuse_texture = self.stick_figure_sprite
        self.character_collider = BoxCollider(self.character)
        self.character.add_collider(self.character_collider)
        self.game.window.add_object(self.character)

        self.floor = Object3D(self.cube_model, Vec3(0,-5,10), scale=Vec3(100,1,100))
        self.floor.material.diffuse_texture = self.concrete_texture
        self.floor_collider = BoxCollider(self.floor)
        self.floor.add_collider(self.floor_collider)
        self.game.window.add_object(self.floor)

        self.item_tip_text = Text("", Vec4(1,1,1,1), Vec2(20, game.dimensions[1] - 35), Vec2(0.5,0.5), font=self.game.globals["fonts"]["font_sofadi_one"])
        self.game.window.add_text(self.item_tip_text)

        self.test_item = Item(game, "Cube", "Very cubic.", self.cube_model, Vec3(-10,-2,10), scale=Vec3(0.1,0.1,0.1))
        self.game.window.add_object(self.test_item.object)
        
        
        dialogue_position = Vec2(30, 30)
        
        dialogue_option_position = Vec2(self.game.dimensions[0]* 2/3, 70)


        self.dialogue_option_background = Sprite.from_texture(Texture.from_file("./sprites/textbox_background.png", filtering=TextureFiltering.NEAREST))


        self.dialogue = Dialogue(game, "Hello how are you?", dialogue_position, options = [
            DialogueOption(game, "Good", self.dialogue_option_background, dialogue_option_position + Vec2(0,80), 
                chosen_callback = lambda: self.change_dialogue(Dialogue(game, "Awesome!", dialogue_position)),
                finished_typing_callback = lambda:self.player.rotation_lock(True),
                end_callback = lambda:self.player.rotation_lock(False)
            ),
            DialogueOption(game, "Bad", self.dialogue_option_background, dialogue_option_position, 
                chosen_callback = lambda: self.change_dialogue(Dialogue(game, "I'm sorry to hear that!", dialogue_position)),
                finished_typing_callback = lambda:self.player.rotation_lock(True),
                end_callback = lambda:self.player.rotation_lock(False)
            )
        ])

        self.items = [self.test_item]
        
    
    def unload(self):
        super().unload()
        if self.dialogue.running:
            self.dialogue.end()
        self.game.window.remove_object(self.character)
        self.game.window.remove_object(self.floor)
        self.game.window.remove_object(self.test_item.object)
        self.game.window.remove_text(self.item_tip_text)

    def update(self):
        dt = self.game.window.deltatime
        event = self.game.window.event

        if event.get_flag(EVENT_FLAG.KEY_ESCAPE) == EVENT_STATE.PRESSED:
            self.game.quit_game = True


        self.player.update(self.player_falling_collision_check, self.player_movement_collision_check)

        # DIALOGUE

        if self.player.position.distance(self.character.position) < 10:
            self.player_on_interact()
        elif self.dialogue.running:
            self.dialogue.end()
            
        self.dialogue.update()
        
        self.bilboard_character(self.character)

        if event.get_flag(EVENT_FLAG.KEY_r) == EVENT_STATE.PRESSED:
            self.game.current_scene = self
    
        self.pickup_check()
        
        self.item_update()

        self.game.window.update()

    def pickup_check(self):
        event = self.game.window.event
        
        did_hit = False

        for item in self.items:
            item_hit = self.player.center_ray_collision(item.pickup_collider)
            if item_hit.hit and self.player.position.distance(item.position) < 10:
                did_hit = True
                self.item_tip_text.text = f"{item.name} : {item.description}"
                if event.get_flag(EVENT_FLAG.KEY_e) == EVENT_STATE.PRESSED:
                    if self.player.held_item:
                        self.player.held_item = None
                    else:
                        self.player.held_item = item

        if not did_hit:
            self.item_tip_text.text = ""

    def item_update(self):
        colliders = [self.floor]
        for item in self.items:
            if item != self.player.held_item:
                item.update(colliders)

    def player_on_interact(self):
        event = self.game.window.event
        mouse = event.mouse
        if mouse.state == EVENT_STATE.PRESSED:
            cube_hit = self.player.center_ray_collision(self.character)
            if cube_hit.hit:
                if not self.dialogue.finished_typing:
                    # CUBE START
                    self.dialogue.start()
                elif self.dialogue.next:
                    self.dialogue.end()
                    self.dialogue = self.dialogue.next
                    self.dialogue.start()
                elif len(self.dialogue.options) == 0:
                    # CUBE END
                    self.dialogue.end()
                
    
    def bilboard_character(self, character:Object3D):
        vec_direction = (character.position - self.player.position).get_normalized()
        fwd_vec = character.rotation.forward
        
        current_yaw = math.atan2(fwd_vec.x, fwd_vec.z)
        target_yaw = math.atan2(vec_direction.x, vec_direction.z)
        
        yaw = target_yaw - current_yaw
        
        yaw_quat = Quat.from_axis_angle(Vec3(0.0,1.0,0.0), yaw)
        
        character.rotation = (yaw_quat * character.rotation).get_normalized()

    def player_falling_collision_check(self):
        if any(self.player.check_collision_future(col) for col in [self.floor, self.character]):
            self.player.velocity = Vec3(0,0,0)
            self.player.can_jump = True

    def player_movement_collision_check(self):
        if any(self.player.check_collision_future(col) for col in [self.character]):
            self.player.velocity = Vec3(0,0,0)
            self.player.can_jump = True
    
    def change_dialogue(self, dialogue:Dialogue):
        self.dialogue.end()
        self.dialogue = dialogue
        self.dialogue.start()

    def start(self):
        self.player.start()

