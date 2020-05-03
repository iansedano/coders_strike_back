# GENETIC ALGORITHMS

import random
import sys
from answer import is_answer, get_mean_score # this is the string that the program is searching to match.

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !'."

def get_letter():
    return random.choice(alphabet)

def create_chromosome(size):
    chromosome = ''
    for i in range(size):
        chromosome += get_letter()
    
    return chromosome

# SCORING - comparing to answer
def get_score(chrom):
    key = get_answer()
    #  * compare the chromosome with the solution (how many character are in the correct position?)
    score = 0
    counter = 0
    for i in key:
        if key[counter] == chrom[counter]:
            score += 1
        counter += 1
    return (score/20)


def make_score_list(population):

    score_list = list(map(lambda c: [get_score(c), c], population)) # makes list of lists showing score and corresponding chromosome
    score_list.sort(reverse=True, key=lambda s: s[0])

    return score_list

# Selecting the chromosomes to pass on to next gen.
def selection(population):
    GRADED_RETAIN_PERCENT = 0.3     # percentage of retained best fitting individuals
    NONGRADED_RETAIN_PERCENT = 0.2  # percentage of retained remaining individuals (randomly selected)

    #  * Sorts individuals by their fitting score
    #  * Selects the best individuals
    #  * Randomly selects other individuals
    
    selection = []
    
    scores = make_score_list(population)
    
    graded_int_to_retain = int(len(scores) * 0.3)
    while graded_int_to_retain > 0:
        selected = scores.pop(0)
        selection.append(selected)
        graded_int_to_retain -= 1
    
    nongraded_int_to_retain = int(len(scores) * 0.2)
    while nongraded_int_to_retain > 0:
        rand_int = random.randint(0, len(scores)-1)
        selection.append(scores.pop(rand_int))
        nongraded_int_to_retain -= 1
    
    selected_c = list(map(lambda chromosome: chromosome[1], selection)) # gets the chromosome not the score
    
    return selected_c


# Chromosone Crossover
def crossover(parent1, parent2):
    #  * Selects half of the parent genetic material
    #  * child = half_parent1 + half_parent2
    #  * Returns the new chromosome
    #  * Genes are not be moved
    
    # maybe not necessary to separate, but if genes are different lengths then it would be.
    half_len_p1 = int(len(parent1) / 2)
    half_len_p2 = int(len(parent2) / 2)
    
    half_p1 = parent1[:half_len_p1]
    half_p2 = parent2[half_len_p2:]
    
    child = half_p1 + half_p2
    
    return child


# Mutation
    
def mutation(chromosome):
    #  * Random gene mutation : a character is replaced
    
    chromosome_len = len(chromosome)
    index = random.randint(0, chromosome_len - 1)
    chromosome = chromosome[:index] + get_letter() + chromosome[index + 1:]
    
    return chromosome


def create_population(pop_size, chrom_size):
    # creates the base population
    
    population = []
    for i in range(pop_size):
        chrom = create_chromosome(chrom_size)
        population.append(chrom)

    return population
    
def generation(population):
    
    select = selection(population)
    
    # reproduction
    # As long as we need individuals in the new population, fill it with children
    children_to_create = population_size - len(population)

    while len(children) < children_to_create:
        ## crossover
        parent1 = population[random.randint(0,len(population)-1)] # randomly selected
        print(f"parent1 {parent1}")
        parent2 = population[random.randint(0,len(population)-1)] # randomly selected
        print(f"parent2 {parent2}")
        # use the crossover(parent1, parent2) function created on exercise 2
        child = crossover(parent1, parent2)
        
        ## mutation
        child = mutation(child)
        population.append(child)
    
    return population

def algorithm():
    chrom_size = int(input())
    population_size = 30
    
    # create the base population
    population = create_population(population_size, chrom_size)
    
    answers = []
    
    # while a solution has not been found :
    while not answers:
        ## create the next generation
        population = generation(population)
        
        score_list = make_score_list(population)
        
        mean = sum([s[0] for s in score_list])/len(score_list)
        print(mean, file=sys.stderr)
    
        ## check if a solution has been found
        for chrom in population:
            if is_answer(chrom):
                answers.append(chrom)
    
    print(answers[0])
