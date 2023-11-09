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
    bullet_speed: int
    bullets: list[DesignerObject]
def create_world() -> World:
    """ Create the world """
    return World(create_spaceship(), 5, 10, [])
def create_spaceship() -> DesignerObject:
    spaceship = emoji("Rocket")
    turn_right(spaceship, 45)
    spaceship.x = 30
    spaceship.y = get_height()/2
    return spaceship
def create_bullets(world: World, key: str) -> DesignerObject:
    if key == 'space':
        bullet = rectangle("red", 20, 5, world.spaceship.x, world.spaceship.y)
        world.bullets.append(bullet)
        print(world.bullets)
        return bullet

def move_bullets(world: World):
    for bullet in world.bullets:
        bullet.x += 10
def destroy_bullets_on_exit(world: World):
    """ Destroy any water drops that have landed on the ground """
    kept = []
    for bullet in world.bullets:
        if bullet.x < get_width():
            kept.append(bullet)
        else:
            destroy(bullet)
    world.bullets = kept
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
when('updating', move_bullets)
when('updating', destroy_bullets_on_exit)
when('typing', control_spaceship_move)
when('typing', create_bullets)
start()