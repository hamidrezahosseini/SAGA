#!/usr/bin/env python3
# -*- coding: utf-8 -*
# from random import randint
from random import *
from Individual import Individual


"""
Operador de crossover de um ponto, retorna os filhos do crossover
"""
def crossover_one_point(parent1, parent2):
    print("-----------OPERADOR CROSSOVER 1 PONTO-----------")
    chromossome1 = parent1.getChromossome()
    chromossome2 = parent2.getChromossome()
    
    num_seq = len(chromossome1)
    # point = randint(1, len(chromossome1[0])-1) # ponto de corte
    point = 4
    # print("ponto = %d" % point)

    part1_a = []
    part1_b = []
    part2_a = []
    part2_b = []
    # divide a primeira matriz
    for i in range(0, num_seq):
        temp = chromossome1[i]
        part1_a.append(temp[0:point])
        part1_b.append(temp[point::])

    for row in part1_a:
        print("part1_a = %s" % row)
    print()
    for row in part1_b:
        print("part1_b = %s" % row)

    num_a = []
    num_b = [] 
    #numero de caracteres  (exceto os gaps)
    for row in chromossome1:
        
        num_char_a = 0
        num_char_b = 0
        for j in range(0, len(row)):
            if row[j] != '*':
                if j < point:
                    num_char_a += 1
                else:
                    num_char_b += 1
        # print("numchar1[%d] = %d\nnumchar2[%d] = %d" % (i, num_char_a, i, num_char_b))
        num_a.append(num_char_a)
        num_b.append(num_char_b)
    
    j = 0
    for row in chromossome2: # Divide o segundo cromossomo
        cont = 0
        for i in range(0, len(row)):
            if row[i] != '*':
                cont += 1

            if cont == num_a[j]: # posicao de corte
                i +=1
                part2_a.append(row[0:i])
                part2_b.append(row[i::])
                # print("num_a = %d\nappend1[0:i] = %s\nappend2[i::] = %s\n" % (num_a[j], row[0:i], row[i::]))
                break
    
    # Tamanho de ajusta da sequencia
    max_seqA = 0
    max_seqB = 0
    for i in range(0, num_seq):
        max_seqA = max(max_seqA, len(part2_a[i]))
        max_seqB = max(max_seqB, len(part2_b[i]))

    print("\nseqA = %d\nseqB = %d" % (max_seqA, max_seqB))
    print()
    for i in range(0,  len(part2_a)):
        while len(part2_a[i]) < max_seqA:
            part2_a[i] = part2_a[i] + '*'

    for i in range(0, len(part2_b)):
        while len(part2_b[i]) < max_seqB:
            part2_b[i] = '*' + part2_b[i]

    print("part2_a = %s" % part2_a)    
    print("part2_b = %s" % part2_b)

    child1 = []
    child2 = []
    for i in range(0, len(part1_a)):
        child1.append(part1_a[i]+part2_b[i])
        child2.append(part2_a[i]+part1_b[i])

    print()
    for row in child1:
        print("child1 = %s" % row)
    print()
    for row in child2:
        print("child2 = %s" % row)
    

