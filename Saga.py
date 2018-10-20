#!/usr/bin/env python3
# -*- coding: utf-8 -*

from random import random
from Individual import Individual
from Operator import Operator

class Saga():
	def __init__(self, population_size = 20, num_generations = 100, mutation_rate = 0.1):
		self.__population = []
		self.__population_size = population_size
		self.__current_generation = 0
		self.__num_generations = num_generations
		self.__mutation_rate = mutation_rate
		self.__bestSolution = 0
		self.__best = []
		self.__worstSolution = 0 # Para efeitos de testes
		self.__worst = [] # Para efeito de testes


	"""
	A partir do alinhamento informado cria uma população de indivíduos randômicos
	"""
	def initialize(self, alignment):
		for i in range(0, self.__population_size):
			indiv = Individual(alignment)
			self.__population.append(indiv)
			# print(indiv.toString())
		

	"""
	Função objetivo, realiza o cálculo de fitness por meio do método da soma de pares
	com natural affine gap penalty (mode="natural") ou com quasi-natural affine 
	gap penalty (mode="quasi") e por meio da matrizes de pesos (Blosum/Pam)
	"""
	def fitness(self, individual, mode="natural"):
		chromosome = individual.getChromosome()
		sp_score = 0
		gap_penalty = 0
		size_sequence = individual.getLenAlignment()

		# Realiza a soma dos match/mismatch e o gap_penalty dos pares alinhados
		for i in range(0, len(chromosome)):
			seq1 = chromosome[i]

			for j in range(i+1, len(chromosome)):
				seq2 = chromosome[j]
				seq_aux1 = ""
				seq_aux2 = ""

				# Calcula o valor de match/mismatch das colunas do alinhamento
				# print("size_sequence = %d" % size_sequence)
				# print("len_seq1 %d\nlen_seq2 %d" % (len(seq1), len(seq2)))
				for k in range(0, size_sequence):
					if seq1[k] != '-' or seq2[k] != '-':
						seq_aux1 += seq1[k]
						seq_aux2 += seq2[k]
						sp_score += self.score(seq1[k], seq2[k])

				# Calcula o gap penalty das sequencias alinhadas
				if mode == "natural":
					gap_penalty += self.gap_penalties(seq_aux1)
					gap_penalty += self.gap_penalties(seq_aux2)
				elif mode == "quasi":
					gap_penalty += self.__quasi_natural_gap(seq1, seq2)
				else:
					raise NameError("The object function mode is invalid!")
		individual.setFitness(sp_score + gap_penalty)


	"""
	Realiza o cálculo do custo de gap da sequência informada por meio de método 
	natural affine gap penalties
	"""
	def gap_penalties(self, sequence, gap_open=-1, gap_extend=-2):
		gap_length = 0
		num_open = 0
		flag = 0

		for i in range(0, len(sequence)):
			# abertura de um gap
			if sequence[i] == '-' and flag == 0:
				flag = 1
			# extencao de gap
			if sequence[i] == '-' and flag == 1:
				num_open += 1
				gap_length += 1
			else:
				flag = 0

		gap_length -= num_open
		num_open *= gap_open

		return num_open + gap_length*gap_extend


	"""
	Realiza o cálculo do custo de gap da sequência informada por meio de metodo 
	quasi-natural affine gap penalties
	"""
	def __quasi_gap_penalty(self, sequence1, sequence2):
		pass


	"""
	Realiza o cálculo do score entre as proteínas informadas por meio da matriz de pesos. 
	Caso seja nucleotídeos e retornado o valor de match/mismatch
	"""
	def score(self, char1, char2, alignment_type="protein", matrix="pam250", match=2, mismatch=-1):
		if alignment_type == "protein":
			local = "./matrices/"+ matrix +".txt"

			with open(local) as file:
				amino_acids = " ARNDCQEGHILKMFPSTWYVBZX-"
				i = amino_acids.index(char1)
				j = 3*amino_acids.index(char2)
				
				for k in range(0, i + 1):
					amino_acids = file.readline()

				# print(char1, char2)
				# print(amino_acids[j-1:j+1])
				# print(j)
				score = int(amino_acids[j-1:j+1])
			return score
		else:
			if char1 == char2:
				return match
			return mismatch


	"""
	Calcula o fitness de cada individuo da população atual, e a ordena com base neste valor
	"""
	def scorePopulation(self):
		for individual in self.__population:
			self.fitness(individual, "natural")

		self.__population = sorted(self.__population, key=lambda indiv: indiv.getFitness(), reverse=True)


	"""
	Realiza a normalização do valor de fitness para a realização da seleção dos pais
	"""
	def offspring(self):

		sum_fitness = 0
		for indiv in self.__population:
			sum_fitness += indiv.getFitness()
		
		print("sum_fitness = %d" % sum_fitness)
		for indiv in self.__population:
			indiv.setOffspring(indiv.getFitness()/sum_fitness)
			# print("offspring = %f" % indiv.getOffspring())

	"""
	Realiza a seleção do pai por meio do metodo da roleta, fazendo uso do offspring como 
	parametro de avaliação de aptidão
	"""
	def select(self):
		sum_offspring = 0
		for indiv in self.__population:
			sum_offspring += indiv.getOffspring()

		relat_aptitude = []
		for indiv in self.__population:
			relat_aptitude.append(indiv.getOffspring()/sum_offspring)
		
		spin = random()*sum_offspring
		# print("spin = %f" % spin)
		i = 0
		while i < self.__population_size and spin > 0:
			spin -= relat_aptitude[i]
			i += 1

		# print("selected %d" % i)
		return self.__population[i-1]

	"""
	Principal metodo do saga, o qual realizará a execução do algoritmo genetico, possui como 
	parametro o alinhamento a ser realizado
	"""
	def execute(self, alignment):
		operator_obj = Operator()

		# gera população inicial
		self.initialize(alignment)
		
		self.scorePopulation()

		while self.__current_generation < self.__num_generations:
			# print("current_generation = %d..." % self.__current_generation)
			next_generation = [] # lista de individuo da proxima geração
			
			# seleciona os individuos da proxima geração 50%
			for indiv in self.__population:
				if len(next_generation) >= int(self.__population_size/2):
					break
				clone = indiv.clone(self.__current_generation+1)
				next_generation.append(clone)

			self.offspring()
			# print("offspring calculado...")
			# realiza o preenchimento da lista de filhos
			while len(next_generation) < self.__population_size:
				# seleciona o operador e armazena o numero de parents
				num_parent = operator_obj.select_operator()
				# print("selecting Operator, size next generation = %d..." % len(next_generation))
				# seleciona um parent
				parent1 = self.select()

				# caso o parent seja incapaz de realizar crossover
				if not parent1.getOffspring():
					print("offspring parent1 invalid..")
					continue

				child1 = parent1.clone(self.__current_generation+1)

				# caso o operador necessite de 2 parents
				if num_parent == 2:
					# seleciona o segundo parent
					parent2 = self.select()

					# caso o parent seja incapaz de realizar crossover
					if not parent2.getOffspring():
						print("offspring parent2 invalid..")
						continue

					child2 = parent2.clone(self.__current_generation+1)
					operator_obj.run_operator(child1, parent2=child2)

					# calcula o score dos filhos
					self.fitness(child1, mode="natural")
					self.fitness(child2, mode="natural")

					# adiciona o filho de maior escore, e valido
					if child1.getFitness() > child2.getFitness():
						if not self.__exist(child1, next_generation):
							next_generation.append(child1)
							# print("add child, total generation %d = %d" % (self.__current_generation, len(next_generation)))
						elif not self.__exist(child2, next_generation):
							next_generation.append(child2)
							# print("add child, total generation %d = %d" % (self.__current_generation, len(next_generation)))
						else:
							# print("child exist! (two child)")
							continue
					else:
						if not self.__exist(child2, next_generation):
							next_generation.append(child2)
							# print("add child, total generation %d = %d" % (self.__current_generation, len(next_generation)))
						elif not self.__exist(child1, next_generation):
							next_generation.append(child1)
							# print("add child, total generation %d = %d" % (self.__current_generation, len(next_generation)))
						else:
							# print("child exist! (one child)")
							continue
				else:
					operator_obj.run_operator(child1)

					# calcula o fitness do filho
					self.fitness(child1, mode="natural")

					# verifica se o filho é valido
					if not self.__exist(child1, next_generation):
						next_generation.append(child1)
					else:
						continue
			
			self.__current_generation += 1
			self.__population = next_generation
			self.scorePopulation()

			# armazena os melhores de cada geracao
			self.__bestSolution = self.__population[0]
			self.__best.append(self.__bestSolution)
			print("Best -> %s" % self.__bestSolution.toString())

			# armazena os piores de cada geracao
			self.__worstSolution = self.__population[self.__population_size-1]
			self.__worst.append(self.__worstSolution)
			print("Worst -> %s" % self.__bestSolution.toString())
			print()

			# self.print_generation()


	"""
	Verifica se existe algum indiviuo igual a população informada como parametro
	"""
	def __exist(self, individual, population):
		flag = True
		chromosome = individual.getChromosome()
		# percorre a população
		for indiv in population:
			#percorre as sequencias
			for i, row in enumerate(indiv.getChromosome()):
				if row != chromosome[i]:
					flag = False
					break
			if not flag:
				return flag
		return flag


	"""
	Realiza a apresentacao de todos os cromossomos da geracao atual
	"""
	def print_generation(self):
		print("Generation: %d" % self.__current_generation)
		cont = 0
		for indiv in self.__population:
			print("index[%d] = <fitness: %d>" % (cont, indiv.getFitness()))
			cont += 1