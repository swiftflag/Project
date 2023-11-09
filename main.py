from dataclasses import dataclass
from designer import *
from random import randint
def create_copter() -> DesignerObject:
    """ Create the copter """
    copter = emoji("Rocket")
    return copter
@dataclass
class World:
    spaceship: DesignerObject
    spaceship_speed: int
def create_world() -> World:
    """ Create the world """
    return World(create_spaceship(), 5)
def create_spaceship() -> DesignerObject:
    spaceship = emoji("Rocket")
    turn_right(spaceship, 45)
    spaceship.x = 30
    spaceship.y = get_height()/2
    return spaceship
def move_spaceship(world: World, key: str):
        world.spaceship.y += world.spaceship_speed
        if world.spaceship.y >= get_height():
            world.spaceship.y = get_height() - 1
        elif world.spaceship.y <= 0:
            world.spaceship.y = 1
def control_spaceship_move(world:World, key:str):
    if key == "up" and world.spaceship_speed > 0:
        world.spaceship_speed = -world.spaceship_speed
    elif key == "down" and world.spaceship_speed < 0:
        world.spaceship_speed = -world.spaceship_speed
when('starting', create_world)
when('updating', move_spaceship)
when('typing', control_spaceship_move)
start()