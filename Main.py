#!/usr/bin/env python3
# -*- coding: utf-8 -*

from Saga import Saga

if __name__ == '__main__':
    aligment = [
        "XTQNPQWLWQEVLQEQQLSRPTYETTT",
        "MTQNPQWLWQEVLTKLRPTYET",
        "MTQNPQWLLSRPTYET",
        "MTQNPQWLWQEVLTKLERPTYET",
        "MTQNPQWLWQEVLTKLEQQLSRPTYET",
        "MTQNPQWLWQEVLTKLEQQSRPTYET",
        "MTQNPQWLWQQLSRPTYET",
        "CTQNPQWLWQEVLQEQQLSRPTYETTT"
    ]

    saga = Saga(population_size=10, num_generations=20)
    print("Parameters:")
    print("Polulation size = 10")
    print("um generations = 20")
    print(aligment)
    print()
    saga.execute(aligment)
    print("Fim execução!!")
   