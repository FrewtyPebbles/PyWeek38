from Loxoc import Camera, Window, EVENT_FLAG, Vec3, Font
import math
from game_tools.scene import Scene

class Game:
    def __init__(self, first_scene:Scene, dimensions:tuple[int, int] = (1280, 720), title:str = "PyWeek 38") -> None:
        # Create all assets
        self.dimensions = dimensions
        self.camera:Camera = Camera(Vec3(0.0, 0.0, 0.0), Vec3(0.0,0.0,0.0), *self.dimensions, 10000, math.radians(60))
        self.window:Window = Window(title, self.camera, *self.dimensions, False, Vec3(1, 1, 1))
        self._current_scene:Scene = first_scene
        self.globals:dict[str, any] = {
            "mouse_sensitivity_x": 50,
            "mouse_sensitivity_y": 50,
            "gravity": 60.7,
            "fonts": {
                "font_sofadi_one": Font("./fonts/Sofadi_One/SofadiOne-Regular.ttf")
            }
        }
        self.quit_game:bool = False
        

    @property
    def current_scene(self) -> Scene:
        return self._current_scene
    
    @current_scene.setter
    def current_scene(self, scene:Scene) -> Scene:
        self._current_scene.unload()
        self._current_scene = scene
        self._current_scene.load(self)
        self._current_scene.start()

    def init_load(self):
        # This is where we load in all of our 3D assets along with our first scene.
        self.current_scene.load(self)


    def game_loop(self):
        self.current_scene.start()
        while not self.window.event.check_flag(EVENT_FLAG.QUIT):
            self.update()
            if self.quit_game:
                break

    def update(self):
        self.current_scene.update()
