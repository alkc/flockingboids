#!/usr/bin/env python3

import argparse
import pygame
from ecosystem import BoidEcosystem
from printers import BoidMetrics
from setup import BoidSettings

'''
This is a pygame program that simulates the
evolution of flocking behavior in a population of
boids when facing a population of predators.
'''

programVersion = "pyFlockingEvolution v0.6.4"

'''
In the dictionary below, all the important
and tweakable settings and parameters of the
simulation are defined and passed to the
BoidSettings class, which configures the other
classes used by the simulation.
'''

settings = {
    'simulationID': "AlexSim03",
    'endlessSimulation': True,
    'maxGenerationNbr': 1000,
    'nbrOfKillsBeforeReset': 10,

    # Headless mode can be toggled by pressing H
    'headless': False,

    # Habitat and pygame display dimensions
    'habitatWidth': 700,
    'habitatHeight': 700,

    # Population sizes
    'nbrOfBoids': 75,
    'nbrOfPredators': 3,

    # Boid (prey) parameters
    'maxBoidVelocity': 2.0,
    'minBoidVelocity': 0.50,
    'minNeighborDist': 10.0,
    'maxBoidForce': 0.30,
    'perceptionRadius': 30.0,
    'fov': 270.0,  # Degrees; 360 gives all-around vision

    # Predator parameters
    # Movement
    'minPredatorNeighborDistance': 10.0,
    'maxPredatorVelocity': 2.05,
    'minPredatorVelocity': 0.50,
    'maxPredatorForce': 0.30,
    'predatorPerceptionRadius': 180.0,
    'predatorFov': 180.0,
    # Rest after successful hunt
    'restAfterKill': True,
    'killRadius': 4.0,
    'huntingInterval': 25.0,

    # Kill and collision parameters

    # Slowdown collision penalty
    'slowDownTimer': 20.0,

    # Collision between boids can result in death
    'deadlyCollisions': True,

    # Nbr of collisions resulting in death
    'maxNbrOfCollisions': 1,
    'collisionRadius': 4.0,

    # Evolutionary algorithm parameters
    'mutationRate': 0.005,
    'mutationSize': 0.75,
    'crossoverRate': 0.0147,  # Currently not implemented
    'maxInitialGeneValues': 0.0,  # Set to 0.0 for no initial flocking behavior
    'maxInitialColorGeneValues': 5.1,  # Color values from 0 to 5.1 map to RGB 0 to 255
    'independentSegregation': True,  # Broken as of v0.5

    # Graphics settings
    'drawVelocityVector': False,  # Toggle with V key
    'drawBoidMinimumDistance': False,  # Toggle with R key
    'drawBoidPerceptionRadius': False,
    'drawPredatorMinimumDistance': False,
    'drawPredatorPerceptionRadius': False,

    # Pygame settings
    'bgColor': (125, 125, 125),
    'winWidth': 700,  # Not implemented
    'winHeight': 700,  # Not implemented
    'windowTitle': "pyFlockingEvolution v0.6.4",

    # Printer settings (Not yet implemented)
    'debugLog': True,
    'debugLogToFile': True,
    'killLog': True,
    'printPerNthGen': 5,
    'printOrderPerNthTick': 50
}

parser = argparse.ArgumentParser(description="Run the flocking boids simulation")
parser.add_argument("--headless", action="store_true", help="run without a pygame window")
parser.add_argument("--max-steps", type=int, help="stop after this many simulation steps")
parser.add_argument("--max-generations", type=int, help="stop after this many generation advances")
args = parser.parse_args()

if args.max_steps is not None and args.max_steps < 1:
    parser.error("--max-steps must be at least 1")
if args.max_generations is not None and args.max_generations < 1:
    parser.error("--max-generations must be at least 1")

if args.headless:
    settings['headless'] = True
if args.max_generations is not None:
    settings['endlessSimulation'] = False
    settings['maxGenerationNbr'] = args.max_generations

'''
SETUP BLOCK
'''

display = None
windowTitle = "{} : {}".format(programVersion, settings['simulationID'])

if settings['headless'] is False:
    pygame.init()
    clock = pygame.time.Clock()
    dimensions = (settings['habitatWidth'], settings['habitatHeight'])
    display = pygame.display.set_mode(dimensions)
    pygame.display.set_caption(windowTitle)

settings['display'] = display

BoidSettings.setup(settings)
BoidEcosystem.createEcosystem()

runSimulation = True
steps = 0
bgColor = settings['bgColor']
exitStatus = 'stopped'

'''
DRAW BLOCK
'''

try:
    while runSimulation:
        if len(BoidEcosystem.boids) < 2:
            exitStatus = 'extinct'
            print('[EXTINCTION] Fewer than two boids remain; breeding cannot continue.')
            break

        if BoidSettings.headless is False or pygame.display.get_init() > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if (BoidEcosystem.totalNbrOfKills >=
                            BoidEcosystem.nbrOfKillsBeforeReset):
                        exitStatus = 'complete'
                    runSimulation = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    BoidSettings.toggleHeadlessMode()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    BoidSettings.toggleRadiusDraw()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                    BoidSettings.toggleVelocityVector()

        if not runSimulation:
            break

        # If kill-threshold is reached, advance to next gen
        if BoidEcosystem.totalNbrOfKills >= BoidEcosystem.nbrOfKillsBeforeReset:
            if BoidSettings.endSimulation():
                exitStatus = 'complete'
                break
            if not BoidEcosystem.advanceGeneration():
                exitStatus = 'extinct'
                print('[EXTINCTION] Fewer than two boids remain; breeding cannot continue.')
                break

        if BoidSettings.headless is False:
            display.fill(bgColor)

        BoidEcosystem.step()
        steps += 1

        if len(BoidEcosystem.boids) < 2:
            exitStatus = 'extinct'
            print('[EXTINCTION] Fewer than two boids remain; breeding cannot continue.')
            break

        if args.max_steps is not None and steps >= args.max_steps:
            exitStatus = (
                'complete' if BoidEcosystem.totalNbrOfKills >=
                BoidEcosystem.nbrOfKillsBeforeReset else 'stopped'
            )
            runSimulation = False

        if BoidSettings.headless is False:
            pygame.display.update()
except KeyboardInterrupt:
    print('[EXIT] Interrupted.')
finally:
    try:
        BoidEcosystem.finishGeneration(exitStatus)
    finally:
        BoidMetrics.close()
        pygame.quit()

# Exit the program
print('[EXIT] Bye.')
