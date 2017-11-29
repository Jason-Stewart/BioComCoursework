from random import random, choice, uniform, randrange
from operator import add, sub
from copy import copy, deepcopy
import sys

POPULATION_SIZE = 100
RULES = 10
MUTATION_RATE = 0.130

class dataSet(object):
    def __init__(self):
        self.condition = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.out = None

    def printOut(self):
        return_string = "["
        for rules in self.condition[:]:
            return_string += str(rules) + ", "
        return_string += "] " + str(self.out)
        return return_string

class Individual(object):
    def __init__(self):
        self.ruleSet = [RuleSet() for _ in range(10)]
        self.fitness = 0

    def printOut(self):
        print "\n Individual: \n"
        for p in self.ruleSet[:]:
            print "     " + p.printOut()
        print "     Fitness: " + str(self.fitness)

    def toArray(self):
        returnArray = []
        for ruleset in self.ruleSet[:]:
            for rule in ruleset.rules[:]:
                returnArray.append(rule.left)
                returnArray.append(rule.right)
            returnArray.append(ruleset.out)
        return returnArray

    def fromArray(self, stringArray):
        count = 0
        for ruleset in self.ruleSet[:]:
            for rule in ruleset.rules[:]:
                rule.left = stringArray[count]
                count += 1
                rule.right = stringArray[count]
                count += 1
            ruleset.out = stringArray[count]
            count += 1

        

class RuleSet(object):
    def __init__(self):
        self.rules = [Rules() for _ in range(6)]
        self.out = None

    def printOut(self):
        return_string = "["
        for rules in self.rules[:]:
            return_string += str(rules.low()) + " - " + str(rules.high()) + ", "
        return_string = return_string[:-2] + "] " + str(self.out)
        return return_string
                

class Rules(object):
    def __init__(self):
        self.left = 0.0
        self.right = 0.0

    def randomGen(self):
        self.left = randomNumber()
        self.right = randomNumber()

    def low(self):
        return float(self.left) if float(self.left) < float(self.right) else float(self.right)
        
    def high(self):
        return float(self.left) if float(self.left) > float(self.right) else float(self.right)

RULESET = [Individual() for _ in range(POPULATION_SIZE)]
TRAINING_DATA = [dataSet() for _ in range(1000)]
TEST_DATA = [dataSet() for _ in range(1000)]
BESTINDIVIDUAL = Individual()

# Function: randomNumber
# Return a random number between 0 and 1 with 6 decimal point

def randomNumber():
    return ("%.6f" % uniform(0, 1))

def randomNumberMutation():
    return ("%.6f" % uniform(0, 0.1))

# Function: getFile
# 

def getFile():
    lines = []
    file_open = open("./data3.txt", "r").read().splitlines()
    for line in file_open:
        lines.append(line)
    lines.pop(0)
    
    return lines

# Function: createPopulation
#

def createPopulation():
    for rule_object in RULESET[:]:
        for ruleset in rule_object.ruleSet[:]:
            for rule in ruleset.rules[:]:
                rule.randomGen()
            ruleset.out = randrange(2)
        Evaluate(rule_object)

# Function: tournamentSelection
# 

def tournamentSelect(binary):
    return_children = [None, None]

    for children in range(len(return_children)):
        for i in range(binary):
            individual = deepcopy(RULESET[randrange(POPULATION_SIZE)])
            if (return_children[children] is None) or individual.fitness > return_children[children].fitness:
                return_children[children] = individual

    return return_children

def rouletteSelection():
    return_children = [None, None]

    # Sum of all fitness
    max = 0;
    for i in RULESET[:]:
        max += int(i.fitness)

    for children in range(len(return_children)):
        pick = randrange(0, max)
        current = 0
        for individual in RULESET[:]:
            current += int(individual.fitness)
            if current > pick:
                return_children[children] = deepcopy(individual)
                break
    
    return return_children