"""
Implementação do operador crossover uniforme
"""
def crossover_uniforme(sequencia1, sequencia2):
    print("\n")
    print("---------------OPERADOR CROSSOVER UNIFORME---------------")
    chromossome1 = sequencia1.getChromossome()
    chromossome2 = sequencia2.getChromossome()
    position = []

    num_seq1 = len(chromossome1)
    num_seq2 = len(chromossome2)

    for x in range(0, num_seq1):
        tam_min = min(len(chromossome1[x]), len(chromossome2[x]))
        chrom1_size = len(chromossome1[x])
        chrom2_size = len(chromossome2[x])

        sequencia_chromossome1 = chromossome1[x]
        sequencia_chromossome2 = chromossome2[x]
        
        for y in range(0, tam_min):
            if sequencia_chromossome1[y] == sequencia_chromossome2[y]: #Condição para o mapeamento
                position.append(y) # Armazenar as posições que corresponde tanto ao pai1 como ao pai2
        print("PAI 1: %s" % sequencia_chromossome1)
        print("PAI 2: %s" % sequencia_chromossome2)
        print('MAPEAMENTO: %s' % position)
        x = sample(position,  2) 
        print ("ESCOLHIDOS: %s" % x)
        del position[:]
        child1_part1 = []
        child1_part2 = []
        child1_part3 = []
        child1_part4 = []
        child1_part5 = []
        
        child2_part1 = []
        child2_part2 = []
        child2_part3 = []
        child2_part4 = []
        child2_part5 = []

        menor_posicao = min(x[0], x[1])
        maior_posicao = max(x[0], x[1])

        # Para fazer a permutação dos pontos
        for y in range(0, chrom1_size):
            if y < menor_posicao:
                child1_part1.append(sequencia_chromossome1[y])
            if y == menor_posicao:
                child1_part2.append(sequencia_chromossome1[y])
            if y > menor_posicao and y < maior_posicao:
                child1_part3.append(sequencia_chromossome1[y])
            if y == maior_posicao:
                child1_part4.append(sequencia_chromossome1[y])
            if y > maior_posicao:
                child1_part5.append(sequencia_chromossome1[y])
        
        for y in range(0, chrom2_size):
            if y < menor_posicao:
                child2_part1.append(sequencia_chromossome2[y])
            if y == menor_posicao:
                child2_part2.append(sequencia_chromossome2[y])
            if y > menor_posicao and y < maior_posicao:
                child2_part3.append(sequencia_chromossome2[y])
            if y == maior_posicao:
                child2_part4.append(sequencia_chromossome2[y])
            if y > maior_posicao:
                child2_part5.append(sequencia_chromossome2[y])
        
        child1 = child1_part1+child1_part2+child2_part3+child1_part4+child1_part5
        child2 = child2_part1+child2_part2+child1_part3+child2_part4+child2_part5

        for y in range(0, len(child1)):
            if y == 0:
                teste = child1[y]
            else:
                teste += child1[y]
        print("CHILD 1: %s" % teste)

        for y in range(0, len(child2)):
            if y == 0:
                teste = child2[y]
            else:
                teste += child2[y]
        print("CHILD 2: %s" % teste)
        print("\n")


"""
Implememtação do operador block shuffling 1
"""
def block_shuffling_left(sequencia):
    # Para o operador block shuffling mover um bloco cheio de lacunas uma posição para esquerda
    print("-----------MOVER BLOCO DE LACUNAS PARA UMA POSIÇÃO NA ESQUERDA-----------")
    sequence = sequencia.getChromossome()
    amount_sequence = len(sequence)
    for x in range(0, amount_sequence):
        size_sequence = len(sequence[x])
        
        child = []
        for y in range(0, size_sequence): # Para identificar os gap e os mover
            if sequence[x][y] == "*":
                temp = child[len(child)-1]
                child.pop()
                child.append(sequence[x][y])
                child.append(temp)
            else:
                child.append(sequence[x][y])         

        for y in range(0, len(child)):
            if y == 0:
                child_new = child[y]
            else:
                child_new += child[y]
        print("PAI: %s" % sequence[x])
        print("FILHO: %s" % child_new)
        print("\n")

if __name__ == '__main__':
    
    chromossome1 = [
		"MGKVN***VDEVGGEAL*",
		"MDKVNEEE***VGGEAL*",
		"MGKVG**AHAGEYGAEAL",
		"MSKVGGHA**GEYGAEAL"
	]

    chromossome2 = [
        "**WGKVNVDEVG*GEAL",
        "WD**KVNEEEVG*GEAL",
        "WGKVGA*HAGEYGAEAL",
        "WSKVGGHAGEY*GAEAL"
    ]

    indiv1 = Individual()
    indiv1.setChromossome(chromossome1)

    indiv2 = Individual()
    indiv2.setChromossome(chromossome2)
    # operadores 
    crossover_one_point(indiv1, indiv2)
    crossover_uniforme(indiv1, indiv2);
    block_shuffling_left(indiv1)

    print()
    print("indiv1 = %s" % indiv1.getChromossome())
    print("indiv2 = %s" % indiv2.getChromossome())
