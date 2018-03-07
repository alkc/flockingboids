#!/usr/import/python

from math import *
import random

''' 
A simple 2D vector class.
'''

class Vector2D:

    # If the Vector class is called without specifying either x and/or y
    # it will initialize a zero vector.
    def __init__(self, x=0.0, y=0.0):

        self.x = x
        self.y = y

    def addVec(self, vector):

        x = self.x + vector.x
        y = self.y + vector.y

        return Vector2D(x, y)

    def subVec(self, vector):

        x = self.x - vector.x
        y = self.y - vector.y

        return Vector2D(x, y)

    def addScalar(self, x=0, y=0):

        x = self.x + x
        y = self.y + y

        return Vector2D(x, y)

    def multScalar(self, term):

        x = self.x * term
        y = self.y * term

        return Vector2D(x, y)

    def divScalar(self, N):

        x = self.x / N
        y = self.y / N

        return Vector2D(x, y)

    # Get the vector magnitude
    def getMag(self):

        mag = sqrt(pow(self.x, 2) + pow(self.y, 2))
        return mag

    # Set the vector magnitude to the value of mag 
    def setMag(self, mag):

        v = Vector2D(self.x, self.y)
        oldMag = v.getMag()

        # Prevent division by zero
        if oldMag > 0:

            v = v.divScalar(oldMag)
            v = v.multScalar(mag)

            return v

        return v

    def distanceTo(self, otherVec):

        dist = sqrt(pow(otherVec.x - self.x, 2) + pow(otherVec.y - self.y, 2))
        return dist

    # Compare the x and y of two vectors
    def equalsVec(self, vector):

        if self.x == vector.x and self.y == vector.y:

            return True

        return False

    # Get the normalized vector
    def normalized(self):

        v = Vector2D(self.x, self.y)
        length = v.getMag()

        return v.divScalar(length)

    # Limit the magnitude of the vector if it exceeds n^2
    # Same as PVector.limit() in processing
    def limit(self, n):

        v = Vector2D(self.x, self.y)

        if self.getMag() > (n ** 2):
            v = v.normalized()
            v = v.multScalar(n)
            return v
        return v

    # Returns the tuple with the x, y coordinates of the
    # vector
    def getXY(self, _type=None):

        if _type == 'int':

            return (int(self.x), int(self.y))

        return (self.x, self.y)
    
    # returns a random vector
    @staticmethod
    def getRandVec(max_n):

        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        

        return Vector2D(x, y).setMag(max_n)


    def transform(self, degrees):

        rads = radians(degrees)
        x = self.x * cos(rads) + self.y * sin(rads)
        y = -1 * self.x * sin(rads) + self.y * cos(rads)
        return Vector2D(x, y)

    # Test if self is clockwise to otherVec

    def isClockwiseTo(self, otherVec):

        return -1 * otherVec.x * self.y + otherVec.y * self.x > 0
