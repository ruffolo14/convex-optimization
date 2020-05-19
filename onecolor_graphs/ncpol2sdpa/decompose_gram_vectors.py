'''
Esta funcao determina os vetores de Gram associados
a uma matriz positiva-semidefinida
'''

import numpy as np

def decompose_gram_vectors(matrix, precision, trashold):
    # decomposicao espectral
    eigvalues, eigvectors = np.linalg.eig(matrix)
    # matriz diagonal das raizes dos autovalores
    Diagonal = np.diag(np.sqrt(eigvalues))
    # matriz de Cholesky
    Cholesky = eigvectors.dot(Diagonal)
    # definindo precisao
    Cholesky = np.around(Cholesky, decimals= precision)
    # descartando entradas menores que trashold
    Cholesky[abs(Cholesky) < trashold]=0
    #Apaga colunas de zeros
    Cholesky= np.delete(Cholesky,np.where(~Cholesky.any(axis=0))[0], axis=1) 

    #Os vetores de Gram sao as linhas de Cholesky
    n_vectors = Cholesky.shape[0]
    Gram = []
    for vector in range(n_vectors):
        Gram.append(Cholesky[vector])

    return Gram

