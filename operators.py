from random import randint
from random import sample
from Individual import Individual


"""
Classe de operadores do saga
"""
class Operator():
    
    def __init__(self):
        pass


    """
    Seleciona de por meio da roleta um operador e retorna o numero de pais a serem selecionados
    """
    def select_operator(self):
        pass


    """
    Operador de crossover de um ponto, retorna os filhos do crossover
    """
    def crossover_one_point(self, individual1, individual2):
        chromossome1 = individual1.getChromossome()
        chromossome2 = individual2.getChromossome()
        
        num_seq = len(chromossome1)
        point = randint(1, len(chromossome1[0])-1) # ponto de corte

        # primeiro cromossomo
        part1_a = []
        part1_b = []

        # segundo cromossomo
        part2_a = []
        part2_b = []

        # divide a primeira matriz
        for row in chromossome1:
            part1_a.append(row[0:point])
            part1_b.append(row[point::])

        num_char_a = []
        for row in part1_a:
            num_char_a.append(len(row) - row.count('*'))

        # Divide o segundo cromossomo
        for i, row in enumerate(chromossome2):
            cont = 0
            for j, char in enumerate(row):
                if char != '*':
                    cont += 1
                if cont == num_char_a[i]:
                    part2_a.append(row[0:j+1])
                    part2_b.append(row[j+1::])
                    break
        
        # Encontra o tamnho da segunda sequencia lado A
        size_seq_A = 0
        for i in part2_a:
            size_seq_A = max(size_seq_A, len(i))

        # Encontra o tamnho da segunda sequencia lado B
        size_seq_B = 0
        for i in part2_b:
            size_seq_B = max(size_seq_B, len(i))

        # Ajusta o tamanho da primeira sequencia
        for i in range(0,  len(part2_a)):
            while len(part2_a[i]) < size_seq_A:
                part2_a[i] = part2_a[i] + '*'

        # Ajusta o tamanho da primeira sequencia
        for i in range(0, len(part2_b)):
            while len(part2_b[i]) < size_seq_B:
                part2_b[i] = '*' + part2_b[i]

        # filhos a serem gerados
        child1 = []
        child2 = []

        # realiza a juncao dos cromossomos
        for i in range(0, num_seq):
            child1.append(part1_a[i]+part2_b[i])
            child2.append(part2_a[i]+part1_b[i])

        # atribui os novos cromossomos aos individuos
        individual1.setChromossome(child1)
        individual2.setChromossome(child2)

    """
    Operador de crossover uniforme, realiza o crossover uniforme entre dois cromossomos
    """
    def crossover_uniforme(self, individual1, individual2):
        print("\n")
        print("---------------OPERADOR CROSSOVER UNIFORME---------------")
        chromossome1 = individual1.getChromossome()
        chromossome2 = individual2.getChromossome()
        position = []

        num_seq1 = len(chromossome1)
        # num_seq2 = len(chromossome2) (não esta sendo usada)

        # cromossomo dos filhos
        child1_chromossome = []
        child2_chromossome = []

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
            child1_chromossome.append(teste)

            for y in range(0, len(child2)):
                if y == 0:
                    teste = child2[y]
                else:
                    teste += child2[y]
            print("CHILD 2: %s" % teste)
            print("\n")
            child2_chromossome.append(teste)

        individual1.setChromossome(child1_chromossome)
        individual2.setChromossome(child2_chromossome)


    """
    Implementação do operador block shuffling 1
    """
    def block_shuffling_left(self, individual1):
        # Para o operador block shuffling mover um bloco cheio de lacunas uma posição para esquerda
        print("-----------MOVER BLOCO DE LACUNAS PARA UMA POSIÇÃO NA ESQUERDA-----------")
        sequence = individual1.getChromossome()
        amount_sequence = len(sequence)
        child_chromossome = []
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

            child_chromossome.append(child_new)
            print("PAI: %s" % sequence[x])
            print("FILHO: %s" % child_new)
            print("\n")

        individual1.setChromossome(child_chromossome)

"""
Implementação do operador block shuffling 2
"""
def block_shuffling_vertically(sequencia):
    # Para o operador block shuffling para dividir a metade um bloco de gaps e mover para esquerda
    print("-----------VERTICAL GAPS-----------")
#
# -----------------------------------------------------------------------
#       

if __name__ == '__main__':
    operator = Operator()
    
    chromossome1 = [
        "WGKVN***VDEVGGEAL*",
        "WDKVNEEE***VGGEAL*",
        "WGKVG**AHAGEYGAEAL",
        "WSKVGGHA**GEYGAEAL"
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

    #operator.crossover_one_point(indiv1, indiv2)
    operator.crossover_uniforme(indiv1, indiv2)
    #operator.block_shuffling_left(indiv1)

    
    print()
    print("indiv1 = %s" % indiv1.getChromossome())
    print("indiv2 = %s" % indiv2.getChromossome())
    
