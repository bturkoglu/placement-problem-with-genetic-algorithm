import random

def rulet_secimi(population, fitnesses, num):
	gercek_fitnesses = [1.0/f for f in fitnesses]
	total_fitness = float(sum(gercek_fitnesses))
	rel_fitness = [f/total_fitness for f in gercek_fitnesses]
	probs = [ sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]

	# Draw new population
	new_population = []
	while len(new_population) < num:
		r = random.random()
		for (i, individual) in enumerate(population):
			if r <= probs[i] and individual not in new_population:
				new_population.append(individual)
				break
	return new_population

def rulet_secimi_Ayniolabilir(population, fitnesses, num):
	gercek_fitnesses = [1.0/f for f in fitnesses]
	total_fitness = float(sum(gercek_fitnesses))
	rel_fitness = [f/total_fitness for f in gercek_fitnesses]
	probs = [ sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]

	# Draw new population
	new_population = []
	for n in range(num):
		r = random.random()
		for (i, individual) in enumerate(population):
			if r <= probs[i]:
				new_population.append(individual)
				break
	return new_population

def roulette_select(population, fitnesses, num):
    """ Roulette selection, implemented according to:
        <http://stackoverflow.com/questions/177271/roulette
        -selection-in-genetic-algorithms/177278#177278>
    """
    total_fitness = float(sum(fitnesses))
    rel_fitness = [f/total_fitness for f in fitnesses]
    # Generate probability intervals for each individual
    probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
    # Draw new population
    new_population = []
    for n in range(num):
        r = random.random()
        for (i, individual) in enumerate(population):
            if r <= probs[i]:
                new_population.append(individual)
                break
    return new_population

p =(1,2,3,4)
f = (4,7,9,5)

sonuc = rulet_secimi(p,f,2)
print(sonuc)