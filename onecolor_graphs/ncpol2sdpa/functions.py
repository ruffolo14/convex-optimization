'''
Funcao que normaliza vetores
'''
import numpy as np

'''
Esta funcao determina os vetores de Gram associados
a uma matriz positiva-semidefinida
'''

def decompose_gram_vectors(matrix):
    from scipy.linalg import cholesky
    # matriz de Cholesky
    Cholesky = cholesky(matrix,lower=True)
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
    column_list = []
    for vector in list_vectors:
        new_vector = np.reshape(vector, (-1,1))
        column_list.append(new_vector)

    matrix = np.hstack(column_list)
    from scipy.linalg import qr
    orthogonal_matrix, triangular = qr(matrix)
    orthogonal = []
    for column in range(len(list_vectors)):
        orthogonal.append(orthogonal_matrix[:,column])
    return orthogonal