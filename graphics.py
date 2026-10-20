#!/usr/bin/python

from math import atan2, cos, hypot, radians, sin

import pygame
from critters import Boid, PredatorBoid


class BoidGraphics:

    # Switches for the range and vision outlines around boids
    drawBoidMinDistance = None
    drawBoidPerceptionRadius = None
    drawPredatorMinDistance = None
    drawPredatorPerceptionRadius = None
    drawVelocityVector = None

    predatorMinDistance = None
    boidMinDistance = None
    boidPerceptionRadius = None
    boidFov = None
    predatorPerceptionRadius = None
    predatorFov = None

    # Colors:
    boidMinDistanceColor = (255, 255, 0)         # White
    boidPerceptionRadiusColor = (255, 255, 255)  # Yellow
    predatorMinDistanceColor = (255, 0, 0)       # Blood red
    predatorPerceptionColor = (255, 140, 70)

    # Headless
    headlessMode = None

    # pygame display
    display = None

    @staticmethod
    def _drawVisionCone(boid, radius, fov, color):
        center = (round(boid.position.x), round(boid.position.y))
        speed = hypot(boid.velocity.x, boid.velocity.y)
        if fov >= 360 or speed == 0:
            pygame.draw.circle(BoidGraphics.display, color, center, radius, 1)
            return

        heading = atan2(boid.velocity.y, boid.velocity.x)
        span = radians(fov)
        start = heading - span / 2
        segments = max(8, round(fov / 10))
        points = [center]
        for step in range(segments + 1):
            angle = start + span * step / segments
            points.append((round(center[0] + radius * cos(angle)),
                           round(center[1] + radius * sin(angle))))
        points.append(center)
        pygame.draw.lines(BoidGraphics.display, color, False, points, 1)

    @staticmethod
    def _trianglePoints(boid, front, back, halfWidth):
        speed = hypot(boid.velocity.x, boid.velocity.y)
        if speed:
            forwardX = boid.velocity.x / speed
            forwardY = boid.velocity.y / speed
        else:
            forwardX, forwardY = 0.0, -1.0

        sideX, sideY = -forwardY, forwardX
        x, y = boid.position.x, boid.position.y
        return [
            (round(x + forwardX * front), round(y + forwardY * front)),
            (round(x - forwardX * back + sideX * halfWidth),
             round(y - forwardY * back + sideY * halfWidth)),
            (round(x - forwardX * back - sideX * halfWidth),
             round(y - forwardY * back - sideY * halfWidth)),
        ]

    @staticmethod
    def drawBoid(boid):

        if BoidGraphics.headlessMode is True:
            return

        renderPos = (int(boid.position.x), int(boid.position.y))

        if isinstance(boid, Boid):

            if BoidGraphics.drawBoidPerceptionRadius:

                try:
                    BoidGraphics._drawVisionCone(
                        boid, BoidGraphics.boidPerceptionRadius,
                        BoidGraphics.boidFov,
                        BoidGraphics.boidPerceptionRadiusColor)
                except Exception as e:
                    print("[ERROR] Could not draw perception radius at pos {}:".format(renderPos), e)
            if BoidGraphics.drawBoidMinDistance:
                try:
                    pygame.draw.circle(BoidGraphics.display,
                                       BoidGraphics.boidMinDistanceColor,
                                       renderPos,
                                       BoidGraphics.boidMinDistance, 1)
                except Exception as e:
                    print("[ERROR] Could not draw minimum distance radius at pos {}:".format(renderPos), e)

        if isinstance(boid, PredatorBoid):

            if BoidGraphics.drawPredatorPerceptionRadius:
                try:
                    BoidGraphics._drawVisionCone(
                        boid, BoidGraphics.predatorPerceptionRadius,
                        BoidGraphics.predatorFov,
                        BoidGraphics.predatorPerceptionColor)
                except Exception as e:
                    print("[ERROR] Could not draw predator vision at pos {}:".format(renderPos), e)

            if BoidGraphics.drawPredatorMinDistance:

                try:
                    pygame.draw.circle(
                        BoidGraphics.display,
                        BoidGraphics.predatorMinDistanceColor,
                        renderPos, BoidGraphics.predatorMinDistance, 1)
                except Exception as e:
                    print("[ERROR] Could not draw predator minimum distance at position {}:".format(renderPos), e)
        try:
            size = (11, 7, 6) if isinstance(boid, PredatorBoid) else (8, 5, 4)
            pygame.draw.polygon(
                BoidGraphics.display,
                boid.color,
                BoidGraphics._trianglePoints(boid, *size))
        except Exception as e:
            print("[ERROR] Could not draw boid at pos {}:".format(renderPos), e)

        if BoidGraphics.drawVelocityVector is True:
                renderLine = boid.position.addVec(
                    boid.velocity.multScalar(3.0)).getXY()
                try:
                    pygame.draw.line(
                        BoidGraphics.display,
                        (255, 255, 255),
                        renderPos, renderLine, 1)
                except Exception as e:
                    print("[ERROR] Could not draw speed vector at pos {}:".format(renderPos), e)
