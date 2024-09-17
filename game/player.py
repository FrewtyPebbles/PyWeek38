from game_tools import Game

from Loxoc import (Camera, Window, EVENT_FLAG, Vec3, Object3D, Quaternion, BoxCollider, Collider, EVENT_STATE, RayCollider, RayHit)

from copy import copy

import math as m

from typing import Callable

class Player:
    def __init__(self, game:Game, position: Vec3 | None = None, rotation: Quaternion | None = None, speed = 7, max_speed = 10, max_jump_speed = 20, friction = 5) -> None:
        self.game: Game = game
        self.position: Vec3 = position if position else Vec3(0,0,0)
        self.velocity: Vec3 = Vec3(0,0,0)
        self.rotation:Quaternion = rotation if rotation else game.camera.rotation
        self.speed = speed
        self.max_speed = max_speed
        self.max_jump_speed = max_jump_speed
        self.friction = friction
        self.player_collider_bounds = Vec3(1,1,1), Vec3(-1,-1,-1)
        self.player_collider = BoxCollider.from_bounds(*self.player_collider_bounds, offset = copy(self.position), scale=Vec3(1,4,1))
        self.can_jump = True

        self.center_ray = RayCollider(self.position, self.rotation)
        
    def center_ray_collision(self, other: Object3D | Collider) -> RayHit:
        return self.center_ray.get_collision(other)

    def check_collision(self, other: Object3D | Collider) -> bool:
        return self.player_collider.check_collision(other)
    
    def check_collision_future(self, other: Object3D | Collider) -> bool:
        collider = BoxCollider.from_bounds(*self.player_collider_bounds, scale=self.player_collider.scale, offset = self.position - Vec3(0,0.01,0) + self.velocity * self.game.window.dt)
        did_collide = collider.check_collision(other)
        return did_collide

    def vel_update(self, middle_callback: Callable[[], None] = lambda:None):
        dt = self.game.window.dt
        gravity = self.game.globals["gravity"]
        event = self.game.window.event

        # find angle between vector and plane to fix forward z/x rotation

        fwd_floor_angle = m.pi/2 - m.acos(min(1, max(-1, self.rotation.forward.dot(Vec3(0,1,0)))))

        fwd_correction_quat = Quaternion.from_axis_angle(self.rotation.right, fwd_floor_angle)
        
        fwd_corrected:Vec3 = fwd_correction_quat * self.rotation.forward

        # Apply movement velocities

        if event.get_flag(EVENT_FLAG.KEY_w) == EVENT_STATE.PRESSED:
            fwd = fwd_corrected * self.speed

            self.velocity += Vec3(fwd.x, 0.0, fwd.z)
        
        if event.get_flag(EVENT_FLAG.KEY_s) == EVENT_STATE.PRESSED:
            fwd = fwd_corrected * self.speed

            self.velocity -= Vec3(fwd.x, 0.0, fwd.z)

        if event.get_flag(EVENT_FLAG.KEY_d) == EVENT_STATE.PRESSED:
            right = self.rotation.right * self.speed

            self.velocity -= Vec3(right.x, 0.0, right.z)

        if event.get_flag(EVENT_FLAG.KEY_a) == EVENT_STATE.PRESSED:
            right = self.rotation.right * self.speed

            self.velocity += Vec3(right.x, 0.0, right.z)

        if event.get_flag(EVENT_FLAG.KEY_SPACE) == EVENT_STATE.PRESSED and self.can_jump:
            self.velocity.y += self.max_jump_speed
            self.can_jump = False

        # clamp velocity

        v_clamp = lambda coord: min(self.max_speed, max(-self.max_speed, coord))

        self.velocity = Vec3(v_clamp(self.velocity.x), max(-self.max_jump_speed, min(self.max_jump_speed, self.velocity.y)), v_clamp(self.velocity.z))

        # callback
        middle_callback()

        # apply velocity

        self.position += self.velocity * dt

        # apply friction to velocity

        if self.velocity.get_magnitude() > 0:
            self.velocity.y = max(-self.max_jump_speed, min(self.max_jump_speed, self.velocity.y - gravity))
            c1 = abs(self.velocity.x) - self.friction < 0
            c2 = abs(self.velocity.z) - self.friction < 0
            if c1:
                self.velocity.x = 0
            else:
                self.velocity.x -= self.friction * m.copysign(1.0, self.velocity.x)
            if c2:
                self.velocity.z = 0
            else:
                self.velocity.z -= self.friction * m.copysign(1.0, self.velocity.z)


    def look_update(self):
        dt = self.game.window.dt
        
        mouse = self.game.window.event.mouse

        mouse_moving = self.game.window.event.check_flag(EVENT_FLAG.MOUSE_MOTION)

        fwd_floor_angle = m.pi/2 - m.acos(min(1, max(-1, self.rotation.forward.dot(Vec3(0,1,0)))))

        if abs(fwd_floor_angle) < m.radians(90):
            self.rotation.rotate(self.rotation.right, mouse_moving * m.radians(mouse.rel_y * self.game.globals["mouse_sensitivity_y"]) * dt)

        self.rotation.rotate(Vec3(0,1,0), -mouse_moving * m.radians(mouse.rel_x * self.game.globals["mouse_sensitivity_x"]) * dt)

    def update(self, middle_callback: Callable[[], None] = lambda:None, velocity_middle_callback: Callable[[], None] = lambda:None):
        camera = self.game.camera

        self.look_update()
        self.vel_update(velocity_middle_callback)
        self.player_collider.offset = camera.position

        self.center_ray.direction = self.rotation
        self.center_ray.origin = self.position

        middle_callback()

        camera.position = self.position
        camera.rotation = self.rotation

    def start(self):
        self.game.window.lock_mouse(True)

        
