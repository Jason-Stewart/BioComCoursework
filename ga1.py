from random import randrange, random, uniform
import copy

RULE_SIZE = 15
MODEL_SIZE = 32
CONDITION_LENGTH = 5
POPULATION_SIZE = 50

MUTATION_RATE = 0.01

SELECTION = "rank" #tournament, roulette, rank
CROSSOVER = "one" # One point, Two-point Crossover
MUTATION = "bitwise" #bitwise


class Rule(object):
    def __init__(self, condition, out):
        self.condition = condition
        self.out = out

class RuleSet(object):
    def __init__(self):
        self.ruleset = [Rule("", "") for _ in range(RULE_SIZE)]
        self.fitness = 0

THEDATASET = [Rule(None, None) for _ in range(MODEL_SIZE)]
ruleSet = [RuleSet() for _ in range(POPULATION_SIZE)]
BESTINDIVIDUAL = RuleSet()

# Function: getFile
# Load dataset into array and return

def getFile(fileName):
    lines = []
    fileOpen = open("./" + fileName + ".txt", "r").read().splitlines()
    for line in fileOpen:
        lines.append(line)
    lines.pop(0)

    return lines

# Function: writeToFile
# Open file and amend fitness stats

def writeToFile(generation):
    average = 0
    for i in ruleSet[:]:
        average += i.fitness
    average = average / len(ruleSet)

    lines = []
    file_open = open("./outputGA1.txt", "r").read().splitlines()
    count = 0
    for line in file_open:
        if str(count) == str(generation):
            lines.append(line + ", " + str(average))
        else:
            lines.append(line)
        count += 1

    if count == generation:
        lines.append(str(average))

    file_save = open("./outputGA1.txt", 'w')
    for line in lines:
        file_save.write(line + "\n")
    file_save.close()

# Function: createPopulation
# Create the initial population

def createPopulation():
    for rule_object in ruleSet[:]:
        for rule_object_key in range(RULE_SIZE):
            rule_object.ruleset[rule_object_key].condition = ""
            for i in range(CONDITION_LENGTH):
                rule_object.ruleset[rule_object_key].condition += str(randrange(2))
            rule_object.ruleset[rule_object_key].out = str(randrange(2))

        fitnessFunction(rule_object)
    return

# Function: tournamentSelection
# Implementation of tournament selection

def tournamentSelection(binary):
    return_children = [None, None]

    for children in range(len(return_children)):
        for i in range(binary):
            individual = ruleSet[randrange(POPULATION_SIZE)]
            if (return_children[children] is None) or individual.fitness > return_children[children].fitness:
                return_children[children] = copy.copy(individual)

    return return_children

# Function: rouletteSelection
# Implementation of roulette selection

def rouletteSelection():
    return_children = [None, None]

    # Sum of all fitness
    max = 0;
    for i in ruleSet[:]:
        max += int(i.fitness)

    for children in range(len(return_children)):
        pick = randrange(0, max)
        current = 0
        for individual in ruleSet[:]:
            current += int(individual.fitness)
            if current > pick:
                return_children[children] = copy.copy(individual)
                break
    
    return return_children

# Function: rankSelection
# Implementation of rank selection

def rankSelection():
    return_children = [None, None]

    for children in range(len(return_children)):

    return return_children

# Function: crossover
#

def crossover(parent):
    returnChildren = [RuleSet(), RuleSet()]

    parent1 = parent[0]
    parent2 = parent[1]

    parent1concat = ""
    for parent1rules in parent1.ruleset[:]:
        parent1concat += parent1rules.condition + parent1rules.out

    parent2concat = ""
    for parent2rules in parent2.ruleset[:]:
        parent2concat += parent2rules.condition + parent2rules.out

    randomNum = randrange(1, (len(parent1concat) - 1))
    children1concat = parent1concat[:randomNum] + parent2concat[randomNum:]
    children2concat = parent2concat[:randomNum] + parent1concat[randomNum:]

    children1split = [children1concat[i:i+6] for i in range(0, len(children1concat), 6)]
    children2split = [children2concat[i:i+6] for i in range(0, len(children2concat), 6)]

    for key, children in enumerate(children1split[:]):
        returnChildren[0].ruleset[key].condition = children[:5]
        returnChildren[0].ruleset[key].out = children[5]

    for key, children in enumerate(children2split[:]):
        returnChildren[1].ruleset[key].condition = children[:5]
        returnChildren[1].ruleset[key].out = children[5]

    return returnChildren

# Function: mutate
# 

def mutate(children):
    for number in range(len(children)):
        parent1concat = ""
        for parent1rules in  children[number].ruleset[:]:
            parent1concat += parent1rules.condition + parent1rules.out

        for letter in parent1concat[:]:
            if 0.1 < random() < (0.1 + MUTATION_RATE):
                letter = str(1 - int(letter))

        children1split = [parent1concat[i:i+6] for i in range(0, len(parent1concat), 6)]

        key = 0
        for whatever in children1split[:]:
            children[number].ruleset[key].condition = whatever[:5]
            children[number].ruleset[key].out = whatever[5]
            key += 1

    return children

# Function: fitnessFunction
#

def fitnessFunction(individual_solution):
    global BESTINDIVIDUAL

    fitness = 0

    for rule in THEDATASET[:]:
        for solution in individual_solution.ruleset[:]:
            if solution.condition == rule.condition:
                if solution.out == rule.out:
                    fitness += 1
                break

    individual_solution.fitness = fitness

    if individual_solution.fitness > BESTINDIVIDUAL.fitness:
        BESTINDIVIDUAL = copy.copy(individual_solution)

# Function: main
#

def main():
    global ruleSet

    #Load dataset into a object
    load_data_set = getFile("data1")
    key = 0
    for i in THEDATASET[:]:
        split = load_data_set[key].split(" ")
        i.condition = split[0]
        i.out = split[1]
        key += 1

    # create a basic population
    createPopulation()
    writeToFile(0)

    generations = 1
    while BESTINDIVIDUAL.fitness < RULE_SIZE:
    #while (generations < 200):
        child_population = []

        while len(child_population) < POPULATION_SIZE:
            # Selection
            if SELECTION == "rank":
                parent = rankSelection()
            elif SELECTION == "roulette":
                parent = rouletteSelection()
            else:
                parent = tournamentSelection(2)

            # Crossover
            children = crossover(parent)

            # Mutate
            children = mutate(children)

            # Evaluate
            fitnessFunction(children[0])
            fitnessFunction(children[1])

            child_population.append(children[0])
            child_population.append(children[1])

        # Survive of the Fittest
        ruleSet = ruleSet + child_population
        ruleSet.sort(key=lambda x: x.fitness, reverse=True)

        for i in range(POPULATION_SIZE):
            ruleSet.pop()

        # Output stats ect
        writeToFile(generations)

        generations += 1
    
    print("Generations Tested: " + str(generations))
    print("Current Best Fitness: " + str(BESTINDIVIDUAL.fitness))

    print("\nThe Found Solution: \n")

    for i in BESTINDIVIDUAL.ruleset[:]:
        print(i.condition + " "+ i.out)
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Didn't find the best solution"
        print BESTINDIVIDUAL.printOut()
