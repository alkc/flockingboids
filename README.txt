[0] TABLE OF CONTENTS

    [1] Introduction
    [2] Settings
    
        [2.1] 	SimulationID and headless mode
        [2.2] 	Habitat dimensions
        [2.3] 	Population constants
        [2.4] 	Boid parameters
        [2.5] 	Predator parameters
	[2.6] 	Kill and collision parameters
        [2.7] 	Genetic algorithm parameters
        [2.8] 	Graphics settings
        [2.9] 	Pygame settings
        [2.10] 	Printers
              
    [3] Modules and classes

        [3.1] run.py
        [3.2] ecosystem.py
        [3.3] behavior.py
        [3.4] critters.py
        [3.5] quadrants.py
        [3.6] vector.py
        [3.7] misc.py



[1] INTRODUCTION

   pyFlockingEvolution is a program implemented in python 2.7 using the game-
   development module pygame (1.3.1 <- check this) whose purpose is to 
   investigate if flocking behavior (as described by Craig Reynolds) can 
   emerge in a population of boids under the influence of one or more 
   predators.

   The program simulates an ecosystem where a population of boids try to avoid
   being hunted down by predator boids. The selection of boids occurs on the
   basis of staying alive until the end of a round, which reaches an end when
   a number of the boids have died. 

   Boids that survive are selected for random mating, through which a new 
   population of boids is spawned that replaces the previous one. 

   The reproduction involves a genetic algorithm, where in the surviving boids
   can pass down a set of genes to their offspring, and the gene can undergo
   mutations and crossover.

   The genes control how strictly boids adhere to a set of rules that control
   their motion and flocking behavior. The first three are the rules originally
   dscribed by Reynolds:
	
	1. Cohesion: 	Flying towards perceived center of flock
	2. Separation: 	Keeping a minimum distance from nearby boids
	3. Alignment:	Matching velocity to nearby boids.

   In addition, a fourth rule is introduced:

	4. Evasion:	Flying away from nearby predators.

   Aside from the weights, a set of markers which do not affect the survival rate
   of boids either way are introduced into the genome. These three markers control
   the Red, Green and Blue (RGB) values of the boid, which are visualized through
   the color the boid adopts in the graphical display.
   
   The program consists of a number of classes and helper classes, which are 
   described in part [3]



