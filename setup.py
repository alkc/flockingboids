#!/usr/bin/python

'''
BoidSettings is a helper class made to configure 
the other classes. In the future it will be expanded 
to read a list of settings from file, so simulations 
can be run automatically, without having to manually
tweak run.py each time.
'''

from graphics import BoidGraphics
from genetics import BoidGenetics
from behavior import BoidBehavior, PredatorBehavior
from ecosystem import BoidEcosystem
from printers import BoidMetrics

class BoidSettings:

    pygameDisplay = None
    headless = None
    settings = None

    # The main method takes a dictionary of settings
    # and distributes the values
    @staticmethod
    def setup(settings):

        BoidSettings.settings = settings

        BoidSettings._setupDisplay()
        BoidSettings._setupGraphics()
        BoidSettings._setupHabitat()
        BoidSettings._setupPopulations()
        BoidSettings._setupBoidBehavior()

        BoidSettings._setupPredatorBehavior()
        BoidSettings._setupKillParams()
        BoidSettings._setupBoidGenomes()
        BoidSettings._setupGeneticAlgorithm()
        BoidSettings._setupPrinters()

    @staticmethod
    def _setupDisplay():
        
        BoidGraphics.display = BoidSettings.settings['display']
        BoidGraphics.headlessMode = BoidSettings.settings['headless']
        BoidSettings.headless = BoidSettings.settings['headless']

    @staticmethod
    def _setupGraphics():

        BoidGraphics.drawBoidMinDistance = BoidSettings.settings['drawBoidMinimumDistance']
        BoidGraphics.drawBoidPerceptionRadius = BoidSettings.settings['drawBoidPerceptionRadius']
        BoidGraphics.drawPredatorMinDistance = BoidSettings.settings['drawPredatorMinimumDistance']
        BoidGraphics.drawVelocityVector = BoidSettings.settings['drawVelocityVector']

        BoidGraphics.boidMinDistance =  int(BoidSettings.settings['minNeighborDist'])
        BoidGraphics.boidPerceptionRadius =  int(BoidSettings.settings['perceptionRadius'])
        BoidGraphics.predatorMinDistance =  int(BoidSettings.settings['minPredatorNeighborDistance'])
        

    @staticmethod
    def _setupHabitat():
        BoidEcosystem.habitatWidth = BoidSettings.settings['habitatWidth']
        BoidEcosystem.habitatHeight = BoidSettings.settings['habitatHeight']
        BoidBehavior.maxWidth= BoidSettings.settings['habitatWidth']
        BoidBehavior.maxHeight= BoidSettings.settings['habitatHeight']
        
    @staticmethod
    def _setupBoidBehavior():

        BoidBehavior.maxVelocity = BoidSettings.settings['maxBoidVelocity']
        BoidBehavior.minVelocity = BoidSettings.settings['minBoidVelocity']
        BoidBehavior.maxForce = BoidSettings.settings['maxBoidForce']
        BoidBehavior.perceptionRadius = BoidSettings.settings['perceptionRadius']
        BoidBehavior.neighborDistance = BoidSettings.settings['minNeighborDist']
        BoidBehavior.maxSlowdownTime = BoidSettings.settings['slowDownTimer']
        BoidBehavior.fov = BoidSettings.settings['fov']

    @staticmethod
    def _setupPredatorBehavior():

        PredatorBehavior.killRadius = BoidSettings.settings['killRadius']
        PredatorBehavior.maxVelocity = BoidSettings.settings['maxPredatorVelocity']
        PredatorBehavior.minVelocity = BoidSettings.settings['minPredatorVelocity']
        PredatorBehavior.minDistance = BoidSettings.settings['minPredatorNeighborDistance']
        PredatorBehavior.maxForce = BoidSettings.settings['maxPredatorForce']
        PredatorBehavior.restAfterKill = BoidSettings.settings['restAfterKill']
        PredatorBehavior.maxKillTimeout = BoidSettings.settings['huntingInterval']

    @staticmethod
    def _setupKillParams():

        BoidEcosystem.nbrOfKillsBeforeReset = BoidSettings.settings['nbrOfKillsBeforeReset']
        BoidEcosystem.deadlyCollisions = BoidSettings.settings['deadlyCollisions']
        BoidEcosystem.maxNbrOfCollisions = BoidSettings.settings['maxNbrOfCollisions']
        BoidEcosystem.collisionRadius = BoidSettings.settings['collisionRadius']
    @staticmethod
    def _setupBoidGenomes():
        # BoidEcosystem.nbrOfLoci = BoidSettings.settings['nbrOfLoci']
        BoidEcosystem.maxInitialGeneVal = BoidSettings.settings['maxInitialGeneValues']

    @staticmethod
    def _setupGeneticAlgorithm():
        BoidGenetics.mutRate = BoidSettings.settings['mutationRate'] 
        BoidGenetics.maxMutationSize = BoidSettings.settings['mutationSize'] 
        BoidGenetics.crossoverRate = BoidSettings.settings['crossoverRate'] 
        BoidGenetics.independentSegregation = BoidSettings.settings['independentSegregation']

    @staticmethod
    def _setupPopulations():
        BoidEcosystem.nbrOfBoids = BoidSettings.settings['nbrOfBoids']
        BoidEcosystem.nbrOfPredators = BoidSettings.settings['nbrOfPredators']

        
    @staticmethod
    def _setupPrinters():
        BoidMetrics.init(BoidSettings.settings['simulationID'])
        BoidMetrics.printSettings(BoidSettings.settings)
        BoidEcosystem.printPerNthGen = BoidSettings.settings['printPerNthGen']
        BoidMetrics.printPerNthGen = BoidSettings.settings['printPerNthGen']
        BoidBehavior.printOrderPerNthTick = BoidSettings.settings['printOrderPerNthTick']

    @staticmethod
    def toggleHeadlessMode():
        BoidSettings.headless = not BoidSettings.headless
        BoidGraphics.headlessMode = not BoidGraphics.headlessMode

    @staticmethod
    def toggleRadiusDraw():

        toggle = not BoidGraphics.drawBoidMinDistance
        BoidGraphics.drawBoidMinDistance = toggle
        BoidGraphics.drawBoidPerceptionRadius = toggle
        BoidGraphics.drawPredatorMinDistance = toggle

    @staticmethod
    def toggleVelocityVector():

        toggle = not BoidGraphics.drawVelocityVector
        BoidGraphics.drawVelocityVector = toggle

    @staticmethod
    def endSimulation():
        
        isFinite = not BoidSettings.settings['endlessSimulation']
        maxGenReached = BoidSettings.settings['maxGenerationNbr'] < BoidEcosystem.currentGeneration
        
        return isFinite and maxGenReached
