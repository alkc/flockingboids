#!/usr/bin/python

from vector import Vector2D as Vec

from graphics import BoidGraphics
from printers import BoidMetrics as bStats

'''
BoidBehavior defines the... well, behavior patterns of boids.
It also stores a variety of parameters that govern this behavior.
'''

class BoidBehavior:

    fov = None
    maxVelocity = None
    minVelocity = None
    minDist = None
    perceptionRadius = None
    display = None
    localBoids = None
    localPredators = None

    maxWidth = None
    maxHeight = None
    maxSlowdownTime = None
    slowdownFactor = None
    headless = False

    maxForce = 0.5

    color = (255, 255, 255)  # temporary

    printOrderPerNthTick = None # temporary

    # Boid movement has been unified into one method
    # The advantage is that only one iteration is required
    # over all the other boids in the habitat per boid.
    # The disadvantage is that it becomes harder to read.
    # So, comments to the rescue:
    @staticmethod
    def moveBoids(localBoids, localPredators):

        BoidBehavior.localPredators = localPredators
        BoidBehavior.localBoids = localBoids

        orientationVectors = []
        printOrder = bStats.printThisGen() and bStats.ticker % BoidBehavior.printOrderPerNthTick == 0

        center = Vec(
            BoidBehavior.maxWidth/2,
            BoidBehavior.maxHeight/2
        )

        for boid in BoidBehavior.localBoids:


            # Initialize empty vectors for each rule
            cohV = Vec()  # Cohesion vector
            sepV = Vec()  # Separation vector
            aliV = Vec()  # Alignment
            evaV = Vec()  # Evasion
            
            cenV = center.subVec(boid.position)  # Fly towards center
            
            randAVec = Vec().getRandVec(BoidBehavior.maxForce)
            randBVec = Vec().getRandVec(BoidBehavior.maxForce)
            randCVec = Vec().getRandVec(BoidBehavior.maxForce)

            cohCounter = 0
            sepCounter = 0

            for otherBoid in BoidBehavior.localBoids:

                if boid is otherBoid:
                    #if boid is otherBoid, skip to the next boid
                    continue

                # Get distance to other boid
                distance = boid.position.subVec(otherBoid.position)
                distance = distance.getMag()

                # Check if otherBoid within perception range
                if distance > 0 and distance < BoidBehavior.perceptionRadius:

                    # If yes, add the position of the boid to the
                    # cohesion vector 
                    cohV = cohV.addVec(otherBoid.position)
                    cohCounter += 1

                    # Check if the otherBoid is too close:
                    if distance < BoidBehavior.minDist:

                        # Create difference vector for pointing the boid away
                        # from the otherBoid 
                        difference = boid.position.subVec(otherBoid.position)
                        difference = difference.normalized()

                        # Weigh the difference vector by distance to otherBoid
                        difference = difference.divScalar(distance)

                        sepCounter += 1
                        sepV = sepV.addVec(difference)

                    # Add the velocity of the other boid to the alignment
                    # vector
                    aliV = aliV.addVec(otherBoid.velocity)

            # If cohesionVector has positions added:
            if cohCounter > 0:
                # Get the mean of the cohesion vector 
                cohV = cohV.divScalar(cohCounter)

                # Implement steering:
                # Create steer by subtracting the boid velocity
                # from a vector pointing to the desired location
                
                cohV = cohV.subVec(boid.position)
                cohV = cohV.setMag(BoidBehavior.maxVelocity)
                cohV = cohV.subVec(boid.velocity)

                # Limit the acceleration to max allowed
                cohV = cohV.limit(BoidBehavior.maxForce)

            # If separation vector has a length:
            if sepV.getMag() > 0:
                # Apply Reynold's steering:
                sepV = sepV.setMag(BoidBehavior.maxVelocity)
                sepV = sepV.subVec(boid.velocity)
                sepV = sepV.limit(BoidBehavior.maxForce)

            # Ditto for alignment vector:
            if aliV.getMag() > 0:
                aliV = aliV.normalized()
                aliV = aliV.subVec(boid.velocity)
                aliV = aliV.limit(BoidBehavior.maxForce)

            # Check if any predator is close by:
            for predator in BoidBehavior.localPredators:

                distance = boid.position.subVec(predator.position).getMag()

                # If predator is within view:
                if distance < BoidBehavior.perceptionRadius:

                    # Create vector pointing the hell away from
                    # the predator.
                    difference = predator.position.subVec(boid.position)
                    difference = difference.normalized()
                    # Weigh it by distance:
                    difference = difference.divScalar(distance)
                    evaV = evaV.addVec(difference)

            # if evasion vector has a length:
            if evaV.getMag() > 0:

                # Point the vector away from the predator
                evaV = evaV.multScalar(-1)
                # Steering
                evaV = evaV.setMag(BoidBehavior.maxVelocity)
                evaV = evaV.subVec(boid.velocity)
                evaV = evaV.limit(BoidBehavior.maxForce)

            distanceToCenter = cenV.getMag()

            if distanceToCenter > 0:
                cenV = cenV.setMag(BoidBehavior.maxVelocity)
                cenV = cenV.subVec(boid.velocity)
                cenV = cenV.limit(BoidBehavior.maxForce)

            # Apply the weights

            cohW = boid.getPhenotype('cohW') - boid.getPhenotype('antiCoh')
            sepW = boid.getPhenotype('sepW') - boid.getPhenotype('antiSep')
            aliW = boid.getPhenotype('aliW') - boid.getPhenotype('antiAli')
            evaW = boid.getPhenotype('evaW') - boid.getPhenotype('antiEva')
            cenW = (
                boid.getPhenotype('center') -
                boid.getPhenotype('antiCenter')
            ) * (distanceToCenter/100)  # Pull reduced by distance to center

            cohW = cohW if 0 <= cohW else 0.0
            sepW = sepW if 0 <= sepW else 0.0
            aliW = aliW if 0 <= aliW else 0.0
            evaW = evaW if 0 <= evaW else 0.0
            cenW = cenW if 0 <= cenW else 0.0
			
            cohV = cohV.multScalar(cohW)
            sepV = sepV.multScalar(sepW)
            aliV = aliV.multScalar(aliW)
            evaV = evaV.multScalar(evaW)
            cenV = cenV.multScalar(cenW)
            randAVec = randAVec.multScalar(boid.getPhenotype('randA'))
            randBVec = randBVec.multScalar(boid.getPhenotype('randB'))
            randCVec = randCVec.multScalar(boid.getPhenotype('randC'))

            # Uncomment this block and tinker with the
            # settings for fixed non-genetic weights
            '''
            cohV = cohV.multScalar(1.50)
            sepV = sepV.multScalar(20.0)
            aliV = aliV.multScalar(5.0)
            evaV = evaV.multScalar(10.0)
            '''

            boid.deltaVel = boid.velocity.addVec(cohV)
            boid.deltaVel = boid.deltaVel.addVec(sepV)
            boid.deltaVel = boid.deltaVel.addVec(aliV)
            boid.deltaVel = boid.deltaVel.addVec(evaV)
            boid.deltaVel = boid.deltaVel.addVec(randAVec)
            boid.deltaVel = boid.deltaVel.addVec(randBVec)
            boid.deltaVel = boid.deltaVel.addVec(randCVec)
            boid.deltaVel = boid.deltaVel.addVec(cenV)

            if printOrder:
                orientationVectors.append(boid.velocity.normalized())

            # Limit velocity to max-velocity if needed.
            BoidBehavior.limitVelocity(boid, BoidBehavior.maxVelocity)

            # Limit the velocity further, if boid is dazed from a collision:
            if boid.dazedTimer > 0:

                BoidBehavior.limitVelocity(boid, BoidBehavior.minVelocity)
                boid.dazedTimer -= 1

            # And finally, move boid
            boid.velocity = boid.deltaVel
            boid.position = boid.position.addVec(boid.velocity)

            # Finally, finally: check if boid is not out of bounds
            # and tell pygame to render it
            BoidBehavior._checkBoundaries(boid)
            BoidGraphics.drawBoid(boid)

        if printOrder:
            bStats.logOrder(orientationVectors)

    @staticmethod
    def _checkBoundaries(boid):

        if boid.position.x < 0:
            boid.position.x += BoidBehavior.maxWidth

        elif boid.position.x > BoidBehavior.maxWidth:
            boid.position.x -= BoidBehavior.maxWidth

        if boid.position.y < 0:
            boid.position.y += BoidBehavior.maxHeight

        elif boid.position.y > BoidBehavior.maxHeight:
            boid.position.y -= BoidBehavior.maxHeight

    @staticmethod
    def limitVelocity(boid, maxVelocity):

        boidSpeed = boid.deltaVel.getMag()

        if boidSpeed > maxVelocity:

            newVel = boid.deltaVel.setMag(maxVelocity)
            boid.deltaVel = newVel


