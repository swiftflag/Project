from dataclasses import dataclass
from designer import *
from random import randint
#make sure that the screen looks appropriately space-y
set_window_color("black")
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
    stars: list[DesignerObject]
    star_speed: int
    score: int
    score_counter: DesignerObject
    lives: int
    lives_counter: DesignerObject


def create_world() -> World:
    return World(create_spaceship(), 10, 15, [],[], 5,135, [], [], 20,0, text("red","Score: 0", 20,get_width()/2, 20),10,text("green","Lives: 10", 20,(get_width()/2) + 100, 20))
def create_spaceship() -> DesignerObject:
    #this function creates the spaceship and give its original position, also rotates it to get it looking right
    spaceship = emoji("Rocket")
    turn_right(spaceship, 45)
    spaceship.x = 30
    spaceship.y = get_height()/2
    return spaceship
def create_stars(world: World) -> DesignerObject:
    star = circle("white", 4)
    star.x = get_width() + 20
    star.y = randint(0, get_height())
    world.stars.append(star)
def move_star(world: World):
    for star in world.stars:
        move_forward(star, world.star_speed, 180)
def destroy_stars_on_exit(world: World):
    #destroys the stars in world.stars that are a bit beyond the left border of the screen
    stars_kept = []
    for star in world.stars:
        if star.x > -20:
            stars_kept.append(star)
        else:
            destroy(star)
    world.stars = stars_kept
spawn_rate = 10
def create_enemies(world: World) -> DesignerObject:
    world.spawn_timer += 1
    global spawn_rate
    #this if statement right here makes it so that the rate of enemy spawns scales up slowly over time
    #it also caps it at a number where it is very difficult but not impossible to eliminate all enemies
    if (world.spawn_timer % 50) == 0 and spawn_rate > 10:
        spawn_rate = spawn_rate - 10
    if (world.spawn_timer % spawn_rate) == 0:
        create_one_enemy(world)

def create_one_enemy(world:World) -> DesignerObject:
    enemy = emoji("Flying Saucer")
    enemy.x = get_width()
    enemy.y = randint(0, get_height())
    world.enemies.append(enemy)
    world.enemy_movement_angles.append(Enemy_Movement(randint(135, 225), randint(0, 1)))

def destroy_enemies_on_exit(world: World):
    # destroys the  in enemies in world.enemies that are a bit beyond the left border of the screen
    enemies_kept = []
    for enemy in world.enemies:
        if enemy.x > -20:
            enemies_kept.append(enemy)
        else:
            destroy(enemy)
            world.lives += -1
            world.lives_counter.text = "Lives: " + str(world.lives)

    world.enemies = enemies_kept
def change_angle(enemy_num: int, world: World):
    #this is a wild one for sure, but essentially it makes the spaceships move in wavy patterns
    #by rotating their direction of movement
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
    #this moves the enemies but also caps their height so they cant go off screen
    for enemy_num, enemy in enumerate(world.enemies):
        move_forward(enemy, world.enemy_speed, (world.enemy_movement_angles[enemy_num].movement_angle))
        change_angle(enemy_num, world)
        if enemy.y < 0:
            enemy.y = 0
        elif enemy.y > get_height():
            enemy.y = get_height()

def create_bullets(world: World, key: str) -> DesignerObject:
    if key == 'space':
        bullet = rectangle("red", 20, 5, world.spaceship.x + 20, world.spaceship.y)
        world.bullets.append(bullet)
        return bullet

def move_bullets(world: World):
    for bullet in world.bullets:
        bullet.x += world.bullet_speed
def destroy_bullets_on_exit(world: World):
    #destroys bullets when they hit the edge of the screen
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
def enemy_bullet_collision(world: World):
    #makes it so enemies and bullets collide and destroy each other
    #also increases score and updates the text counter when that happens
    destroyed_enemies = []
    destroyed_bullets = []
    # Compare every bullet to every enemy
    for bullet in world.bullets:
        for enemy in world.enemies:
            if colliding(bullet, enemy):
                destroyed_bullets.append(bullet)
                destroyed_enemies.append(enemy)
                world.score += 1
                world.score_counter.text = "Score: " + str(world.score)
    world.bullets = filter_from(world.bullets, destroyed_bullets)
    world.enemies = filter_from(world.enemies, destroyed_enemies)
def filter_from(old_enemy_list: list[DesignerObject], destroyed_enemy_list: list[DesignerObject]) -> list[DesignerObject]:
    #this is a helper function that sorts through a list of designer objects, destroys any that match
    #those that have collided, appends a new list with those that have not collided and returns that new list
    kept_enemies = []
    for enemy in old_enemy_list:
        if enemy in destroyed_enemy_list:
            destroy(enemy)
        else:
            kept_enemies.append(enemy)
    return kept_enemies
def Game_Over(world: World):
    if world.lives <= 0:
        text("red", "GAME OVER", 50, get_width() / 2, get_height()/2)
        explosion = emoji("fire")
        explosion.scale += 1
        explosion.y = world.spaceship.y - 10
        explosion.x = world.spaceship.x
        return True
when('starting', create_world)
when('updating', create_enemies)
when('updating', create_stars)
when('updating', move_star)
when('updating', destroy_stars_on_exit)
when('updating', move_spaceship)
when('updating', move_enemies)
when('updating', move_bullets)
when('updating', destroy_enemies_on_exit)
when('updating', destroy_bullets_on_exit)
when('updating', enemy_bullet_collision)
when('typing', control_spaceship_movement)
when('typing', create_bullets)
when(Game_Over, pause)
start()