def crossover(parents):
    children = [];

    parent1 = parents[0].toArray()
    parent2 = parents[1].toArray()

    # above 0 and not parent1 length
    ranNum = randrange(1, len(parent1) - 1);

    parents[0].fromArray((parent1[:ranNum] + parent2[ranNum:]))
    parents[1].fromArray((parent2[:ranNum] + parent1[ranNum:]))

    return parents

def mutate(parents):
    children = [];

    parent1 = parents[0].toArray()
    parent2 = parents[1].toArray()

    ops = [add, sub]

    for number, parent in enumerate(parents[:]):
        parent1 = parent.toArray()
        for c, i in enumerate(parent1[:]):
            if (isinstance(i, int)):
                if 0.1 < random() < (0.1 + MUTATION_RATE):
                    parent1[c] = 1 - int(i);
            else:
                if 0.1 < random() < (0.1 + MUTATION_RATE):
                    done1 = True
                    while (done1):
                        operation = choice(ops)
                        new_number = operation(float(i), float(randomNumberMutation()))
                        if new_number > 0.0 and new_number < 1.0:
                            parent1[c] = str(new_number)
                            done1 = False

        parents[number].fromArray(parent1)

    return parents

# Function: Evaluate
#
def Evaluate(individual_solution):
    global BESTINDIVIDUAL, TRAINING_DATA

    fitness = 0

    for td in TRAINING_DATA[:]:
        for i in individual_solution.ruleSet[:]:
            correct = 0
            for condition_count, c in enumerate(td.condition[:]):
                if float(c) >= i.rules[condition_count].low() and float(c) <= i.rules[condition_count].high():
                    correct += 1;
                    continue;

            if correct == 6:
                if str(td.out) == str(i.out):
                    fitness += 1;
                break;

    individual_solution.fitness = int(fitness)

    if individual_solution.fitness > BESTINDIVIDUAL.fitness:
        BESTINDIVIDUAL = deepcopy(individual_solution)

def main():
    global RULESET

    load_dataset = getFile()
    pointer = 0

    # Load Training Data
    for i in TRAINING_DATA[:]:
        split = load_dataset[pointer].split(" ")
        i.condition[0] = split[0]
        i.condition[1] = split[1]
        i.condition[2] = split[2]
        i.condition[3] = split[3]
        i.condition[4] = split[4]
        i.condition[5] = split[5]
        i.out = split[6]
        pointer += 1

    # Load Testing Data
    for i in TEST_DATA[:]:
        split = load_dataset[pointer].split(" ")
        i.condition[0] = split[0]
        i.condition[1] = split[1]
        i.condition[2] = split[2]
        i.condition[3] = split[3]
        i.condition[4] = split[4]
        i.condition[5] = split[5]
        i.out = split[6]
        pointer += 1

    createPopulation()

    #BESTINDIVIDUAL.printOut()
    #writeToFile(0)

    generations = 1
    while (generations < 1500):
    #while (BESTINDIVIDUAL.fitness < 1000):
        child_population = []

        while len(child_population) < POPULATION_SIZE:
            # Selection
            parent = rouletteSelection()

            # Crossover
            children = crossover(parent)

            # Mutate
            children = mutate(children)

            # Evaluate
            Evaluate(children[0])
            Evaluate(children[1])

            child_population.append(children[0])
            child_population.append(children[1])

        RULESET += child_population
        RULESET.sort(key=lambda x: x.fitness, reverse=True)

        print BESTINDIVIDUAL.fitness
        print BESTINDIVIDUAL.printOut()

        for i in range(POPULATION_SIZE):
            RULESET.pop()

        print ("\nGenerations: "+ str(generations) + "\n\n")

        printString = ""

        for i in RULESET[:]:
            printString += str(i.fitness) + ", "

        print printString
        generations += 1
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Didn't find the best solution"
        print BESTINDIVIDUAL.printOut()