[2] SETTINGS

   Most if not all of the parameters governing the simulation can be edited from
   the main class (run.py) to adjust the simulation to your liking. What follows
   is an indepth description of each setting.


   [2.1] SimulationID and headless mode

	simulationID:
		Simulation ID is used to set the title of the current simulation
		session. In the future it will reflect itself in the filenames
		of the data output, for easier distinction of runs.
	   
	headless:
		If headless mode is set to True before starting the simulation,
		the simulation will start without initializing pygame and the 
		rest of the graphical components. If the simulation is 
		initialized with graphics on, headless mode can be toggled on
		and off by pressing the key H when the pygame window is in focus.
    

    [2.2] Habitat dimensions

	Habitatwidth and heigh define the dimensions of the habitat in pixels and
	also the size of the pygame display, if headless mode is off.


    [2.3] Population size

    	nbrOfBoids:
		The amount of boids to be generated at the start of each generation.
	nbrOfPredators: 
		The amount of predators to be simulated.
    

    [2.4] Boid (prey) parameters

	maxBoidVelocity:
		The maximum velocity a boid is permitted to reach. Any higher
		velocities are capped at this limit.

	minBoidVelocity:
		The minimum velocity a boid is allowed to keep. This setting 
		also doubles as the velocity to which a boid is reduced if
		it collides with another boid.

    	minNeighborDist:
		The minimum distance a boid should keep to other nearby boids.
		The presence of another boid within this radius should trigger
		the separation rule.

	maxBoidForce:
		The max amount of acceleration a boid is permitted to display.

    	perceptionRadius:
		Defines the radius within which a boid can detect other boids 
		or predators.


    [2.5] Predator parameters

    	minPredatorNeighborDistance:
		Defines the minimum distance a predator should keep to other
		predators. [Has not yet been tested to work]		
	
    	maxPredatorVelocity:
		Self-explanatory
	
	minPredatorVelocity:
		The velocity to which a predator is reduced after a successful 
		hunt.

    	restAfterKill
		When set to true, predators that have recently eaten a boid 
		will 'rest' for a specifed amount of time. Meaning they will
		be reduced to their minimum allowed velocity, until they start
		hunting again.

    	maxPredatorForce:
		Max predator acceleration.

	killRadius:
		If a boid enters a hunting predators kill radius, it will be 
		eaten. The cruelty of Artifical Nature remains the same, even
		without pixel perfection.

    	huntingInterval:
		The time (measured in program ticks) for which a predator rests
		after a successful kill.


    [2.6] Kill and collision parameters
	
	deadlyCollisions:
		Enables death penalty for boids for colliding too many times 
		with other boids.

    	slowDownTimer:
		The time in program ticks for which a boid is slowed down 
		after a collision

	maxNbrOfCollisions:
		Max amount of collisions before the boid is removed for its
		 poor flying.

	collisionRadius:
		Radius from the center of a boid within which the presence
		of another boid counts as a collision.

    	nbrOfKillsBeforeReset:
		The kill count cutoff at which the simulation is advanced to 
		the next generation of boids.


    [2.7] Evolutionary algorithm parameters
	
	mutationRate:
		Mutation rate defines the chance per base/position at which
		a mutation can occur.
	
	mutationSize
		No longer implemented.

    	crossoverRate
		Rate at which one-point crossover can occur per base.
	
	maxInitialGeneValues
		Defines the upper limit of the range in which the random genes
		of the first generation are generated. A value of zero leads to
		the initial boids being spawned as "blank slates", i.e. no 
		initial flocking behavior or colors.

    	independentSegregation
		If set to True, the program will assume there is no linkage at 
		all between the boid genes, and they will be independently 
		segregated when forming the "gametes"		


    [2.8] Graphics settings

	drawVelocityVector
		Enable the rendering of each boid and predator velocity vector.
		Can be toggled during the simulation by pressing the 'V' key.

	drawBoidMinimumDistance, drawBoidPerceptionRadius, 
	drawPredatorMinimumDistance:
		Enable the rendering of each boid and predator neighbor or 
		perception radius. Can be toggled during the simulation by 
		pressing the 'V' key.


    [2.9] pygame settings

	bgColor:
		The background color of the pygame display.

	windowTitle:
		Specifies the title in the menubar of the pygame display.

    [2.10] Printer settings
	   
	[Work in progress!]



[3] MODULES AND CLASSES

   Description of the various modules and associated classes


[3.1] run.py

   run.py is the main program that sets the settings and runs the simulation.
   Currently all settings are set from within run.py.


[3.2] ecosystem.py

   ecosystem.py contains the class BoidEcosystem. BoidEcosystem is the most
   important class that stores all parameters that define the boid/predator
   ecosystem and handles all events occurring during the simulation.


[3.3] genetics.py

   BoidGenetics is a class that handles the events relevant to the
   sexual reproduction of the boids. In addition, there is a Chromosome
   and Gene class, that define the boid chromosome and alleles/genes
   respectively. Both come with useful functions that make life easier.

   [DESCRIBE MUTATION AND RECOMBINATION HERE]


[3.4] behavior.py

   behavior.py (formerly flock.py) stores two classes: BoidBehavior and 
   PredatorBehavior that describe and apply the rules that control the movement
   of boids and predators respectively.


[3.5] critters.py

   critters (formerly boids.py) store the Boid and Predator classes that define
   the skeletons of boids and predators.


[3.6] printers.py

   [WORK IN PROGRESS]


[3.6] vector.py

   Helper class that defines a two-dimensional vector. The class also posseses
   class methods that allow for easy arethmitic operations on vectors, together
   with methods borrowed from the Processing PVector class, such as limit() or
   setMagnitude().


[3.7] settings.py

	[WORK IN PROGRESS:
		- class BoidSettings
		- Reading in settings from file?
	]
