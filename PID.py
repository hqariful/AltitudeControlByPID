import pygame
import pymunk
import math
import pymunk.pygame_util

pygame.init()
target = 400

kp = 5
kd = 5
ki = 7

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH,HEIGHT))

def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

def create_ball(space, radius, mass):
    body = pymunk.Body()
    body.position = (300, 30)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape

def refball(space, x, y):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (x, y)
    shape = pymunk.Circle(body, 5)
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape
 

def create_boundaries(space, width, height):
    rects = [
        [(width/2, height-10), (width, 20)], 
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height/2), (20, height)]
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps
    pressed_pos = pygame.mouse.get_pos()

    space = pymunk.Space()
    space.gravity = (0, 981)

    ball = create_ball(space, 30, 1)
    create_boundaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(window)
    isum = 0
    error = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_pos = pygame.mouse.get_pos()
        ypos = pressed_pos[1]
        perror = error
        error = ypos - ball.body.position.y
        
        d = (error-perror)/dt
        isum = isum + error*dt
        force = kp*error + ki*isum + kd*d
        ball.body.apply_force_at_local_point((0, 5*force), (0,0))
        draw(space, window, draw_options) 
        space.step(dt)  
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
