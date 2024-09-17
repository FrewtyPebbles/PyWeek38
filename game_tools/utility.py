from Loxoc import (MouseDevice, Vec2, Object2D, EVENT_STATE)

def is_clicking_sprite(obj: Object2D, mouse: MouseDevice) -> bool:
    o_wd2 = obj.width/2
    o_hd2 = obj.height/2
    return mouse.state == EVENT_STATE.PRESSED and \
    obj.position.x - o_wd2 < mouse.x < obj.position.x + o_wd2 and\
    obj.position.y - o_hd2 < mouse.y < obj.position.y + o_hd2