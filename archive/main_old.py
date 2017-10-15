#! /Users/iandanforth/tensorflow/bin/python
import sys
import numpy as np
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import random
import time

def add_ball(space):
    mass = 1
    radius = 14
    moment = pymunk.moment_for_circle(mass, 0, radius) # 1
    body = pymunk.Body(mass, moment) # 2
    x = random.randint(120, 380)
    body.position = x, 550 # 3
    shape = pymunk.Circle(body, radius) # 4
    space.add(body, shape) # 5
    return shape

def add_static_L(space):
    body = pymunk.Body(body_type = pymunk.Body.STATIC) # 1
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (255, 0), 5) # 2
    l2 = pymunk.Segment(body, (-150, 0), (-150, 50), 5)

    space.add(l1, l2) # 3
    return l1,l2

def draw_lines(screen, lines):
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle) # 1
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1) # 2
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

    ############### Arm
    space_center = (300, 300)

    # upper_arm_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    # upper_arm_body.position = space_center
    # upper_arm_body.angle = np.deg2rad(-45)
    # upper_arm_line = pymunk.Segment(upper_arm_body, (0, 0), (-200, 0), 5.0)
    # upper_arm_line.sensor = True # Disable collision
    # space.add(upper_arm_line)
 

    lower_arm_body = pymunk.Body(10, 10000, body_type=pymunk.Body.DYNAMIC)
    lower_arm_body.position = (300, 300)
    # lower_arm_body.angle = np.deg2rad(45)
    lower_arm_line = pymunk.Segment(lower_arm_body, (0, 0), (200, 0), 10.0)

    space.add(lower_arm_line)

    # rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    # rotation_center_body.position = (300, 300)
    # elbow_joint = pymunk.PinJoint(rotation_center_body, lower_arm_body, (0, 0), (0, 0))

    # space.add(elbow_joint)

    # stiffness = 100
    # damping = 100
    # # rotation_limit_spring = pymunk.DampedSpring(upper_arm_body, lower_arm_body, (-45, 45), (80, 0), 10.0, stiffness, damping)

    # space.add(upper_arm_line, lower_arm_body, lower_arm_box, elbow_joint)


    ############## L Shape
    # rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    # rotation_center_body.position = (300,300)

    # rotation_limit_body = pymunk.Body(body_type = pymunk.Body.STATIC) # 1
    # rotation_limit_body.position = (200,300)

    # body = pymunk.Body(10, 10000)
    # body.position = (300,300)
    # l1 = pymunk.Segment(body, (-150, 75), (150.0, -75.0), 5.0)
    # l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)

    # rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0))
    # joint_limit = 25

    # stiffness = 5
    # damping = 100
    # rotation_limit_spring = pymunk.DampedSpring(body, rotation_limit_body, (-100,0), (0,0), 10.0, stiffness, damping)
    # rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100,0), (0,0), 0, joint_limit) # 2

    # space.add(l1, l2, body, rotation_center_joint, rotation_limit_spring)


    #######################
    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        space.step(1/50.0)

        screen.fill((255,255,255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        
        clock.tick(50)

if __name__ == '__main__':
    main()
