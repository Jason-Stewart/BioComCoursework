from random import randrange, random, uniform
import re
import string
import copy

RULE_SIZE = 10
CONDITION_LENGTH = 5
POPULATION_SIZE = 50

MUTATION_RATE = 0.14

CHOOSE = [
    {0:"tournament", 1:"one", 2:"bitwise"},
    {0:"roulette", 1:"one", 2:"bitwise"},
    {0:"rank", 1:"one", 2:"bitwise"},
]

PICK = CHOOSE[0]

class Rule:
    def __init__(self, condition, out):
        self.condition = condition
        self.out = out

class RuleSet:
    def __init__(self):
        self.ruleset = [Rule("", "") for _ in range(RULE_SIZE)]
        self.fitness = 0

THEDATASET = [Rule(None, None) for _ in range(32)]
ruleSet = [RuleSet() for _ in range(POPULATION_SIZE)]
BESTINDIVIDUAL = RuleSet()

# Function: getFile
# Load dataset into array and return

def get_file(fileName):
    lines = [];
    fileOpen = open("./" + fileName + ".txt", "r").read().splitlines()
    for line in fileOpen:
        lines.append(line)
    lines.pop(0)
    
    return lines;

# Function: writeToFile
# Open file and amend fitness stats

def writeToFile(generation):
    sum = 0
    for i in ruleSet[:]:
        sum += i.fitness
    average = sum / len(ruleSet)

    lines = []
    file_open = open("./outputGA2A.txt", "r").read().splitlines()
    count = 0
    for line in file_open:
        if str(count) == str(generation):
            lines.append(line + ", " + str(average) + ", " + str(BESTINDIVIDUAL.fitness))
        else:
            lines.append(line)
        count += 1

    if count == generation:
        lines.append(str(average)+ ", " + str(BESTINDIVIDUAL.fitness))

    file_save = open("./outputGA2A.txt", 'w');
    for line in lines:
        file_save.write(line + "\n")
    file_save.close();

# Function: createPopulation
# Create the initial population

def createPopulation():
    for ruleObject in ruleSet[:]:
        for ruleObjectKey in range(RULE_SIZE):
            ruleObject.ruleset[ruleObjectKey].condition = ""
            for binaryString in range(CONDITION_LENGTH):
                ruleObject.ruleset[ruleObjectKey].condition += str(randrange(3))
            ruleObject.ruleset[ruleObjectKey].out = str(randrange(2))
        
        fitnessFunction(ruleObject);
    return;

# Function: tournamentSelection
# Implementation of tournament selection

def tournamentSelection(binary):
    return_children = [None, None]

    for children in range(len(return_children)):
        for i in range(binary):
            individual = ruleSet[randrange(POPULATION_SIZE)]
            if (return_children[children] is None) or individual.fitness > return_children[children].fitness:
                return_children[children] = individual

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
        p = uniform(0, max)
        for i, f in enumerate(ruleSet[:]):
            if p < 0:
                break
            p -= f.fitness;
        return_children[children] = copy.deepcopy(f)
    
    return return_children

# Function: rankSelection
# Implementation of rank selection

def rankSelection():
    return_children = [None, None]

    rankTotal = (POPULATION_SIZE * (POPULATION_SIZE + 1)) / 2

    for children in range(len(return_children)):
        p = uniform(0, rankTotal)
        for i, f in enumerate(ruleSet[:]):
            if p < 0:
                break
            p -= (POPULATION_SIZE - i);
        return_children[children] = copy.deepcopy(f)

    return return_children

# Function: crossover
#

