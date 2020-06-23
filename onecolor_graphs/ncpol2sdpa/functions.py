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
Essa função obtém o projetor associado a um subspaço gerado por uma lista de vetores
'''
def get_orthogonal_span(list_vectors):
    # list_vectors e uma lista de arrays
    matrix = 0
    for vector in list_vectors:
        normal_vector = vector / np.linalg.norm(vector)
        projector = np.outer(normal_vector,normal_vector)
        matrix = matrix + projector

    eigenvalue, eigenvector = np.linalg.eigh(matrix)
    ## descartando autovalores proximos de zero
    mask = np.isclose(eigenvalue,np.zeros(eigenvalue.shape),atol = 1e-1)
    eigenvalue = np.delete(eigenvalue, np.where(mask))

    matrix = sum([eigenvalue[i]*np.outer(eigenvector[i],eigenvector[i])/(np.linalg.norm(eigenvector[i])**2) for i in range(eigenvalue.shape[0])])

    return matrix