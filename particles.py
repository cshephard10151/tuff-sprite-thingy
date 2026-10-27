import pygame as pg
from random import randint, uniform

GRAVITY = 9.81
SPEED_MULT = 10.0

class particle():
    def __init__(self, posx, posy, size, vel_x = 20.0, vel_y = 60.0):
        self.position = [posx, posy]
        self.velocity = [uniform(-vel_x, vel_x), uniform(-vel_y, -vel_y + vel_y / 2)]
        self.color =  pg.Color("#7CFC00") if randint(0, 1) == 0 else pg.Color("#00A86B")
        self.size = size
        self.decay_speed = uniform(.55, 1.2)

    def update_vel(self, dt):
        self.velocity[1] += GRAVITY * dt * SPEED_MULT

    def update_pos(self, dt):
        self.position[0] += self.velocity[0] * dt * SPEED_MULT
        self.position[1] += self.velocity[1] * dt * SPEED_MULT

    def update_size(self, dt):
        self.size -= self.decay_speed * dt * SPEED_MULT

    def update(self, dt):
        self.update_vel(dt)
        self.update_pos(dt)
        self.update_size(dt)

pg.init()
pg.mixer.init()

SCREEN_HEIGHT = 650
SCREEN_WIDTH = 900
pg.display.set_caption("Particle test")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pg.font.SysFont("arial", 36)
sprite_img = pg.image.load("assets/sprite.png").convert_alpha()
sprite_img = pg.transform.scale(sprite_img, (sprite_img.get_width() / 5, sprite_img.get_height() / 5))
sprite_sound = pg.mixer.Sound("assets/soda_sound.wav")
sprite_sound.set_volume(.2)
sprite_rect = sprite_img.get_rect(topleft = (500, 400))
clock = pg.time.Clock()

RUNNING = True

particle_group = []
spray_time = 0.0
while RUNNING:
    dt = clock.tick(150) / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            RUNNING = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                RUNNING = False

    clicks = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    screen.fill((55, 55, 55))

    sprite_rect.midtop = mouse_pos
    spray_mult = 1
    if clicks[0] or clicks[2]:
        if sprite_sound.get_num_channels() == 0:
            sprite_sound.play()
        spray_time += dt
        spray_mult = .5 + spray_time / 3
        spray_mult = pg.math.clamp(spray_mult, 0.5, 2.0)
        for _ in range(int(4 * spray_mult)):
            particle_group.append(particle(
                sprite_rect.midtop[0] + randint(-5, 5), 
                sprite_rect.midtop[1] + 7, 
                6.0, 20 * spray_mult, 
                60 * spray_mult))
    else: 
        spray_time = 0.0
        sprite_sound.fadeout(1000)

    for p in particle_group:
        p.update(dt)
        pg.draw.circle(screen, p.color, (pg.Vector2(p.position)), p.size)
        if p.size <= 0.0: particle_group.remove(p)

    screen.blit(font.render(str(round(clock.get_fps(), 2)), True, (255, 255, 255)), (100, 100))
    screen.blit(font.render(str(len(particle_group)), True, (255, 255, 255)), (300, 100))
    screen.blit(sprite_img, sprite_rect)
    pg.display.flip()

pg.quit()