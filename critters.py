#!/usr/bin/python

from vector import Vector2D as Vec


# A peaceful boid
class Boid:

    def __init__(self, pos, chr_1, chr_2):

        self.ID = None

        # Spatial vars
        # Position defines the Boid's position in the habitat
        self.position = pos

        # Same, for velocity
        self.velocity = Vec()

        # deltaVel is used for velocity change (acceleration)
        # when moving the boid
        self.deltaVel = Vec()

        # Genetic vars
        # Chromosome one and two.
        self.chromosome_1 = chr_1
        self.chromosome_2 = chr_2

        # Gene expression: the phenotypes controlled by the genes manifest
        # themselves as the mean value of the two alleles.

        self.phenotypes = {}

        for key, val in self.chromosome_1.genes.iteritems():

            self.phenotypes[key] = (
                self.chromosome_1.getExpressedWeight(key) +
                self.chromosome_2.getExpressedWeight(key)) / 2.0

        self.color = []

        for col in ['red', 'green', 'blue']:

            colval = int(self.phenotypes[col]) * 50

            # A color value outside 0-255 would break the program:
            if colval > 255:
                colval = 255
            elif colval < 0:
                colval = 0

            self.color.append(colval)

        # Nbr of collissions the boid is guilty of and
        # confusion timer
        self.collisions = 0
        self.dazedTimer = 0

    # Print phenotype
    def getStats(self):

        stats = ""

        for key, val in self.phenotypes.iteritems():
            stats += "{}: {:.2f} ".format(key, val)

        stats = stats.rstrip()

        return stats

    # Print pretty genotype (rounded down)
    def getPrettyGenome(self):
        # Currently broken.
        return "Implement pretty genome print in critters.py:Boid"

        output = ""
        output += str(["%0.2f" % i for i in self.chrom_1])
        output += "/"
        output += str(["%0.2f" % i for i in self.chrom_2])

        return output

    def getChromosomes(self):

        return [self.chromosome_1, self.chromosome_2]

    def getPhenotype(self, phenotype):

        try:
            return self.phenotypes[phenotype]
        except Exception:
            print "Phenotype for gene {} cannot be found in list of phenotypic values.".format(phenotype)
            exit()

    def getPhenotypes(self):

        return self.phenotypes

# The predator is similar to the boid, but much less complicated.


class PredatorBoid:

    def __init__(self, pos):

        # Seriously less complicated
        self.position = pos
        self.velocity = Vec()
        self.deltaVel = Vec()

        # If hunger reaches a threshold the predator will go on
        # a hunt.
        self.currHunger = 0

        PredatorBoid.color = (255, 0, 0)
