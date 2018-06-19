from random import randint
from random import sample
from Individual import Individual


"""
Classe de operadores do saga
"""
class Operator():
    """
    Construtor da classe operador, armazena os operadores em um dicionario, a fim de serem selecionados
    aleatoriamente pelos seus indices.
    """
    def __init__(self):
        self.function_dict = {
            1: self.crossover_one_point, # 2 parents
            2: self.crossover_uniform, # 2 parents
            3: self.block_shuffling_left, # 1 parents
            4: self.block_shuffling_vertically, # 1 parents
        }
        self.selected_op = 0 # guarda a key do operador selecionado


    """
    Seleciona de por meio da roleta um operador e retorna o numero de pais a serem selecionados
    """
    def select_operator(self):
        dict_len = len(self.function_dict)

        # seleciona o operador aleatoriamente
        self.selected_op = randint(1,dict_len)

        # Verifica se o operator escolhido necessita de 1 parent
        if self.selected_op == 3 or self.selected_op == 4:
            return 1
        else:
            return 2


    """
    Executa o operador selecionado, retornando os filhos gerados pelo operador
    """
    def run_operator(self, parent1, parent2 = None):
        if parent2 is not None:
            self.function_dict[self.selected_op](parent1, parent2)
        else:
            self.function_dict[self.selected_op](parent1)


    """
    Operador de crossover de um ponto, retorna os filhos do crossover
    """
    def crossover_one_point(self, individual1, individual2):
        # print("Individual1 = %s" % individual1.toString())
        # print("Individual2 = %s\n" % individual2.toString())
        chromosome1 = individual1.getChromosome()
        chromosome2 = individual2.getChromosome()
        
        num_seq = len(chromosome1)
        point = randint(1, len(chromosome1[0])-1) # ponto de corte

        # primeiro cromossomo
        part1_a = []
        part1_b = []

        # segundo cromossomo
        part2_a = []
        part2_b = []

        # divide o primeiro cromossomo
        for row in chromosome1:
            part1_a.append(row[0:point])
            part1_b.append(row[point::])

        num_char_a = []
        for row in part1_a:
            num_char_a.append(len(row) - row.count('*'))

        # Divide o segundo cromossomo
        for i, row in enumerate(chromosome2):
            cont = 0
            # print("num_char_a[i] = %d\nrow %s\n" % (num_char_a[i], row))
            for j, char in enumerate(row):
                if char != '*':
                    cont += 1
                if not num_char_a[i]:
                    part2_a.append('')
                    part2_b.append(row)
                elif cont == num_char_a[i]:
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

        # Ajusta o tamanho da segunda sequencia lado A
        for i in range(0,  len(part2_a)):
            while len(part2_a[i]) < size_seq_A:
                part2_a[i] = part2_a[i] + '*'

        # Ajusta o tamanho da segunda sequencia lado B
        for i in range(0, len(part2_b)):
            while len(part2_b[i]) < size_seq_B:
                part2_b[i] = '*' + part2_b[i]

        # filhos a serem gerados
        child1 = []
        child2 = []

        # realiza a juncao dos cromossomos
        # print("part1_a %s\npart1_b %s" % (part1_a, part1_b))
        # print("part2_a %s\npart2_b %s\n" % (part2_a, part2_b))
        for i in range(0, num_seq):
            child1.append(part1_a[i]+part2_b[i])
            child2.append(part2_a[i]+part1_b[i])

        # atribui os novos cromossomos aos individuos
        individual1.setChromosome(child1)
        individual2.setChromosome(child2)

    """
    Operador de crossover uniforme, realiza o crossover uniforme entre dois cromossomos
    """
    def crossover_uniform(self, individual1, individual2):
        # print("---------------OPERADOR CROSSOVER UNIFORME---------------")
        chromosome1 = individual1.getChromosome()
        chromosome2 = individual2.getChromosome()
        position = []

        num_seq1 = len(chromosome1)
        # num_seq2 = len(chromosome2) (não esta sendo usada)

        # cromossomo dos filhos
        child1_chromosome = []
        child2_chromosome = []

        for x in range(0, num_seq1):
            tam_min = min(len(chromosome1[x]), len(chromosome2[x]))
            chrom1_size = len(chromosome1[x])
            chrom2_size = len(chromosome2[x])

            sequencia_chromosome1 = chromosome1[x]
            sequencia_chromosome2 = chromosome2[x]
            
            for y in range(0, tam_min):
                if sequencia_chromosome1[y] == sequencia_chromosome2[y]: #Condição para o mapeamento
                    position.append(y) # Armazenar as posições que corresponde tanto ao pai1 como ao pai2
            # print("PAI 1: %s" % sequencia_chromosome1)
            # print("PAI 2: %s" % sequencia_chromosome2)
            # print('MAPEAMENTO: %s' % position)
            x = sample(position,  2) #escolhe aleatório dois
            # print ("ESCOLHIDOS: %s" % x)
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
                    child1_part1.append(sequencia_chromosome1[y])
                if y == menor_posicao:
                    child1_part2.append(sequencia_chromosome1[y])
                if y > menor_posicao and y < maior_posicao:
                    child1_part3.append(sequencia_chromosome1[y])
                if y == maior_posicao:
                    child1_part4.append(sequencia_chromosome1[y])
                if y > maior_posicao:
                    child1_part5.append(sequencia_chromosome1[y])
            
            for y in range(0, chrom2_size):
                if y < menor_posicao:
                    child2_part1.append(sequencia_chromosome2[y])
                if y == menor_posicao:
                    child2_part2.append(sequencia_chromosome2[y])
                if y > menor_posicao and y < maior_posicao:
                    child2_part3.append(sequencia_chromosome2[y])
                if y == maior_posicao:
                    child2_part4.append(sequencia_chromosome2[y])
                if y > maior_posicao:
                    child2_part5.append(sequencia_chromosome2[y])
            
            child1 = child1_part1+child1_part2+child2_part3+child1_part4+child1_part5
            child2 = child2_part1+child2_part2+child1_part3+child2_part4+child2_part5

            for y in range(0, len(child1)):
                if y == 0:
                    teste = child1[y]
                else:
                    teste += child1[y]
            # print("CHILD 1: %s" % teste)
            child1_chromosome.append(teste)

            for y in range(0, len(child2)):
                if y == 0:
                    teste = child2[y]
                else:
                    teste += child2[y]
            # print("CHILD 2: %s" % teste)
            # print("\n")
            child2_chromosome.append(teste)

        individual1.setChromosome(child1_chromosome)
        individual2.setChromosome(child2_chromosome)


    """
    Implementação do operador block shuffling 1
    """
    def block_shuffling_left(self, individual1):
        # Para o operador block shuffling mover um bloco cheio de lacunas uma posição para esquerda
        # print("-----------MOVER BLOCO DE LACUNAS PARA UMA POSIÇÃO NA ESQUERDA-----------")
        sequence = individual1.getChromosome()
        amount_sequence = len(sequence)
        child_chromosome = []
        for x in range(0, amount_sequence):
            size_sequence = len(sequence[x])            
            child = []
            # var = ""
            # contador = 0
            for y in range(0, size_sequence): # Para identificar os gap e os mover
                if sequence[x][y] == "*":
                    if y != 0:
                        temp = child[len(child)-1] 
                        child.pop()
                        child.append(sequence[x][y])
                        child.append(temp)
                    else:
                        # contador = 1
                        var = sequence[x][size_sequence-1]
                        child.append(sequence[x][y])
                else:
                    child.append(sequence[x][y])
            for y in range(0, len(child)):
                if y == 0:
                    child_new = child[y]
                else:
                    child_new += child[y]

            child_chromosome.append(child_new)
            # print("PAI: %s" % sequence[x])
            # print("FILHO: %s" % child_new)
            # print("\n")

        individual1.setChromosome(child_chromosome)


    """
    Implementação do operador block shuffling 2
    """
    def block_shuffling_vertically(self, individual1):
        # Para o operador block shuffling para dividir a metade um bloco de gaps e mover para esquerda
        # print("-----------VERTICAL GAPS-----------")
        sequence = individual1.getChromosome()
        amount_sequence = len(sequence)
        contador1 = 0
        contador2 = 0
        child_chromosome = []
        for x in range(0, amount_sequence):
            
            size_sequence = len(sequence[x])
            child = []
            position = []
            for y in range(0, size_sequence):
                if sequence[x][y] == "*":
                    position.append(y)
                    contador1 += 1
                    contador2 = 0
                else:
                    contador2 = 1
                if contador1 > 1 and contador2 == 1:
                    contador1 = 0
                    contador2 = 0
                    break
                    
            if len(position) % 2 == 0:
                teste = len(position) / 2
            else:
                teste = len(position) / 2
            child = []
            temp = ""
            for y in range(0, size_sequence):
                if position == []:
                    child.append(sequence[x][y])
                else:
                    recebe = int(position[0]) + teste
                    # print("CHILD: %s" % child)
                    if y == position[0]:
                        if child != []:
                            temp = child[len(child)-1]
                            child.pop()
                        
                    if y == recebe:
                        child.append(temp)
                        child.append(sequence[x][y])
                    else:
                        child.append(sequence[x][y])
            
            for y in range(0, len(child)):
                if y == 0:
                    child_new = child[y]
                else:
                    child_new += child[y]  
            del child
            print("PAI:\t%s" % sequence[x]) 
            print("FILHO:\t%s" % child_new) 
            print("\n")
            child_chromosome.append(child_new)

        individual1.setChromosome(child_chromosome)