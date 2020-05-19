'''
Funcao que normaliza vetores
'''
from math import sqrt

def normalize(vector):
    vector_length = len(vector) 
    norm_squared = sum([vector[index]*vector[index] for index in range(vector_length)])

    norm = sqrt(norm_squared)
    normalized_vector = vector/norm
    return normalized_vector