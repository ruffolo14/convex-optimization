'''
Este programa realiza a ortogonalizacao de Gram-Schmidt para
uma lista de arrays
'''
from get_projection import get_projection
from normalize import normalize

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