class PredatorBehavior:

    maxKillTimeout = None
    predators = None
    prey = None
    maxVelocity = None
    minVelocity = None
    minDistance = None
    maxForce = 0.3
    killRadius = None
    perceptionRadius = None
    maxSlowdownTime = None

    color = (255, 0, 0)

    @staticmethod
    def movePredators(predators, boids):

        for predator in predators:

            preyV = PredatorBehavior.targetPrey(predator, boids)
            predator.deltaVel = predator.velocity.addVec(preyV)
            sepV = PredatorBehavior.separatePredator(predator, predators)
            predator.deltaVel = predator.deltaVel.addVec(sepV)
            PredatorBehavior.limitVelocity(
                predator, PredatorBehavior.maxVelocity)

            if predator.currHunger <= PredatorBehavior.maxKillTimeout:
                predator.currHunger += 1
                predator.deltaVel = predator.deltaVel.limit(
                    PredatorBehavior.minVelocity)

            predator.velocity = predator.deltaVel
            predator.position = predator.position.addVec(predator.velocity)
            BoidBehavior._checkBoundaries(predator)
            BoidGraphics.drawBoid(predator)

    @staticmethod
    def targetPrey(predator, boids):

        if predator.currHunger <= PredatorBehavior.maxKillTimeout:

            return Vec()

        closestBoid = None
        closestBoidDistance = None

        preyVec = Vec()

        for boid in boids:

            distance = predator.position.distanceTo(boid.position)

            if distance < closestBoidDistance or closestBoidDistance is None:

                closestBoidDistance = distance
                closestBoid = boid

        if closestBoid is not None:

            preyVec = closestBoid.position.subVec(
                predator.position)
            preyVec = preyVec.setMag(PredatorBehavior.maxVelocity)
            preyVec = preyVec.subVec(predator.velocity)
            preyVec = preyVec.limit(PredatorBehavior.maxForce)

        return preyVec

    # Separate predator from other predators
    @staticmethod
    def separatePredator(predator, predators):

        sepV = Vec()

        for otherPredator in predators:

            if predator is otherPredator:
                continue

            difference = predator.position.subVec(otherPredator.position)
            distance = difference.getMag()

            if distance < PredatorBehavior.minDistance:

                difference = difference.normalized()
                difference = difference.divScalar(distance)

                sepV = sepV.addVec(difference)

        if sepV.getMag() > 0:

            sepV = sepV.setMag(PredatorBehavior.maxVelocity)
            sepV = sepV.subVec(predator.velocity)
            sepV = sepV.limit(PredatorBehavior.maxForce)

        return sepV

    @staticmethod
    def limitVelocity(predator, maxVelocity):

        boidSpeed = predator.deltaVel.getMag()

        if boidSpeed > maxVelocity:

            newVel = predator.deltaVel.setMag(maxVelocity)
            predator.deltaVel = newVel
