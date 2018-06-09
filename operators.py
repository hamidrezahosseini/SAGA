from random import randint
from Individual import Individual


"""
Operador de crossover de um ponto, retorna os filhos do crossover
"""
def crossover_one_point(parent1, parent2):

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

    crossover_one_point(indiv1, indiv2)

    print()
    print("indiv1 = %s" % indiv1.getChromossome())
    print("indiv2 = %s" % indiv2.getChromossome())
