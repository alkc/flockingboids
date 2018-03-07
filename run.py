#!/usr/bin/python

import pygame
from ecosystem import BoidEcosystem
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
    'description': "mutRate = 0.0005, 10 kills before reset, deadly collisions, no predators",
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
    'fov': 270.0,  # Degrees, not implemented

    # Predator parameters
    # Movement
    'minPredatorNeighborDistance': 10.0,
    'maxPredatorVelocity': 2.05,
    'minPredatorVelocity': 0.50,
    'maxPredatorForce': 0.30,
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
    'independentSegregation': True,  # Broken as of v0.5

    # Graphics settings
    'drawVelocityVector': False,  # Toggle with V key
    'drawBoidMinimumDistance': False,  # Toggle with R key
    'drawBoidPerceptionRadius': False,
    'drawPredatorMinimumDistance': False,

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
bgColor = settings['bgColor']

'''
DRAW BLOCK
'''

while runSimulation:

    if BoidSettings.headless is False or pygame.display.get_init() > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit this loop
                runSimulation = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                # On keypress H:
                BoidSettings.toggleHeadlessMode()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # On keypress R:
                BoidSettings.toggleRadiusDraw()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                # On keypress V:
                BoidSettings.toggleVelocityVector()

    # If kill-threshold is reached, advance to next gen
    if BoidEcosystem.totalNbrOfKills >= BoidEcosystem.nbrOfKillsBeforeReset:

        if BoidSettings.endSimulation():
            runSimulation = False
            continue

        BoidEcosystem.advanceGeneration()

    if BoidSettings.headless is False:
        # Wipe the display clean
        display.fill(bgColor)

    # Advance the simulation one step
    BoidEcosystem.step()

    if BoidSettings.headless is False:
        # Render everything anew:
        pygame.display.update()

        # Comment this out to remove the fps limit:
        # clock.tick(60)

# Exit pygame
pygame.quit()

# Exit the program
exit('[EXIT] Bye.')
