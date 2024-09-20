from Loxoc import (
        Object3D, Object2D, Sprite, Vec3, Quaternion, ConvexCollider, Collider, Mesh, Model
)

class MutKwarg:
    def __init__(self, value:any):
        self.value = value

    def __repr__(self) -> str:
        return repr(self.value)

    def __str__(self) -> str:
        return str(self.value)
    

class Item:
    def __init__(self, name:str, description:str, model:Model, position:Vec3 = None, rotation:Quaternion = None, scale:Vec3 = None, collider:Collider = None, **kwargs:dict[str, any]):
        # The description has certain kwarg substitutions
        self.name = name
        self.model = model
        self.position = position if position else Vec3(0.0,0.0,0.0)
        self.rotation = rotation if rotation else Quaternion.from_axis_angle(Vec3(0.0,1.0,0.0), 0)
        self.scale = scale if scale else Vec3(1.0,1.0,1.0)
        self._description = description
        self.substitutions = kwargs
        print("Attempting to create object...")
        self.object = Object3D(self.model, self.position, self.rotation, self.scale)
        print("Created object")
        self.collider = collider if collider else ConvexCollider(self.object)
        print("Created collider")
        self.object.add_collider(self.collider)
        print("Added collider to object")

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

