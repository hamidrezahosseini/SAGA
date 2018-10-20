#!/usr/bin/env python3
# -*- coding: utf-8 -*

from NeighborJoining import NeighborJoining
from Saga import Saga
from Files import Files

if __name__ == '__main__':
    '''
    aligment = [
        "XTQNPQWLWQEVLQEQQLSRPTYETTT",
        "MTQNPQWLWQEVLTKLRPTYET",
        #"MTQNPQWLLSRPTYET",
        "MTQNPQWLWQEVLTKLERPTYET",
        "MTQNPQWLWQEVLTKLEQQLSRPTYET",
        "MTQNPQWLWQEVLTKLEQQSRPTYET",
        "MTQNPQWLWQQLSRPTYET",
        "CTQNPQWLWQEVLQEQQLSRPTYETTT"
    ]
    '''

    files = Files()
    files.open("input.fasta")
    nj = NeighborJoining(files.getLabels(), files.getSequencias())
    #nj.execute()
    #print(files.getSequencias())
    #print(files.getLabels())

    saga = Saga(population_size=20, num_generations=100)
    print("Parameters:")
    print("Polulation size = 20")
    print("um generations = 100")
    print(files.getSequencias())
    print()
    saga.execute(files.getSequencias())
    print("Fim execução!!")
