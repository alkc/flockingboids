#!/usr/bin/python

from critters import Boid, PredatorBoid
from behavior import BoidBehavior
from behavior import PredatorBehavior
from printers import BoidGazer as logbook
from printers import BoidMetrics as bStats
from genetics import BoidGenetics, Chromosome
from vector import Vector2D as Vec
import random

'''
BoidEcosystem is the main class for keeping track off and simulating the
Boid/Predator ecosystem

Contains functions for creating, repopulating a habitat, advancing the
simulation and kill/collission detection.
'''


class BoidEcosystem:

    # Population sizes
    nbrOfBoids = None
    nbrOfPredators = None

    # Boid genetic properties
    nbrOfLoci = 7
    maxInitialGeneVal = None

    # Flocks
    boids = []
    predators = []

    # Collissions
    deadlyCollisions = None
    maxNbrOfCollisions = None
    collisionRadius = None

    # Habitat vars
    habitatHeight = None
    habitatWidth = None
    colliTimeout = 10

    totalNbrOfKills = 0
    nbrOfKillsBeforeReset = None

    currentGeneration = 0
    printPerNthGen = None

    # The most important stuff:
    # Initialize the BoidEcosystem class.
    # Basically: start up the pygame display or set the program to headless
    # mode and initialize the stats printer.

    @staticmethod
    def init():
        # Initiate the stats printer (move this to settings?)
        bStats.init()

    # Advance the simulation one step
    @staticmethod
    def step():

        # Move all boids!
        BoidBehavior.moveBoids(BoidEcosystem.boids, BoidEcosystem.predators)

        # Move all predators
        PredatorBehavior.movePredators(
            BoidEcosystem.predators, BoidEcosystem.boids)

        # Slow down boids that fly into each other, and -- if deadly
        # collisions are enabled -- kill off repeat offenders.
        BoidEcosystem._checkForCollissions(BoidEcosystem.boids)

        # Check for and kill any hunted down boids.
        BoidEcosystem._checkForKills(
            BoidEcosystem.boids, BoidEcosystem.predators)

        bStats.ticker += 1

    # Breed a new population of boids from the previous generation
    # and spawn new predators
    @staticmethod
    def advanceGeneration():
        # Advance generation counter
        BoidEcosystem.currentGeneration += 1

        # This function is here to print info about how the
        # simulation is progressing to the terminal. The function
        # takes a string and an integer specifying the desired indent
        # of the output as input.

        logbook.log("[NEXT] Advancing to generation {}".format(
            BoidEcosystem.currentGeneration))

        # Note to self: combine this with currenGeneration
        # into separate function
        bStats.ticker = 0
        bStats.generation += 1

        # Replace old list of predators with an empty list
        BoidEcosystem.predators = []

        # Reset kill count
        BoidEcosystem.totalNbrOfKills = 0

        # Get new boids from the old ones
        BoidEcosystem._repopulateBoids()

        # Spawn fresh predators
        BoidEcosystem._spawnbrOfPredators()

    # Create and populate ecosystem with fresh boids and predators
    @staticmethod
    def createEcosystem():

        # Spawn boids
        BoidEcosystem._spawnbrOfBoids()

        # Spawn predators
        BoidEcosystem._spawnbrOfPredators()

    # Spawn first generation of boids in the ecosystem
    @staticmethod
    def _spawnbrOfBoids():

        # Get a list of random and non-overlapping position tuples
        spawnPositions = BoidEcosystem._getBoidSpawns()

        logbook.log("[START] Initializing {} new boids".format(
            BoidEcosystem.nbrOfBoids))
     
        # For each new boid:
        for n in range(BoidEcosystem.nbrOfBoids):

            # Get new boid at next spawn position:
            newBoid = BoidEcosystem._getNewBoid(spawnPositions[n])
            newBoid.ID = n


            # Breathe some life into it by setting a random velocity
            newBoid.velocity = Vec.getRandVec(BoidBehavior.maxVelocity)

            # Add to new list of boids
            BoidEcosystem.boids.append(newBoid)
            # logbook.log("[START] New Boid: {}".format(newBoid.getStats()))

            # Log the geno and phenotype data
            bStats.logGenotype(newBoid.getChromosomes())
            bStats.logPhenotype(newBoid.getPhenotypes())

    # Get a list of random spawn positions generated around the coordinate
    # defined by habitatCenter
    @staticmethod
    def _getBoidSpawns():

        positions = []
        habitatCenter = (BoidEcosystem.habitatWidth / 2,
                         BoidEcosystem.habitatHeight / 2)

        # Radius around the spawn point
        # (doesn't really work as a radius at this point,
        # more like a spawn square)
        spawnRadius = 150.0

        while len(positions) < BoidEcosystem.nbrOfBoids:

            rand_x = random.uniform(
                habitatCenter[0] - spawnRadius, habitatCenter[0] + spawnRadius)
            rand_y = random.uniform(
                habitatCenter[1] - spawnRadius, habitatCenter[1] + spawnRadius)

            if (rand_x, rand_y) not in positions:
                positions.append(Vec(rand_x, rand_y))

        return positions

    # S I M U L A T I O N  F U N C T I O N S

    # Check if any boids have been hunted down by a predator. Only one boid
    # can be killed at a time by one predator. Boids that come too close to a
    # a predator will survive the encounter, if the predator is not "hungry".

    @staticmethod
    def _checkForKills(localBoids, predators):

        # logbook.log("[HUNT] Start predation check")

        for predator in predators:

            # if predator isn't hungry, advance to the next predator
            if predator.currHunger <= PredatorBehavior.maxKillTimeout:
                continue

            # Brainwave: make the predator store the closest boid in a
            # self.target variable that can be called by this function.
            # This could remove the need to iterate over all boids below:
            for boid in localBoids:
                distance = predator.position.distanceTo(boid.position)
                # if distance to boid within killRadius:
                if distance < PredatorBehavior.killRadius:
                    # Try to remove the boid from the list
                    try:
                        localBoids.remove(boid)
                        BoidEcosystem.totalNbrOfKills += 1
                        predator.currHunger = 0
                    except ValueError as e:
                        # If it fails, print an error message and continue
                        # the simulation
                        logbook.log('[SIM][ERROR] Could not remove hunted boid from boids: {}'.format(e))
                    # Continue exits the boid in boids loop
                    continue

        # logbook.log("[HUNT] End predation check")

    # Check for collissions between boids. Boids can collide an N amount of
    # times before they are removed from the simulation. The idea being that
    # if they get into this situation repeatedly, they're bound to crash to
    # death or suffer a similar bad fate. Boids that have not reached their
    # max collission limit will be slowed down by a factor of x for an amount
    # of time, both of which can be edited from the settings in run.py
    @staticmethod
    def _checkForCollissions(localBoids):

        for boid in localBoids:

            # If boid is already dazed from a previous collission skip it.
            # This is to give it time to fly away. If boids in a simulation
            # appear to stop in the habitat and not really move on, then
            # this is likely the culprit.
            if boid.dazedTimer > 0:
                continue

            for otherBoid in localBoids:

                # if boid and otherBoid are the same boid, well, advance the
                # iteration
                if boid is otherBoid:
                    continue

                distance = boid.position.subVec(otherBoid.position).getMag()

                if distance < BoidEcosystem.collisionRadius:

                    # Uncomment to get annoying collision info in real time:
                    # logbook.log("[COLLISSION] {} and {}".format(boid.getStats(), otherBoid.getStats()))

                    # Start the confusion timer.
                    boid.dazedTimer = BoidBehavior.maxSlowdownTime

                    # Likewise for the other boid involved in the colission
                    if otherBoid.dazedTimer > 0:
                        otherBoid.dazedTimer = BoidBehavior.maxSlowdownTime
                        otherBoid.collisions += 1

                    # Increase both boids collission counts and...
                    boid.collisions += 1

                    # ... and if they exceed the max allowed collissions:
                    # remove one or both boids from the simulation:
                    if BoidEcosystem.deadlyCollisions is True:
                        if boid.collisions > BoidEcosystem.maxNbrOfCollisions:
                            
                            try:
                                # logbook.log(
                                BoidEcosystem.boids.remove(boid)
                                BoidEcosystem.totalNbrOfKills += 1
                            except ValueError as e:
                                logbook.log("[ERROR] Could not remove boid from boids: {}".format(e))

                        if otherBoid.collisions > BoidEcosystem.maxNbrOfCollisions:
                            try:
                                BoidEcosystem.boids.remove(otherBoid)
                                BoidEcosystem.totalNbrOfKills += 1
                            except ValueError as e:
                                logbook.log(
                                    "[ERROR] Could not remove other boid from boids: {}".format(e)
                                )

        # logbook.log("[COLISSION] End collission check")

    # B O I D   R E P R O D U C T I O N

    # Main function for initiating the creation of a new generation from the
    # gene pool of the previous generation. The class BoidGenetics is utilized
    # in subfunctions to simulate random segregation (if it has been enabled in
    # run.py), one-point crossover and mutation. All the probabilities and
    # parameters governing the genetic details of the reproduction can be
    # tinkered with in run.py
    @staticmethod
    def _repopulateBoids():

        youngBoids = []

        logbook.log("[NEXT] Repopulating habitat with {} new boids".format(
            BoidEcosystem.nbrOfBoids))

        # I use a set of pregenerated random positions for the new boids.
        # This makes it easier to generate a set of positions without any
        # duplicates, meaning none of them will start off sharing a coordinate
        # and colliding right off the bat
        randomPositions = BoidEcosystem._getBoidSpawns()

        for n in range(0, BoidEcosystem.nbrOfBoids):

            # logbook.log("[NEW] Boidlet {}:".format(n + 1), 1)

            # Parent 1 is selected randomly from the boid population
            # and removed to prevent it being selected twice
            male = random.choice(BoidEcosystem.boids)
            BoidEcosystem.boids.remove(male)

            # Parent 2.
            female = random.choice(BoidEcosystem.boids)
            BoidEcosystem.boids.remove(female)

            # logbook.log("[NEW] Parent 1: {}".format(male.getStats()), 2)
            # logbook.log("[NEW] Parent 2: {}".format(female.getStats()), 2)

            # A boidlet, given a position and a random velocity vector and
            # added to the list of new boids.
            offspring = BoidEcosystem._breedNewBoid(
                male, female, randomPositions[n])

            offspring.ID = n
            offspring.velocity = Vec.getRandVec(BoidBehavior.maxVelocity)

            youngBoids.append(offspring)

            # Parents are reinserted into ecosystem for next round of random
            # selection
            BoidEcosystem.boids.append(male)
            BoidEcosystem.boids.append(female)

        # Print some nice mean values of the new boids to the terminal
        logbook.logMeans(youngBoids, 1)
        # List of new boids replaces the old boids
        BoidEcosystem.boids = youngBoids
        # for boid in BoidEcosystem.boids:
        #    logbook.log("[NEXTGEN] {}".format(boid.getStats()))

    # Insert parents and a good spot and get a boidlet.
    @staticmethod
    def _breedNewBoid(m, f, pos):

        # Placeholders for parental gametes
        maleGamete = None
        femGamete = None

        # logbook.log("[NEW] Parental genomes", 1)
        # logbook.log("[NEW] Parent 1: {}".format(m.getPrettyGenome()), 1)
        # logbook.log("[NEW] Parent 2: {}".format(f.getPrettyGenome()), 1)

        # If independent segregation is enables in the settings, the genetic
        # algorithm will assume that there is no linkage occuring between the
        # passed down genes. Otherwise the whole boid genome will be treated
        # as one physical chromosome.

        if BoidGenetics.independentSegregation is True:

            # The genes are segregated and grouped as a "gamete" (the name
            # being a lefotver from the previously default linked chromosome)
            maleGamete = BoidGenetics.segregateAlleles(m.getChromosomes())
            femGamete = BoidGenetics.segregateAlleles(f.getChromosomes())
        else:
            # If the random segregation is disabled, two parental
            # chromosomes are randomly chosen, and no segregation occurs.
            maleGamete = random.choice(m.getChromosomes())
            femGamete = random.choice(f.getChromosomes())

        # Crossover occurs in the newly made boid.
        # BoidGenetics.getCrossover(
        #    maleGamete, femGamete, BoidEcosystem.nbrOfLoci)

        # Mutations likewise
        maleGamete = BoidGenetics.getMutation(maleGamete)
        femGamete = BoidGenetics.getMutation(femGamete)

        # And voila:
        boidlet = Boid(pos, maleGamete, femGamete)

        # logbook.log("[NEW] Final boidlet parameters:", 1)
        # logbook.log("[NEW] Position: {}".format(pos.getXY()), 2)
        # logbook.log("[NEW] Genome: {}".format(boidlet.getPrettyGenome()), 2)
        # logbook.log("[NEW] Stats: {}\n".format(boidlet.getStats()), 2)
        if BoidEcosystem.currentGeneration % BoidEcosystem.printPerNthGen == 0:
            bStats.logGenotype(boidlet.getChromosomes())
            bStats.logPhenotype(boidlet.getPhenotypes())

        return boidlet

    # Generating fresh predators
    @staticmethod
    def _spawnbrOfPredators():

        for predator in range(0, BoidEcosystem.nbrOfPredators):

            randPos = BoidEcosystem._getRandPos()
            newPred = PredatorBoid(randPos)
            newPred.velocity = Vec.getRandVec(PredatorBehavior.maxVelocity)
            BoidEcosystem.predators.append(newPred)

    # Function for generating a boid with a random genome at
    # a given position
    @staticmethod
    def _getNewBoid(pos):

        chromosome_a = BoidEcosystem._getRandChromosome()
        chromosome_b = BoidEcosystem._getRandChromosome()

        return Boid(pos, chromosome_a, chromosome_b)

    # Random chromosome generator
    @staticmethod
    def _getRandChromosome():

        geneSet = {}

        for gene in BoidGenetics.geneList:
            allele = BoidGenetics.getRandAllele(
                BoidEcosystem.maxInitialGeneVal
            )
            geneSet[gene] = allele

        newChromosome = Chromosome(geneSet)
        return newChromosome

    # Get random position in habitat
    @staticmethod
    def _getRandPos():

        randPos = Vec(random.randrange(0, BoidEcosystem.habitatWidth),
                      random.randrange(0, BoidEcosystem.habitatHeight))
        return randPos
