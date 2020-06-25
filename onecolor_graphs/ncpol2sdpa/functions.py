import numpy as np
'''
Esta funcao determina os vetores de Gram associados
a uma matriz positiva-semidefinida
'''

def decompose_gram_vectors(matrix):
    val, vec = np.linalg.eigh(matrix)
    ## zero autovalores proximos de zero
    val[abs(val)<5e-1] = 0
    ## apago os autovetores associados a autovalores nulos e os autovalores nulos
    vec = np.delete(vec, np.where(val == 0), axis = 1)
    val = np.delete(val, np.where(val == 0))
    diag_root = np.diag(np.sqrt(val))
    Cholesky = vec@diag_root
    ## os vetores de Gram sao as linhas da matriz Cholesky
    Gram = []
    for vector in range(Cholesky.shape[0]):
        Gram.append(Cholesky[vector])

    return Gram

'''
Essa função obtem o projetor associado a um subspaço gerado por uma lista de vetores
'''
def get_orthogonal_span(list_vectors):
    # list_vectors e uma lista de arrays
    matrix = 0
    for vector in list_vectors:
        normal_vector = vector / np.linalg.norm(vector)
        normal_vector = np.reshape(normal_vector, (normal_vector.shape[0],1))
        vector_transpose = normal_vector.transpose()
        projector = np.outer(normal_vector,vector_transpose)
        matrix = matrix + projector

    ## construindo projetor associado ao maior autovalor
    val, vec = np.linalg.eigh(matrix)
    val[abs(val)<5e-1] = 0
    vec = np.delete(vec, np.where(val == 0), axis = 1)
    projector = vec@vec.transpose()
        
    return projector