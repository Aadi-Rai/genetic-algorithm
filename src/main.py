from copy import deepcopy
from random import choices, random
from time import perf_counter

from problems.countdown import config
from problems.countdown.genome import Genome

survival_number: int = round(config.POPULATION_SIZE * config.SURVIVAL_PERCENTAGE)

population: list[Genome] = [Genome() for _ in range(config.POPULATION_SIZE)]
best_genome: Genome = population[0]

for generation in range(config.GENERATION_LIMIT + 1):
    start: float = perf_counter()
    print(f"\n****** Running generation {generation} ******")

    for genome in population:
        genome.calculate_fitness()
    fitnesses: list[float] = [x.fitness for x in population]
    average_fitness: float = sum(fitnesses) / config.POPULATION_SIZE
    max_fitness: float = max(fitnesses)

    print(f"Population's average fitness: {average_fitness:.4f}")
    print(f"Max fitness: {max_fitness:.4f}")

    population.sort(key=lambda x: x.fitness, reverse=True)

    if max_fitness > best_genome.fitness:
        best_genome = population[0]

    if config.USE_FITNESS_CRITERION:
        if config.FITNESS_CRITERION == "average":
            fitness_metric: float = average_fitness
        elif config.FITNESS_CRITERION == "min":
            fitness_metric = min(fitnesses)
        else:
            fitness_metric = max_fitness
        if fitness_metric >= config.FITNESS_THRESHOLD:
            break

    fittest_genomes: list[Genome] = population[:survival_number]
    population[config.ELITISM :] = choices(
        fittest_genomes,
        [x.fitness if x.fitness != 0 else 0.1 for x in fittest_genomes],
        k=config.POPULATION_SIZE - config.ELITISM,
    )

    population = [deepcopy(x) for x in population]
    for i in range(config.ELITISM, config.POPULATION_SIZE):
        if random() < config.MUTATION_RATE:
            population[i].mutate()

    print(f"Generation took: {perf_counter() - start:.4f}s")

print(str(best_genome))
