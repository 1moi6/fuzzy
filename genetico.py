import numpy as np
import random

class genetico():
	def __init__(self):
		self.objetivo = lambda x:sum(x)
		self.tol = 1.0e-5
		self.nGenetations = 10000
		self.tCrom = 36
		self.genValues = [i for i in range(6)]
		self.nPop = 100
		self.population = [[random.choice(self.genValues) for _ in range(self.tCrom)] for i in range(self.nPop)]
		self.fitness = [np.nan for _ in range(self.tCrom)]
		self.params = {"nParents":int(0.4*self.nPop),
						"sizeCrossover":int(0.4*self.nPop),
						"sizeMutation":int(0.2*self.nPop),
						"mutationRate": 5/self.tCrom}
	
	def crossover(self,parents,size):
		childs = []
		while (len(childs)<size):
			parent1,parent2 = random.choices(parents,k=2)
			crossover_point = random.randint(5, len(parent1) - 5)
			childs.append(parent1[:crossover_point] + parent2[crossover_point:])
			
		return childs
	
	def mutate(self,parents,size):
		mutated_individuals = []
		while (len(mutated_individuals)<size):
			individual = random.choice(parents)
			mutated_individual = []
			for gene in individual:
				if random.random() < self.params["mutationRate"]:
					mutated_individual+= [min(max(0,gene+random.choice([-1,1])),5)]
				else:
					mutated_individual += [gene]
			
			mutated_individuals.append(mutated_individual)
		
		return mutated_individuals

	# Algoritmo genético
	def genetic_algorithm(self):
		generation = 1
		contagem = 0
		best0 = 1
		while generation < self.nGenetations and contagem<50:
			new_population = []
			self.fitness = [self.objetivo(individual) for individual in self.population]	
			idx_parents = np.argsort(self.fitness)[0:self.params["nParents"]]
			print(f"Generation {generation}: Best fitness = {self.fitness[idx_parents[0]]}, Best individual = {self.population[idx_parents[0]]}")

			parents = [self.population[i] for i in idx_parents]
			new_population.extend(parents)
			newchilds = self.crossover(parents,self.params["sizeCrossover"])
			new_population.extend(newchilds)
			newmutateds = self.mutate(new_population,self.params["sizeMutation"]) 
			new_population.extend(newmutateds)
			self.population = new_population
			generation = generation + 1
			best1 = self.fitness[idx_parents[0]]
			diferenca = np.abs(best0-best1)<self.tol
			if diferenca:
				contagem = contagem +1
			else:
				contagem = 0
			best0 = self.fitness[idx_parents[0]]  
