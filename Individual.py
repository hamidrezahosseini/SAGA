#!/usr/bin/env python3
# -*- coding: utf-8 -*

from random import randint

class Individual():
	"""
	Realiza a instanciacao do individual, em que caso o alignment ou a generation nao sejam informados
	os mesmos receberao valores nulos, caso o alignment seja informado o chromosome é inicializado de
	forma randomica a fim de criar a populacao inicial
	"""
	def __init__(self, alignment = [], generation = 0):
		self.__generation = generation
		self.__chromosome = []
		self.__fitness = 0
		self.__expectOffspring = 0 # expected offspring (EO)
		self.__lenAlignment = 0

		for row in alignment:
			self.__chromosome.append(row)
		
		self.__lengthChromosome()

		if self.__lenAlignment:
			self.__randChromosome()


	"""
	Calcula o comprimento da maior sequencia do chromosome
	"""
	def __lengthChromosome(self):
		for row in self.__chromosome:
			self.__lenAlignment = max(self.__lenAlignment, len(row))


	"""
	Inicializa de forma randomica o chromosome, adicionando gaps a direita de cada linha
	até que todos tenham o mesmo comprimento
	"""
	def __randChromosome(self):
		for row in range(0, len(self.__chromosome)):
			while len(self.__chromosome[row]) < self.__lenAlignment:
				j = randint(0, len(self.__chromosome[row])-1)
				self.__chromosome[row] = self.__chromosome[row][0:j].upper() + "-" + self.__chromosome[row][j::].upper()


	"""
	Cria um novo individual com os mesmos atributos
	"""
	def clone(self, generation = -1):
		clone = Individual()

		if generation == -1:
			generation = self.getGeneration()

		# atribui os valores copiados ao clone
		clone.setGeneration(generation)
		clone.setChromosome(self.__chromosome)
		clone.setFitness(self.__fitness)
		clone.setOffspring(self.__expectOffspring)
		return clone


	def setChromosome(self, chromosome):
		self.__chromosome = chromosome
		self.__lengthChromosome()


	def setFitness(self, fitness):
		self.__fitness = fitness


	def setGeneration(self, generation):
		self.__generation = generation


	def setOffspring(self, offspring):
		self.__expectOffspring = offspring


	def getChromosome(self):
		return self.__chromosome


	def getFitness(self):
		return self.__fitness


	def getGeneration(self):
		return self.__generation


	def getLenAlignment(self):
		return len(self.__chromosome)


	def getOffspring(self):
		return self.__expectOffspring

	
	def toString(self):
		chromosome = ""
		for row in self.__chromosome:
			chromosome += row+"\n"
		return "[%d] score: %d offspring: %f\nchromosome:\n%s" % (self.__generation, self.__fitness,
		self.__expectOffspring, chromosome)