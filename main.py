from Loxoc import Camera, Window, EVENT_FLAG
from game_tools import Game
from game import SceneMainMenu


game = Game(SceneMainMenu())
game.init_load()
game.game_loop()