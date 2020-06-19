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


'''
A função a seguir recebe uma matrix nxn de rank r e a projeta em um espaço de dimensão r
resultando em uma matrix rxr
'''
def project_eff_dim(matrix):
    # matrix é a matriz de entrada, nxn
    # dim é a dimensão n da matriz de entrada nxn
    # rank é o rank de matrix
    dim = matrix.shape[0]
    rank = np.linalg.matrix_rank(matrix)
    v = np.identity(dim)
    w = np.identity(rank)
    projector = sum([np.outer(w[i],v[i]) for i in range(rank)])
    new_matrix = projector@matrix@projector.transpose()

    return new_matrix