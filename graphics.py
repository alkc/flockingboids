#!/usr/bin/python

import pygame
from critters import Boid, PredatorBoid


class BoidGraphics:

    # Switches for the circles around boids
    drawBoidMinDistance = None
    drawBoidPerceptionRadius = None
    drawPredatorMinDistance = None
    drawVelocityVector = None

    predatorMinDistance = None
    boidMinDistance = None
    boidPerceptionRadius = None

    # Colors:
    boidMinDistanceColor = (255, 255, 0)         # White
    boidPerceptionRadiusColor = (255, 255, 255)  # Yellow
    predatorMinDistanceColor = (255, 0, 0)       # Blood red

    # Headless
    headlessMode = None

    # pygame display
    display = None

    @staticmethod
    def drawBoid(boid):

        if BoidGraphics.headlessMode is True:
            return

        renderPos = (int(boid.position.x), int(boid.position.y))

        if isinstance(boid, Boid):

            if BoidGraphics.drawBoidPerceptionRadius:

                try:
                    pygame.draw.circle(
                        BoidGraphics.display,
                        BoidGraphics.boidPerceptionRadiusColor,
                        renderPos, BoidGraphics.boidPerceptionRadius,
                        1)
                except Exception as e:
                    print "[ERROR] Could not draw perception radius at pos {}:".format(renderPos), e
            if BoidGraphics.drawBoidMinDistance:
                try:
                    pygame.draw.circle(BoidGraphics.display,
                                       BoidGraphics.boidMinDistanceColor,
                                       renderPos,
                                       BoidGraphics.boidMinDistance, 1)
                except Exception as e:
                    print "[ERROR] Could not draw minimum distance radius at pos {}:".format(renderPos) , e

        if isinstance(boid, PredatorBoid):

            if BoidGraphics.drawPredatorMinDistance:

                try:
                    pygame.draw.circle(
                        BoidGraphics.display,
                        BoidGraphics.predatorMinDistanceColor,
                        renderPos, BoidGraphics.predatorMinDistance, 1)
                except Exception as e:
                    print "[ERROR] Could not draw predator minimum distance at position {}:".format(renderPos),  e
        try:
            pygame.draw.circle(
                BoidGraphics.display,
                boid.color, renderPos, 2, 0)
        except Exception as e:
            print "[ERROR] Could not draw boid at pos {}:".format(renderPos), e

        if BoidGraphics.drawVelocityVector is True:
                renderLine = boid.position.addVec(
                    boid.velocity.multScalar(3.0)).getXY()
                try:
                    pygame.draw.line(
                        BoidGraphics.display,
                        (255, 255, 255),
                        renderPos, renderLine, 1)
                except Exception as e:
                    print "[ERROR] Could not draw speed vector at pos {}:".format(renderPos), e
