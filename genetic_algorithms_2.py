import random
import sys
from answer import is_answer, get_mean_score
# You can redefine these functions with the ones you wrote previously.
# Another implementation is provided here.
from encoding import create_chromosome
from tools import selection, crossover, mutation

def create_population(pop_size, chrom_size):
    # creates the base population
    
    population = []
    for i in range(pop_size):
        chrom = create_chromosome(chrom_size)
        population.append(chrom)

    return population
    
def generation(population):
    
    selected_pop = selection(population)
    population_size = len(population)
    # reproduction
    # As long as we need individuals in the new population, fill it with children
    children_to_create = population_size - len(selected_pop)

    for i in range(children_to_create):
        ## crossover
        parent1 = selected_pop[random.randint(0,len(selected_pop)-1)] # randomly selected
        parent2 = selected_pop[random.randint(0,len(selected_pop)-1)] # randomly selected
        # use the crossover(parent1, parent2) function created on exercise 2
        child = crossover(parent1, parent2)
        
        ## mutation
        child = mutation(child)
        selected_pop.append(child)
    
    return selected_pop

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
        
        #print(get_mean_score(population), file=sys.stderr)
    
        ## check if a solution has been found
        for chrom in population:
            if is_answer(chrom):
                answers.append(chrom)
    print(answers[0], file=sys.stderr)
    print(answers[0])
    