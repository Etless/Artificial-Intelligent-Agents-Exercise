import random

# The min and max population dictates at what values the population x
# values can start and end at. f is the function used. Generation is the
# number of generation iterations to be performed. Size is the size of
# the population to be tested.
def iterate(population_size, generations, min_population, max_population, f, mutation_prob, crossover_prob):

    # Create starting population
    population = [random.uniform(min_population, max_population) for _ in range(population_size)]

    # Used to keep track of the best fitness for
    # each generation
    best_history = []

    for gen in range(generations):

        # Evaluate all elements in population list
        evaluated = [(x, f(x)) for x in population]

        # Sort the list by its fitness f(x)
        evaluated.sort(key=lambda x: x[1], reverse=True)

        best_history.append(evaluated[0][1]) # Save best y-value

        # Get the top 50%
        parents = evaluated[:population_size // 2]

        # Temp population (new population)
        _population = []

        while len(_population) < population_size:
            p1, p2 = random.sample(parents, 2)

            # Crossover (a)
            child_x = crossover_prob * (p1[0] + p2[0])

            # Mutation (p)
            if random.random() < mutation_prob:
                child_x += random.uniform(-0.1, 0.1) # Random variation (mutation)

            _population.append(child_x)

        # Update new population
        population = _population

    return best_history, population



