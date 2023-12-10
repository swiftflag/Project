from dataclasses import dataclass
from designer import *
from random import randint
#make sure that the screen looks appropriately space-y
set_window_color("black")
set_window_layers(['stars', 'planet','bullets','powerups','enemies','spaceship'])
@dataclass
class Enemy_Movement:
    movement_angle: int
    rotate_up: int
class Spaceship(image):
    speed: int
    is_moving_up: bool
    is_moving_down: bool
class Bullet(rectangle):
    speed: int
class Enemy(emoji):
    speed:int
    move_class: Enemy_Movement
class Powerup(image):
    speed: int
    powerup_type: int


@dataclass
class World:
    spaceship: Spaceship
    bullets: list[Bullet]
    enemies: list[Enemy]
    spawn_timer: int
    stars: list[DesignerObject]
    star_speed: int
    score: int
    score_counter: DesignerObject
    lives: int
    lives_counter: DesignerObject
    Earth: DesignerObject
    powerups: list[Powerup]
    powerup_spawn_rate: int
    powerup_timer: int

def create_world() -> World:
    return World(prepare_spaceship(),[],[],135, [], 20,0, text("red","Score: 0", 20,get_width()/2, 20),10,text("green","Lives: 10", 20,(get_width()/2) + 100, 20),create_earth(),[], 500, -1)
def create_earth() -> DesignerObject:
    earth = image('Earth.png')
    earth.y = get_height()/2
    earth.x = -150
    earth.layer = 'planet'
    return earth
def prepare_spaceship():
    #this function creates the spaceship and give its original position, also rotates it to get it looking right
    spaceship = Spaceship('Space_fighter.png', speed = 10, is_moving_up = False, is_moving_down = False)
    turn_right(spaceship, 90)
    shrink(spaceship, 4)
    spaceship.x = 30
    spaceship.y = get_height()/2
    spaceship.layer = 'spaceship'
    return spaceship
def create_stars(world: World):
    star = circle("white", 4)
    star.layer = 'stars'
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
spawn_rate = 100
def create_enemies(world: World):
    world.spawn_timer += 1
    global spawn_rate
    #this if statement right here makes it so that the rate of enemy spawns scales up slowly over time
    #it also caps it at a number where it is very difficult but not impossible to eliminate all enemies
    if (world.spawn_timer % 500) == 0 and spawn_rate > 10:
        spawn_rate = spawn_rate - 10
    if (world.spawn_timer % spawn_rate) == 0:
        create_one_enemy(world)

def create_one_enemy(world:World):
    enemy = Enemy('Flying Saucer', speed = 5, move_class = Enemy_Movement(randint(135, 225), randint(0, 1)))
    enemy.x = get_width()
    enemy.y = randint(0, get_height())
    world.enemies.append(enemy)


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
def change_angle(enemy: Enemy, world: World):
    #this is a wild one for sure, but essentially it makes the spaceships move in wavy patterns
    #by rotating their direction of movement
    if enemy.move_class.movement_angle < 135:
        enemy.move_class.movement_angle = 135
        enemy.move_class.rotate_up = 1
    elif enemy.move_class.movement_angle > 225:
        enemy.move_class.movement_angle = 225
        enemy.move_class.rotate_up = 0
    if enemy.move_class.rotate_up == 1:
        enemy.move_class.movement_angle += 1
    else:
        enemy.move_class.movement_angle -= 1
def move_enemies(world: World):
    #this moves the enemies but also caps their height so they cant go off-screen
    for enemy in world.enemies:
        move_forward(enemy, enemy.speed, enemy.move_class.movement_angle)
        change_angle(enemy, world)
        if enemy.y < 0:
            enemy.y = 0
        elif enemy.y > get_height():
            enemy.y = get_height()

def create_bullets_on_space(world: World, key: str):
    if key == 'space':
        create_single_bullet(world)
def create_single_bullet(world: World):
    bullet = Bullet("red", 20, 5, world.spaceship.x + 20, world.spaceship.y, speed=15)
    bullet.layer = 'bullets'
    world.bullets.append(bullet)
def move_bullets(world: World):
    for bullet in world.bullets:
        bullet.x += bullet.speed
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
    if world.spaceship.is_moving_up:
        world.spaceship.y += -world.spaceship.speed
    if world.spaceship.is_moving_down:
        world.spaceship.y += world.spaceship.speed
    if world.spaceship.y >= get_height():
        world.spaceship.y = get_height() - 1
    elif world.spaceship.y <= 0:
        world.spaceship.y = 1

def start_spaceship_movement(world:World, key:str):
    if key == "up":
        world.spaceship.is_moving_up = True
    elif key == "down":
        world.spaceship.is_moving_down = True
def end_spaceship_movement(world:World, key:str):
    if key == "up":
        world.spaceship.is_moving_up = False
    if key == "down":
        world.spaceship.is_moving_down = False

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
def filter_from(old_list: list[DesignerObject], removal_list: list[DesignerObject]) -> list[DesignerObject]:
    #this is a helper function that sorts through a list of designer objects, destroys any that match
    #those that have collided, appends a new list with those that have not collided and returns that new list
    kept_objects = []
    for object in old_list:
        if object in removal_list:
            destroy(object)
        else:
            kept_objects.append(object)
    return kept_objects
def create_powerup(world: World):
    if (world.spawn_timer % 150) == 0 and world.powerup_spawn_rate > 100:
        world.powerup_spawn_rate = world.powerup_spawn_rate - 100
    if (world.spawn_timer % world.powerup_spawn_rate) == 0:
        create_one_powerup(world)
def move_powerups(world: World):
    for powerup in world.powerups:
        move_forward(powerup, powerup.speed)

def create_one_powerup(world:World):
    powerup = Powerup('Gear_powerup.png', speed = -5, powerup_type = 0)
    shrink(powerup, 30)
    powerup.x = get_width()
    powerup.y = randint(0, get_height())
    world.powerups.append(powerup)
def destroy_powerups_on_exit(world: World):
    #destroys bullets when they hit the edge of the screen
    powerups_kept = []
    for powerup in world.powerups:
        if powerup.x > -50:
            powerups_kept.append(powerup)
        else:
            destroy(powerup)
    world.powerups = powerups_kept
def player_powerup_collision(world: World):
    destroyed_powerups = []
    for powerup in world.powerups:
        if colliding(world.spaceship, powerup):
            destroyed_powerups.append(powerup)
            world.powerup_timer = 150
    world.powerups = filter_from(world.powerups, destroyed_powerups)
def powerup_handler(world:World):
    world.powerup_timer -= 1
    if world.powerup_timer > 0:
        create_single_bullet(world)

def Game_Over(world: World):
    if world.lives <= 0:
        text("red", "GAME OVER", 50, get_width() / 2, get_height()/2)
        explosion = emoji("collision_symbol")
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
when('updating', move_powerups)
when('updating', destroy_enemies_on_exit)
when('updating', destroy_bullets_on_exit)
when('updating', destroy_powerups_on_exit)
when('updating', enemy_bullet_collision)
when('updating', player_powerup_collision)
when('updating', create_powerup)
when('updating', powerup_handler)
when('typing', start_spaceship_movement)
when('done typing', end_spaceship_movement)
when('typing', create_bullets_on_space)
when(Game_Over, pause)
start()