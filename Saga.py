#!/usr/bin/env python3
# -*- coding: utf-8 -*

from random import random
from Individual import Individual
from Operator import Operator

class Saga():
	def __init__(self, populationSize = 20, numGenerations = 100, mutationRate = 0.1):
		self.__population = []
		self.__populationSize = populationSize
		self.__generation = 0
		self.__numGenerations = numGenerations
		self.__mutationRate = mutationRate
		self.__bestSolution = 0
		self.__best = []
		self.__worstSolution = 0 # Para efeitos de testes
		self.__worst = [] # Para efeito de testes


	"""
	A partir do alinhamento informado cria uma populacao de individuos randomicos
	"""
	def __initialPopulation(self, alignment):
		for i in range(0, self.__populationSize):
			self.__population.append(Individual(alignment))
		

	"""
	Funcao objetivo, realiza o calculo de fitness por meio do metodo da soma de pares
	com natural affine gap penalty (mode="natural") ou com quasi-natural affine 
	gap penalty (mode="quasi") e por meio da matrizes de pesos (Blosum/Pam)
	"""
	def __objctive_function(self, individual, mode="natural"):
		chromosome = individual.getChromosome()
		sp_score = 0
		gap_penalty = 0
		size_sequence = individual.getLenAlignment()

		# Realiza a soma dos match/mismatch e o gap_penalty dos pares alinhados
		for i in range(0, len(chromosome)):
			seq1 = chromosome[i]

			for j in range(i+1, len(chromosome)):
				seq2 = chromosome[j]
				seq_aux1 = seq_aux2 = ""

				# Calcula o valor de match/mismatch das colunas do alinhamento
				for k in range(0, size_sequence):
					if seq1[k] != '*' or seq2[k] != '*':
						seq_aux1 += seq1[k]
						seq_aux2 += seq2[k]
						sp_score += self.__calc_score(seq1[k], seq2[k])

				# Calcula o gap penalty das sequencias alinhadas
				if mode == "natural":
					gap_penalty += self.__natural_gap(seq_aux1)
					gap_penalty += self.__natural_gap(seq_aux2)
				elif mode == "quasi":
					gap_penalty += self.__quasi_natural_gap(seq1, seq2)
				else:
					raise NameError("The object function mode is invalid!")
		individual.setFitness(sp_score + gap_penalty)


	"""
	Realiza o calculo do custo de gap da sequencia informada por meio de metodo 
	natural affine gap penalties
	"""
	def __natural_gap(self, sequence, gap_open=-1, gap_extend=-2):
		gap_length = 0
		num_open = 0
		flag = 0

		for i in range(0, len(sequence)):
			# abertura de um gap
			if sequence[i] == '*' and flag == 0:
				flag = 1
			# extencao de gap
			if sequence[i] == '*' and flag == 1:
				num_open += 1
				gap_length += 1
			else:
				flag = 0

		gap_length -= num_open
		num_open *= gap_open

		return num_open + gap_length*gap_extend


	"""
	Realiza o calculo do custo de gap da sequencia informada por meio de metodo 
	quasi-natural affine gap penalties
	"""
	def __quasi_natural_gap(self, sequence1, sequence2):
		pass


	"""
	Realiza o calculo do score entre as proteinas informadas por meio da matriz de pesos. 
	Caso seja nucleotideos e retornado o valor de match/mismatch
	"""
	def __calc_score(self, char1, char2, alignment_type="protein", matrix="pam250", match=2, mismatch=-1):
		if alignment_type == "protein":
			local = "./matrices/"+ matrix +".txt"

			with open(local) as file:
				amino_acids = " ARNDCQEGHILKMFPSTWYVBZX*"
				i = amino_acids.index(char1)
				j = 3*amino_acids.index(char2)
				
				for k in range(0, i + 1):
					amino_acids = file.readline()

				score = int(amino_acids[j-1:j+1])
			return score
		else:
			if char1 == char2:
				return match
			return mismatch


	"""
	Calcula o fitness de cada individuo da população atual, e a ordena com base neste valor
	"""
	def __scorePopulation(self):
		for individual in self.__population:
			self.__objctive_function(individual, "natural")

		self.__population = sorted(self.__population, key=lambda indiv: indiv.getFitness(), reverse=True)


	"""
	Realiza a normalizacao do valor de fitness para a realização da selecao dos pais
	"""
	def __calc_offspring(self):

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
	def __select_parent(self):
		sum_offspring = 0
		for indiv in self.__population:
			sum_offspring += indiv.getOffspring()

		relat_aptitude = []
		for indiv in self.__population:
			relat_aptitude.append(indiv.getOffspring()/sum_offspring)
		
		spin = random()*sum_offspring
		# print("spin = %f" % spin)
		i = 0
		while i < self.__populationSize and spin > 0:
			spin -= relat_aptitude[i]
			i += 1

		# print("parent selected = %d" % i)
		return self.__population[i]

	"""
	Principal metodo do saga, o qual realizará a execução do algoritmo genetico, possui como 
	parametro o alinhamento a ser realizado
	"""
	def execute(self, alignment):
		operator_obj = Operator()
		self.__initialPopulation(alignment)
		self.__scorePopulation()

		while self.__generation < self.__numGenerations:
			list_replaced = [] # lista de individuo indicados a proxima geração
			for i in range(0, int(self.__populationSize/2)):
				list_replaced.append(self.__population[i])

			self.__calc_offspring()
			list_child = [] # lista de filhos gerados

			# Realiza uma amostragem estocatisca sem reposição
			while True:
				if len(list_child) < (self.__populationSize - len(list_replaced)):
					# seleciona o operador e armazena o numero de parents
					num_parent = operator_obj.select_operator()
					
					parent1 = self.__select_parent()
					child1 = parent1.clone()
					if num_parent == 2:
						parent2 = self.__select_parent()
						child2 = parent2.clone()
						operator_obj.run_operator(child1, parent2=child2)
						
					else:
						operator_obj.run_operator(child1)
						list_child.append(child1)
				else:
					break
			self.__generation = self.__numGenerations


	"""
	Realiza a apresentacao de todos os cromossomos da geracao atual
	"""
	def current_generation(self):
		print("Generation: %d" % self.__generation)
		cont = 0
		for indiv in self.__population:
			print("index[%d] = <fitness: %d>" % (cont, indiv.getFitness()))
			cont += 1