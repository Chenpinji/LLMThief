import json
import random
import argparse
import os
import importlib.util
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from seeds_constructor.seed import *
from mutator.standalone_mutator import *

shadow_num = 3
desired_population_size = 100
chromosome_length = 6
first_gene_range = list(range(10))  # 0..9
other_genes_range = list(range(4))  # 0..3
unique_chromosomes = set()
quicktop = int(0.1 * desired_population_size)
select = int(0.5 * desired_population_size)
crossnum = int(0.36 * desired_population_size)
mutationnum = int(0.1 * crossnum)
# interaction part

class Chromosome:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.prompt = None
        self.score = 0
    def chromosome2prompt(self, init_prompt):
        self.prompt = init_prompt
        base_mutators = [
            synonym_replacing,
            character_stuffing,
            scenario_simulating,
            language_switching,
            suffix_guiding
        ]
        for i, mutator in enumerate(base_mutators):
            if self.chromosome[i + 1] != 0:
                self.prompt = mutator(self.prompt, self.chromosome[i + 1])
def crossover_chromosome(chromosome1, chromosome2):
    crossover_point = random.randint(1, len(chromosome1.chromosome) - 1)
    new_chromosome1 = chromosome1.chromosome[:crossover_point] + chromosome2.chromosome[crossover_point:]
    new_chromosome2 = chromosome2.chromosome[:crossover_point] + chromosome1.chromosome[crossover_point:]
    return Chromosome(new_chromosome1), Chromosome(new_chromosome2)
def mutation_chromosome(chromosome):
    new_chromosome = chromosome.chromosome.copy()
    mutation_point = random.randint(0, len(new_chromosome) - 1)
    if mutation_point == 0:
        new_chromosome[mutation_point] = random.choice([i for i in range(10) if i != new_chromosome[mutation_point]])
    else:
        new_chromosome[mutation_point] = random.choice([i for i in range(4) if i != new_chromosome[mutation_point]])
    return Chromosome(new_chromosome)
