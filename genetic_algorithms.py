# SCORING OF CHROMOSOMES

from answer import get_answer

def get_score(chrom):
    key = get_answer()
    # TODO: implement the scoring function
    #  * compare the chromosome with the solution (how many character are in the correct position?)
    score = 0
    counter = 0
    for i in key:
        if key[counter] == chrom[counter]:
            score += 1
        counter += 1
    return (score/20)


# CHROMOSOME SELECTION

import random
from answer import get_score
    
def score(chrom):
    # floating number between 0 and 1. The better the chromosome, the closer to 1
    # We coded the get_score(chrom) in the previous exercise
    return get_score(chrom)
    
def selection(chromosomes_list):
    GRADED_RETAIN_PERCENT = 0.3     # percentage of retained best fitting individuals
    NONGRADED_RETAIN_PERCENT = 0.2  # percentage of retained remaining individuals (randomly selected)
    # TODO: implement the selection function
    #  * Sort individuals by their fitting score
    #  * Select the best individuals
    #  * Randomly select other individuals
    
    selection = []
    
    scores = list(map(lambda c: [score(c), c], chromosomes_list))
    
    scores.sort(reverse = True, key = lambda s: s[0])
    
    g_retain = int(len(scores) * 0.3)
    
    while g_retain > 0:
        toSelect = scores.pop(0)
        selection.append(toSelect)
        g_retain -= 1
    
    
    ng_retain = int(len(scores) * 0.2)
    print(ng_retain)
    
    while ng_retain > 0:
        rand_int = random.randint(0, len(scores)-1)
        selection.append(scores.pop(rand_int))
        ng_retain -= 1
    
    selected_c = list(map(lambda list: list[1], selection))
    print(selected_c)
    
    return selected_c


# Chromosone Crossover

def crossover(parent1, parent2):
    # TODO: implement the crossover function
    #  * Select half of the parent genetic material
    #  * child = half_parent1 + half_parent2
    #  * Return the new chromosome
    #  * Genes should not be moved
    
    half_len_p1 = int(len(parent1) / 2)
    half_len_p2 = int(len(parent2) / 2)
    
    half_p1 = parent1[:half_len_p1]
    half_p2 = parent2[half_len_p2:]
    
    child = half_p1 + half_p2
    print(child)
    
    return child


# Mutation

import random
from answer import alphabet

def get_letter():
    return random.choice(alphabet)
    
def mutation(chrom):
    # TODO: implement the mutation function
    #  * Random gene mutation : a character is replaced
    
    c_len = len(chrom)
    
    index = random.randint(0,c_len-1)
    
    chrom = chrom[:index] + get_letter() + chrom[index+1:]
    
    return chrom