#!/usr/bin/env python3
# -*- coding: utf-8 -*

from random import random
from Individual import Individual

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
		chromossome = individual.getChromossome()
		sp_score = 0
		gap_penalty = 0
		size_sequence = individual.getLenAlignment()

		# Realiza a soma dos match/mismatch e o gap_penalty dos pares alinhados
		for i in range(0, len(chromossome)):
			seq1 = chromossome[i]

			for j in range(i+1, len(chromossome)):
				seq2 = chromossome[j]
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
					gap_penalty += self.__quasi_natural_gap(sequence1, sequence2)
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
			self.__objctive_function(individual)

		self.__population = sorted(self.__population, key=lambda indiv: indiv.getFitness(), reverse=True)


	"""
	Principal metodo do saga, o qual realizará a execução do algoritmo genetico, possui como 
	parametro o alinhamento a ser realizado
	"""
	def execute(self, alignment):
		self.__initialPopulation(alignment)
		self.__scorePopulation()


	"""
	Realiza a apresentacao de todos os cromossomos da geracao atual
	"""
	def current_generation(self):
		print("Generation: %d" % self.__generation)
		cont = 0
		for indiv in self.__population:
			print("index[%d] = <fitness: %d>" % (cont, indiv.getFitness()))
			cont += 1