# genetic part
def genetic_algorithm(shadow_url, shadow_ground_truth, shadow_seeds, platform):
    
    for pos in range(chromosome_length):
        if pos == 0:
            for value in first_gene_range:
                while True:
                    chromosome = [random.choice(first_gene_range if i == 0 else other_genes_range) 
                                 for i in range(chromosome_length)]
                    chromosome[pos] = value
                    chromosome_tuple = tuple(chromosome)
                    if chromosome_tuple not in unique_chromosomes:
                        unique_chromosomes.add(chromosome_tuple)
                        break
        else:
            for value in other_genes_range:
                while True:
                    chromosome = [random.choice(first_gene_range if i == 0 else other_genes_range) 
                                 for i in range(chromosome_length)]
                    chromosome[pos] = value
                    chromosome_tuple = tuple(chromosome)
                    if chromosome_tuple not in unique_chromosomes:
                        unique_chromosomes.add(chromosome_tuple)
                        break

    while len(unique_chromosomes) < desired_population_size:
        chromosome = [random.choice(first_gene_range if i == 0 else other_genes_range) 
                     for i in range(chromosome_length)]
        chromosome_tuple = tuple(chromosome)
        unique_chromosomes.add(chromosome_tuple)

    population = [list(ch) for ch in unique_chromosomes]
    random.shuffle(population)
    # print(population)
    population = [Chromosome(chromosome) for chromosome in population]

    module_path = f"../interactor/{platform}/attack_{platform}_instruction.py"
    spec = importlib.util.spec_from_file_location(f"attack_{platform}_instruction", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"interactor.{platform}.attack_{platform}_instruction"] = module
    spec.loader.exec_module(module)
    evaluate_mutation = getattr(module, "mutation_interaction")

    iteration = 0
    while iteration < 30:
        iteration += 1
        for url, ground_truth, seeds in zip(shadow_url, shadow_ground_truth, shadow_seeds):
            for chromosome in population:
                init_prompt = seeds[chromosome.chromosome[0]]
                chromosome.chromosome2prompt(init_prompt)
                print("================================================")
                print(chromosome.prompt)
                print(chromosome.score)
                import time
                # time.sleep(20)
                score = evaluate_mutation(chromosome.prompt, url, ground_truth)
                print(score)
                chromosome.score += score
        
        population.sort(key=lambda x: x.score, reverse=True)
        for chromosome in population:
            chromosome.score = chromosome.score / shadow_num
            print(chromosome.score)
        # assert False
        sum_score = 0
        for i in range(int(desired_population_size / 4)):
            sum_score += population[i].score
        if sum_score >= 0.75 * int(desired_population_size / 4):
            break
        
        top_10 = population[:quicktop]
        
        remaining_population = population[quicktop:] 
        
        total_fitness = sum(chromosome.score for chromosome in remaining_population)
        
        if total_fitness == 0:
            selected_50 = random.sample(remaining_population, min(select, len(remaining_population)))
        else:
            selected_50 = []
            for _ in range(min(select, len(remaining_population))):
                random_value = random.uniform(0, total_fitness)
                
                cumulative_fitness = 0
                for chromosome in remaining_population:
                    cumulative_fitness += chromosome.score
                    if cumulative_fitness >= random_value:
                        selected_50.append(chromosome)
                        break
        
        next_population = top_10 + selected_50
        # crossover
        crossover_population = []
        for i in range(len(next_population)):
            for j in range(i + 1, len(next_population)):
                if random.random() < 0.6:
                    print("====================Crossover=====================")
                    print(next_population[i].chromosome)
                    print(next_population[j].chromosome)
                    new_chromosome1, new_chromosome2 = crossover_chromosome(next_population[i],next_population[j])
                    print(new_chromosome1.chromosome)
                    print(new_chromosome2.chromosome)
                    print("================================================")
                    crossover_population.append(new_chromosome1)
                    crossover_population.append(new_chromosome2)
                if len(crossover_population) >= crossnum:
                    break
            if len(crossover_population) >= crossnum:
                break
        # mutation
        mutation_population = []
        for chromosome in crossover_population:
            if random.random() < 0.1:
                print("====================Mutation=====================")
                print(chromosome.chromosome)
                temp = mutation_chromosome(chromosome)
                print(temp.chromosome)
                print("================================================")
                mutation_population.append(temp)

        next_population = next_population + crossover_population + mutation_population
        population = []
        for chromosome in next_population:
            new_chromosome = Chromosome(chromosome.chromosome.copy())
            new_chromosome.score = 0
            population.append(new_chromosome)

    return population


def main(platform, type):
    if type == "instruction":
        file_path = f"../ground_truth/preparation/{platform}_pre/{platform}_attack_{type}_pre.json"
        with open(file_path, 'r', encoding='utf-8') as file:
            i = 0
            shadow_url = []
            shadow_ground_truth = []
            shadow_seeds = []
            for line in file:
                i += 1
                if i > shadow_num:
                    break
                data = json.loads(line)
                url = data['URL']
                shadow_url.append(url)
                ground_truth = data['Prompt Leaking']['public system prompt']
                shadow_ground_truth.append(ground_truth)
                seeds = initial_seeds(data, platform, type, 4)
                shadow_seeds.append(seeds)
            mutation_result = genetic_algorithm(shadow_url, shadow_ground_truth, shadow_seeds, platform)
            reslist = []
            for chromosome in mutation_result:
                reslist.append({
                    "chromosome": chromosome.chromosome,
                    "prompt": chromosome.prompt,
                    "score": chromosome.score
                })
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output_{platform}_{type}_{timestamp}_{shadow_num}_{desired_population_size}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(reslist, f, ensure_ascii=False, indent=4)
    return mutation_result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Select platform for attack prompt generation.')
    parser.add_argument('-p', '--platform', choices=['ali', 'openai', 'baidu','hug','flowgpt','coze','poe'], required=True, help='indicate the LLM app store to launch LLMThief')
    parser.add_argument('-t', '--type', choices=['instruction', 'api', 'knowledge'], required=True, help='indicate the LLMThief attack type')
    #Usage: python main.py -p ali -t instruction
    args = parser.parse_args()
    main(args.platform, args.type)