def crossover(parent):
    returnChildren = [RuleSet(), RuleSet()]

    parent1 = parent[0]
    parent2 = parent[1]

    parent1concat = ""
    for parent1rules in parent1.ruleset[:]: parent1concat += parent1rules.condition + parent1rules.out

    parent2concat = ""
    for parent2rules in parent2.ruleset[:]: parent2concat += parent2rules.condition + parent2rules.out

    randomNum = randrange(1, (len(parent1concat) - 1))
    children1concat = parent1concat[:randomNum] + parent2concat[randomNum:]
    children2concat = parent2concat[:randomNum] + parent1concat[randomNum:]

    children1split = [children1concat[i:i+(CONDITION_LENGTH + 1)] for i in range(0, len(children1concat), (CONDITION_LENGTH + 1))]
    children2split = [children2concat[i:i+(CONDITION_LENGTH + 1)] for i in range(0, len(children2concat), (CONDITION_LENGTH + 1))]

    key = 0;
    for children in children1split[:]:
        returnChildren[0].ruleset[key].condition = children[:CONDITION_LENGTH]
        if (children[CONDITION_LENGTH] == 2):
            returnChildren[0].ruleset[key].out = 1
        else:
            returnChildren[0].ruleset[key].out = children[CONDITION_LENGTH]
        key += 1;

    key = 0;
    for children in children2split[:]:
        returnChildren[1].ruleset[key].condition = children[:CONDITION_LENGTH]
        if (children[CONDITION_LENGTH] == 2):
            returnChildren[1].ruleset[key].out = 1
        else:
            returnChildren[1].ruleset[key].out = children[CONDITION_LENGTH]
        key += 1;

    return returnChildren;

# Function: mutate
# 

def mutate(children):
    for number in range(len(children)):
        parent1concat = ""
        for parent1rules in children[number].ruleset[:]: 
            parent1concat += parent1rules.condition + parent1rules.out

        word = "";

        for count, letter in enumerate(parent1concat[:], 1):
            if count % (CONDITION_LENGTH + 1) == 0:
                if 0.1 < random() < (0.1 + MUTATION_RATE):
                    word += str(randrange(2))
                else:
                    word += letter 
            elif 0.1 < random() < (0.1 + MUTATION_RATE):
                word += str(randrange(3))
            else:
                word += letter

        parent1concat = word

        children1split = [parent1concat[i:i+(CONDITION_LENGTH + 1)] for i in range(0, len(parent1concat), (CONDITION_LENGTH + 1))]

        key = 0;
        for whatever in children1split[:]:
            children[number].ruleset[key].condition = whatever[:CONDITION_LENGTH]
            children[number].ruleset[key].out = whatever[CONDITION_LENGTH]
            key += 1;

    return children;

# Function: fitnessFunction
#

def fitnessFunction(individual_solution):
    global BESTINDIVIDUAL

    fitness = 0;

    for rule in THEDATASET[:]:
        for solution in individual_solution.ruleset[:]:
            tryVariable = string.replace(solution.condition, "2", "[0-1]")
            if (re.match(tryVariable, rule.condition) is not None):
                if (solution.out == rule.out):
                    fitness+=1
                break;
    
    individual_solution.fitness = fitness

    if (individual_solution.fitness > BESTINDIVIDUAL.fitness):
        BESTINDIVIDUAL = copy.deepcopy(individual_solution)

# Function: main
#

def main():
    global ruleSet, CONDITION_LENGTH, THEDATASET

    #Load dataset into a object
    dataSet = get_file("data2")

    lengthData = dataSet[0].split(" ")
    CONDITION_LENGTH = len(lengthData[0])

    THEDATASET = [Rule(None, None) for _ in range(len(dataSet))]

    key = 0
    for i in THEDATASET[:]:
        split = dataSet[key].split(" ")
        i.condition = split[0]
        i.out = split[1]
        key += 1

    # create a basic population
    createPopulation()
    writeToFile(0)

    generations = 1;
    while (generations < 100):
        child_population = [];

        while (len(child_population) < POPULATION_SIZE):
            # Selection
            if PICK[0] == "rank":
                parent = rankSelection()
            elif PICK[0] == "roulette":
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

        # Output stats ect
        writeToFile(generations)

        print BESTINDIVIDUAL.fitness

        generations += 1;
    
    print("Generations Tested: " + str(generations))
    print("Current Best Fitness: " + str(BESTINDIVIDUAL.fitness))

    print("\nFound Solution: \n")

    for i in BESTINDIVIDUAL.ruleset[:]:
        print(i.condition + " "+ i.out);

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Didn't find the best solution"
        print BESTINDIVIDUAL.printOut()
