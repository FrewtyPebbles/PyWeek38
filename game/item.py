from __future__ import annotations
from Loxoc import (
        Object3D, Object2D, Sprite, Vec3, Quaternion, ConvexCollider, Collider, Mesh, Model,
        BoxCollider
)

from game_tools import Game

class MutKwarg:
    def __init__(self, value:any):
        self.value = value

    def __repr__(self) -> str:
        return repr(self.value)

    def __str__(self) -> str:
        return str(self.value)
    

class Item:
    def __init__(self, game:Game, name:str, description:str, model:Model, position:Vec3 = None, rotation:Vec3 = None, scale:Vec3 = None, collider:Collider = None, **kwargs:dict[str, any]):
        # The description has certain kwarg substitutions
        self.game = game
        self.name = name
        self.model = model
        self.position = position if position else Vec3(0.0,0.0,0.0)
        self.scale = scale if scale else Vec3(1.0,1.0,1.0)
        self._description = description
        self.substitutions = kwargs
        self.object = Object3D(self.model, self.position, rotation, self.scale)
        self.collider = collider if collider else BoxCollider(self.object)
        self.object.add_collider(self.collider)
        self.future_collider = type(self.collider)(self.object)
        self.pickup_collider = type(self.collider)(self.object, scale = Vec3(3,3,3))
        self.rotation = self.object.rotation
        self.velocity = Vec3(0,0,0)
        self.max_velocity = 20

    def check_collision(self, other:Vec3 | Collider | Object3D):
        return self.collider.check_collision(other)
    
    def check_collision_future(self, other: Object3D | Collider) -> bool:
        self.future_collider.offset = self.object.position + self.velocity * self.game.window.dt
        return self.future_collider.check_collision(other)
    
    def update(self, collisions:list[Vec3 | Collider | Object3D]):
        dt = self.game.window.dt
        c2 = any(self.check_collision_future(col) for col in collisions)
        if not c2:
            self.velocity.y -= self.game.globals["gravity"] * dt
        elif self.velocity.get_magnitude() > 0:
            # move to touch
            move_towards = self.velocity.get_normalized() * 0.0001
            while not any(self.check_collision(col) for col in collisions):
                self.object.position += move_towards
                self.object.get_model_matrix()
            self.velocity = Vec3(0,0,0)
            
        self.velocity.y = max(-self.max_velocity, min(self.max_velocity, self.velocity.y))
        self.object.position += self.velocity * dt

    @property
    def description(self):
        ret_d = ""
        escape = False
        parsing_kw = False
        kw_buffer = ""
        for c in self._description:
            if escape:
                escape = False
                if c not in {'{','}'}:
                    ret_d += '\\'
                ret_d += c
            elif c == "\\":
                escape = True
                continue
            elif c == '{':
                parsing_kw = True
                kw_buffer = ""
            elif c == '}':
                ret_d += str(self.substitutions[kw_buffer])
                parsing_kw = False
            elif parsing_kw:
                kw_buffer += c
            else:
                ret_d += c
        return ret_d
    
    @description.setter
    def description(self, value:str):
        self._description = value

