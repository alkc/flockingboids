#!/usr/bin/python

import csv
from datetime import datetime, timezone
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

        print("   " * indent + line)

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
    genotypeOutput = None
    orderOutput = None
    settingsOutput = None
    fateOutput = None
    generationOutput = None
    generation = 0
    ticker = -1
    printPerNthGen = None
    startedAtUTC = None
    _cohort = None
    _deaths = {}

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

        BoidMetrics.close()
        BoidMetrics.generation = 0
        BoidMetrics.ticker = -1
        BoidMetrics.startedAtUTC = datetime.now(timezone.utc).isoformat(timespec='seconds')
        BoidMetrics._cohort = None
        BoidMetrics._deaths = {}

        timePrefix = strftime("%Y-%m-%d_%H.%M.%S_")

        phenotypeOutput = timePrefix + simID + "_phenotypes.tsv"
        genotypeOutput = timePrefix + simID + "_genotypes.tsv"
        orderOutput = timePrefix + simID + "_order.tsv"
        settingsOutput = timePrefix + simID + "_metadata.tsv"
        fateOutput = timePrefix + simID + "_fates.tsv"
        generationOutput = timePrefix + simID + "_generations.tsv"

        BoidMetrics.phenotypeOutput = open(phenotypeOutput, "w", newline="")
        BoidMetrics.genotypeOutput = open(genotypeOutput, "w", newline="")
        BoidMetrics.orderOutput = open(orderOutput, "w", newline="")
        BoidMetrics.settingsOutput = open(settingsOutput, "w", newline="")
        BoidMetrics.fateOutput = open(fateOutput, "w", newline="")
        BoidMetrics.generationOutput = open(generationOutput, "w", newline="")

        phenoHeader = "generation\t" + "\t".join(
            BoidMetrics.genePrintOrder) + "\n"
        BoidMetrics.phenotypeOutput.write(phenoHeader)

        genoHeader = "generation\t" + "\t".join(
            BoidMetrics.genePrintOrder) + "\n"
        BoidMetrics.genotypeOutput.write(genoHeader)

        orderHeader = "generation\ttick\torder\n"
        BoidMetrics.orderOutput.write(orderHeader)

        csv.writer(BoidMetrics.fateOutput, delimiter="\t", lineterminator="\n").writerow(
            ["generation", "boid_id", "parent1_id", "parent2_id",
             "outcome", "death_tick", *BoidMetrics.genePrintOrder]
        )
        csv.writer(BoidMetrics.generationOutput, delimiter="\t", lineterminator="\n").writerow(
            ["generation", "status", "ticks", "births", "predation_deaths",
             "collision_deaths", "alive_at_end"]
        )

    @staticmethod
    def printSettings(settings):

        writer = csv.writer(
            BoidMetrics.settingsOutput, delimiter="\t", lineterminator="\n")
        writer.writerow(["key", "value"])
        writer.writerow(["schema_version", "2"])
        writer.writerow(["started_at_utc", BoidMetrics.startedAtUTC])
        for key, val in settings.items():
            if key not in ("description", "display"):
                writer.writerow([key, val])

        BoidMetrics.settingsOutput.close()
        BoidMetrics.settingsOutput = None

    @staticmethod
    def startGeneration(boids):
        if BoidMetrics._cohort is not None:
            raise RuntimeError("Previous generation has not been recorded")
        BoidMetrics._cohort = tuple(boids)
        BoidMetrics._deaths = {}

    @staticmethod
    def recordDeath(boid, cause, tick):
        # Standalone collision tests do not initialize the metrics writer.
        if BoidMetrics._cohort is None:
            return
        if boid not in BoidMetrics._cohort or boid in BoidMetrics._deaths:
            raise RuntimeError("Death does not belong to the active generation")
        if cause not in ("predation", "collision"):
            raise ValueError("Unknown death cause: {}".format(cause))
        BoidMetrics._deaths[boid] = (cause, tick)

    @staticmethod
    def finishGeneration(status, ticks, aliveBoids):
        if BoidMetrics._cohort is None:
            return
        if status not in ("complete", "stopped", "extinct"):
            raise ValueError("Unknown generation status: {}".format(status))

        cohort = BoidMetrics._cohort
        alive = set(aliveBoids)
        deaths = BoidMetrics._deaths
        if (not alive.issubset(cohort) or
                alive.intersection(deaths) or
                len(alive) + len(deaths) != len(cohort)):
            raise RuntimeError("Generation outcomes do not match its births")

        fateWriter = csv.writer(
            BoidMetrics.fateOutput, delimiter="\t", lineterminator="\n")
        for boid in cohort:
            outcome, deathTick = deaths.get(
                boid, ("survived" if status == "complete" else "censored", "")
            )
            fateWriter.writerow([
                BoidMetrics.generation,
                "{}:{}".format(BoidMetrics.generation, boid.ID),
                boid.parent1ID or "",
                boid.parent2ID or "",
                outcome,
                deathTick,
                *("{:.3f}".format(boid.getPhenotype(gene))
                  for gene in BoidMetrics.genePrintOrder),
            ])
        BoidMetrics.fateOutput.flush()

        csv.writer(
            BoidMetrics.generationOutput, delimiter="\t", lineterminator="\n"
        ).writerow([
            BoidMetrics.generation,
            status,
            ticks,
            len(cohort),
            sum(cause == "predation" for cause, _ in deaths.values()),
            sum(cause == "collision" for cause, _ in deaths.values()),
            len(alive),
        ])
        BoidMetrics.generationOutput.flush()
        BoidMetrics._cohort = None
        BoidMetrics._deaths = {}

    @staticmethod
    def close():
        for name in ("phenotypeOutput", "genotypeOutput", "orderOutput",
                     "settingsOutput", "fateOutput", "generationOutput"):
            output = getattr(BoidMetrics, name)
            if output is not None:
                output.close()
                setattr(BoidMetrics, name, None)

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
