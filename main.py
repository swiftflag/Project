from dataclasses import dataclass
from designer import *
from random import randint

@dataclass
class Enemy_Movement:
    movement_angle: int
    rotate_up: int
@dataclass
class World:
    spaceship: DesignerObject
    spaceship_speed: int
    bullet_speed: int
    bullets: list[DesignerObject]
    enemies: list[DesignerObject]
    enemy_speed: int
    spawn_timer: int
    enemy_movement_angles: list[Enemy_Movement]

def create_world() -> World:
    """ Create the world """
    return World(create_spaceship(), 5, 10, [],[], 5,135, [])
def create_spaceship() -> DesignerObject:
    spaceship = emoji("Rocket")
    turn_right(spaceship, 45)
    spaceship.x = 30
    spaceship.y = get_height()/2
    return spaceship
def create_enemies(world: World) -> DesignerObject:
    world.spawn_timer += 1
    if (world.spawn_timer % 10) == 0:
        enemy = emoji("Rocket")
        turn_left(enemy, 135)
        enemy.x = get_width()
        enemy.y = randint(0,get_height())
        world.enemies.append(enemy)
        world.enemy_movement_angles.append(Enemy_Movement(randint(135, 225),randint(0,1)))
        return enemy
def change_angle(enemy_num: int, world: World):
    if world.enemy_movement_angles[enemy_num].movement_angle < 135:
        world.enemy_movement_angles[enemy_num].movement_angle = 135
        world.enemy_movement_angles[enemy_num].rotate_up = 1
    elif world.enemy_movement_angles[enemy_num].movement_angle > 225:
        world.enemy_movement_angles[enemy_num].movement_angle = 225
        world.enemy_movement_angles[enemy_num].rotate_up = 0
    if world.enemy_movement_angles[enemy_num].rotate_up == 1:
        world.enemy_movement_angles[enemy_num].movement_angle += 1
    else:
        world.enemy_movement_angles[enemy_num].movement_angle -= 1
def move_enemies(world: World):
    for enemy_num, enemy in enumerate(world.enemies):
        move_forward(enemy, world.enemy_speed, (world.enemy_movement_angles[enemy_num].movement_angle))
        change_angle(enemy_num, world)

def create_bullets(world: World, key: str) -> DesignerObject:
    if key == 'space':
        bullet = rectangle("red", 20, 5, world.spaceship.x + 20, world.spaceship.y)
        world.bullets.append(bullet)
        print(world.bullets)
        return bullet

def move_bullets(world: World):
    for bullet in world.bullets:
        bullet.x += 10
def destroy_bullets_on_exit(world: World):
    """ Destroy any water drops that have landed on the ground """
    bullets_kept = []
    for bullet in world.bullets:
        if bullet.x < get_width():
            bullets_kept.append(bullet)
        else:
            destroy(bullet)
    world.bullets = bullets_kept
def move_spaceship(world: World, key: str):
        world.spaceship.y += world.spaceship_speed
        if world.spaceship.y >= get_height():
            world.spaceship.y = get_height() - 1
        elif world.spaceship.y <= 0:
            world.spaceship.y = 1

def control_spaceship_movement(world:World, key:str):
    if key == "up" and world.spaceship_speed > 0:
        world.spaceship_speed = -world.spaceship_speed
    elif key == "down" and world.spaceship_speed < 0:
        world.spaceship_speed = -world.spaceship_speed
when('starting', create_world)
when('updating', create_enemies)
when('updating', move_spaceship)
when('updating', move_enemies)
when('updating', move_bullets)
when('updating', destroy_bullets_on_exit)
when('typing', control_spaceship_movement)
when('typing', create_bullets)
start()