#!/usr/bin/python

import random
from printers import BoidGazer as logbook

'''
BoidGenetics deals with sexual reproduction,
gene segregation, mutations and crossing over

Documentation pending
'''


class BoidGenetics:

    mutationRate = None
    crossoverRate = None
    maxMutationSize = None
    independentSegregation = None
    geneList = [
        'cohW',       # Cohesion gene
        'sepW',       # Separation gene
        'aliW',       # Alignment gene
        'evaW',       # Evasion gene
        'red',        # Red color (neutral gene)
        'green',      # Green
        'blue',       # Blue
        'neutralA',   # Additional neutral genes
        'neutralB',
        'neutralC',
        'randA',      # Random walk genes
        'randB',
        'randC',
        'antiCoh',    # Solitary: non cohesion
        'antiAli',    # Solitary: non aligning
        'antiSep',    # Solitary: non separating
        'antiEva',    # Kamikaze, unimplemented
        'center',     # Fly to center
        'antiCenter'  # Mutes the center gene
    ]

    @staticmethod
    def segregateAlleles(chromosomes):
        gameteGeneSet = {}

        for gene in BoidGenetics.geneList:

            chromosome = random.choice(chromosomes)
            gameteGeneSet[gene] = chromosome.genes[gene]

        return Chromosome(gameteGeneSet)

    @staticmethod
    def getCrossover(mGamete, fGamete, nLoci):

        for gene in BoidGenetics.geneList:

            mGene = mGamete.genes[gene]
            fGene = fGamete.genes[gene]

            seqLength = len(mGene.sequence)

            nbrOfCrossovers = 0

            mNewSeq = mGene.sequence
            fNewSeq = fGene.sequence

            crossOverPositions = []

            for position in range(0, seqLength):

                chance = random.uniform(0, 1)

                if chance <= BoidGenetics.crossoverRate:

                    ab = mNewSeq[:position] + fNewSeq[position:]
                    ba = fNewSeq[:position] + mNewSeq[position:]

                    mNewSeq = ab
                    fNewSeq = ba

                    nbrOfCrossovers += 1
                    crossOverPositions.append(position)

            if nbrOfCrossovers > 0:

                logbook.log(
                    "[CROSS] {} Crossover(s) detected in {} gene at positions: {} ".format(
                        nbrOfCrossovers, gene, crossOverPositions), 2)

                logbook.log("[CROSS] Old sequences:", 2)
                logbook.log("[CROSS] {}".format(mGene.sequence), 3)
                logbook.log("[CROSS] {}".format(fGene.sequence), 3)
                logbook.log("[CROSS] New sequences:", 2)
                logbook.log("[CROSS] {}".format(mNewSeq), 3)
                logbook.log("[CROSS] {}".format(fNewSeq), 3)

            mGamete.genes[gene].sequence = mNewSeq
            fGamete.genes[gene].sequence = fNewSeq

    @staticmethod
    def getMutation(gamete):

        newGenes = {}

        for gene in BoidGenetics.geneList:

            geneValue = gamete.genes[gene].getWeightValue()
            chance = random.uniform(0, 1)

            if chance <= BoidGenetics.mutRate:

                oldVal = geneValue
                mutation = random.uniform(
                    -1 * BoidGenetics.maxMutationSize,
                    BoidGenetics.maxMutationSize)
                geneValue += mutation

                if geneValue < 0:
                    geneValue = 0.0

                logbook.log("[MUT] A mutation event occured in {} gene".format(gene), 2)
                logbook.log("[MUT] Value\t{} -> {}".format(oldVal, geneValue), 2)

            newGenes[gene] = Gene(geneValue)

        return Chromosome(newGenes)

    @staticmethod
    def getRandAllele(maxInitialGeneVal):

        randomValue = random.uniform(
            0, maxInitialGeneVal)

        return Gene(randomValue)


class Chromosome:

    def __init__(self, genes):
        self.genes = genes

    def getExpressedWeight(self, geneName):

        weightGene = self.genes[geneName]
        return weightGene.getWeightValue()

    def getExpressedColor(self, colorName):
        colorGene = self.genes[colorName]
        return colorGene.getColorValue()

    def copy(self):

        return Chromosome(self.genes)


class Gene:

    def __init__(self, value):

        # self.sequence = sequence
        # self.id_ = id_
        self.value = value

    def getWeightValue(self):
        return self.value

    def getColorValue(self):
        return self.value
