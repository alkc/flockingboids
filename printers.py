#!/usr/bin/python

from time import strftime
from vector import Vector2D as Vec


class BoidGazer:

    ticker = 0
    genePrintOrder = [
        'cohW',      # Cohesion gene
        'sepW',      # Separation gene
        'aliW',      # Alignment gene
        'evaW',      # Evasion gene
        'randA',     # Random walk genes
        'randB',
        'randC',
        'antiCoh',   # Solitary: non cohesion
        'antiAli',   # Solitary: non aligning
        'antiSep',   # Solitary: non separating
        'antiEva',   # Kamikaze
        'antiCenter',
        'center',
        'neutralA',  # Additional neutral genes
        'neutralB',
        'neutralC',
        'red',       # Red color (neutral gene)
        'green',     # Green
        'blue'       # Blue
    ]

    def __init__(self):

        # self.output = "log.txt"
        pass

    @staticmethod
    def log(line, indent=0):

        print "   " * indent + line

    @staticmethod
    def logMeans(boids, indent):

        weights = {}

        output = []

        for gene in BoidGazer.genePrintOrder:
            weights[gene] = []

        for boid in boids:
            for gene in BoidGazer.genePrintOrder:
                weights[gene].append(boid.getPhenotype(gene))

        for gene in BoidGazer.genePrintOrder:
            output.append("{}: {:.2f}".format(
                gene, sum(weights[gene]) / float(len(weights[gene]))))

        BoidGazer.log("[MEAN] Mean gene values: {}".format(", ".join(output)))


class BoidMetrics:

    phenotypeOutput = None
    generation = 0
    ticker = -1
    printPerNthGen = None

    genePrintOrder = [
        'cohW',      # Cohesion gene
        'sepW',      # Separation gene
        'aliW',      # Alignment gene
        'evaW',      # Evasion gene
        'randA',     # Random walk genes
        'randB',
        'randC',
        'center',
        'antiCoh',   # Solitary: non cohesion
        'antiAli',   # Solitary: non aligning
        'antiSep',   # Solitary: non separating
        'antiEva',   # Kamikaze
        'antiCenter',
        'neutralA',  # Additional neutral genes
        'neutralB',
        'neutralC',
        'red',       # Red color (neutral gene)
        'green',     # Green
        'blue'       # Blue
    ]

    @staticmethod
    def init(simID):

        timePrefix = strftime("%Y-%m-%d_%H.%M.%S_")

        phenotypeOutput = timePrefix + simID + "_phenotypes.txt"
        genotypeOutput = timePrefix + simID + "_genotypes.txt"
        orderOutput = timePrefix + simID + "_order.txt"
        settingsOutput = timePrefix + simID + "_metadata.txt"

        BoidMetrics.phenotypeOutput = open(phenotypeOutput, "w")
        BoidMetrics.genotypeOutput = open(genotypeOutput, "w")
        BoidMetrics.orderOutput = open(orderOutput, "w")
        BoidMetrics.settingsOutput = open(settingsOutput, "w")

        phenoHeader = "generation\t" + "\t".join(
            BoidMetrics.genePrintOrder) + "\n"
        BoidMetrics.phenotypeOutput.write(phenoHeader)

        genoHeader = "generation\t" + "\t".join(
            BoidMetrics.genePrintOrder) + "\n"
        BoidMetrics.genotypeOutput.write(genoHeader)

        orderHeader = "generation\ttick\torder\n"
        BoidMetrics.orderOutput.write(orderHeader)

    @staticmethod
    def printSettings(settings):

        for key, val in settings.iteritems():
            BoidMetrics.settingsOutput.write(
                "{}\t{}\n".format(key, val)
            )

        BoidMetrics.settingsOutput.close()

    @staticmethod
    def logPhenotype(phenotypes):

        line = str(BoidMetrics.generation)

        for phenotype in BoidMetrics.genePrintOrder:

            line += "\t" + "{:.3f}".format(phenotypes[phenotype])

        line += "\n"

        BoidMetrics.phenotypeOutput.write(line)
        BoidMetrics.phenotypeOutput.flush()

    @staticmethod
    def logGenotype(chromosomes):

        line = ""

        for chromosome in chromosomes:

            line += str(BoidMetrics.generation)

            for gene in BoidMetrics.genePrintOrder:

                line += "\t" + "{:.3f}".format(
                    chromosome.genes[gene].getWeightValue()
                )

            line += "\n"

        BoidMetrics.genotypeOutput.write(line)
        BoidMetrics.genotypeOutput.flush()

    @staticmethod
    def logOrder(orientationVectors):
        vectorSum = Vec()

        for v in orientationVectors:
            vectorSum = vectorSum.addVec(v)

        vectorSum = vectorSum.divScalar(
            float(len(orientationVectors))
        )

        order = vectorSum.getMag()

        BoidMetrics.orderOutput.write("{}\t{}\t{:.3f}\n".format(
            BoidMetrics.generation, BoidMetrics.ticker, order))

        BoidMetrics.orderOutput.flush()

    @staticmethod
    def printThisGen():

        return BoidMetrics.generation % BoidMetrics.printPerNthGen == 0

    '''
    @staticmethod
    def closeOutput():
        close(BoidMetrics.phenotypeOutput)
        close(BoidMetrics.genotypeOutput)
    '''
