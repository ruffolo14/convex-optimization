'''
Funcao que normaliza vetores
'''
import numpy as np

def normalize(vector):
    vector_length = len(vector) 
    norm_squared = sum([vector[index]*vector[index] for index in range(vector_length)])

    norm = np.sqrt(norm_squared)
    normalized_vector = vector/norm
    return normalized_vector

def get_projection(vector_1,vector_2):
    # funcao retorna projecao de vector_2 em vector_1
    # dimensao dos vetores deve ser iguais
    dimension = len(vector_1)
    norm_squared_vector_2 = sum([vector_2[index]*vector_2[index] for index in range(dimension)]) 
    alpha = sum([vector_1[index]*vector_2[index] for index in range(dimension)])
    alpha = alpha/norm_squared_vector_2
    return alpha*vector_2


'''
Esta funcao determina os vetores de Gram associados
a uma matriz positiva-semidefinida
'''

def decompose_gram_vectors(matrix):
    # decomposicao espectral
    eigvalues, eigvectors = np.linalg.eig(matrix)
    # matriz diagonal das raizes dos autovalores
    Diagonal = np.diag(np.sqrt(eigvalues))
    # matriz de Cholesky
    Cholesky = eigvectors.dot(Diagonal) 
    #Os vetores de Gram sao as linhas de Cholesky
    n_vectors = Cholesky.shape[0]
    Gram = []
    for vector in range(n_vectors):
        Gram.append(Cholesky[vector])

    return Gram

'''
Este programa realiza a ortogonalizacao de Gram-Schmidt para
uma lista de arrays
'''

def get_orthogonal_span(list_vectors):
    # list_vectors e uma lista de arrays
    vector_0 = normalize(list_vectors[0])
    orthogonal = [vector_0]
    for index in range(len(list_vectors)):
        vector = list_vectors[index]
        for j in range(1,index):
            vector_projection = get_projection(orthogonal[j], vector)
            vector = vector - vector_projection

        vector = normalize(vector)
        orthogonal.append(vector)

    return orthogonal