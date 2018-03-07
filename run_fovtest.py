#!/usr/bin/python

'''
This is my lame attempt to figure out how to implement
a proper field of vision in the boids

press key 'U' on the keyboard while the program runs
to generate a random "boid"
'''

import random
from vector import Vector2D as Vec
import pygame
from math import *

pygame.init()
display = pygame.display.set_mode((500,500))
center = Vec(250, 250)
pygame.display.set_caption("pygame sector test")

runGame = True

points = []

for n in range(400):
    x = random.randint(0,500)
    y = random.randint(0,500)

    points.append(Vec(x,y))

class SimpleBoid:

    fov = 270.0
    detectionRadius = 50.0


    def __init__(self):

        self.velocity = self.getRandomVelocity()
        self.position = self.getRandomPosition()
        self.orientation  = self.velocity.normalized()
        self.sectorArms = []

    def constructSector(self):

        self.sectorArms = []

        sectorStart = Vec(0,0)
        sectorEnd = Vec(0,0)

        sectorStart = self.orientation.transform(-SimpleBoid.fov/2)
        sectorEnd = self.orientation.transform(SimpleBoid.fov/2)

        self.sectorArms.append(sectorStart)
        self.sectorArms.append(sectorEnd)

    def getRandomPosition(self):

        x = random.randint(0, 500)
        y = random.randint(0, 500)

        return Vec(x,y)

    def getRandomVelocity(self):

        x = random.randint(-2, 2)
        y = random.randint(-2, 2)

        print x, y
        
        return Vec(x,y)
   
   
    def isInsideSector(self, otherBoid):
   
        relPoint = Vec(
            point.x - boid.position.x,
            point.y - boid.position.y
        )

        return relPoint.isClockwiseTo(self.sectorArms[0]) and not relPoint.isClockwiseTo(self.sectorArms[1])  

    

boid = SimpleBoid()
boid.constructSector()
    
while runGame:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # Exit this loop
            runGame = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            # On keypress U:
            boid = SimpleBoid()
            boid.constructSector()

    display.fill((80,80,80))
   
    for point in points:
        if point.distanceTo(boid.position) <= boid.detectionRadius and boid.isInsideSector(point):
            pygame.draw.circle(display, (0, 255, 255), point.getXY(), 2, 1)
        else:
            pygame.draw.circle(display, (20, 20, 20), point.getXY(), 2, 1)

    position = boid.position.getXY(_type='int')
    orientationLine = boid.orientation.multScalar(boid.detectionRadius).addVec(boid.position)
    sectorStartPos = boid.sectorArms[0].multScalar(boid.detectionRadius).addVec(boid.position)
    sectorEndPos = boid.sectorArms[1].multScalar(boid.detectionRadius).addVec(boid.position)

    pygame.draw.line(display, (255, 255, 255), position, orientationLine.getXY(_type='int'), 1)
    pygame.draw.line(display, (0, 255, 0), position, sectorStartPos.getXY(_type='int'), 1)
    pygame.draw.line(display, (255, 0, 0), position, sectorEndPos.getXY(_type='int'), 1)
    pygame.draw.circle(display, (255, 255, 255), boid.position.getXY(_type='int'), int(boid.detectionRadius), 1)
    pygame.display.update()
        

pygame.quit()
quit()
