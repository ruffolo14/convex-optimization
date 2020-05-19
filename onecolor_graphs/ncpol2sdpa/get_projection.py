def get_projection(vector_1,vector_2):
    # funcao retorna projecao de vector_2 em vector_1
    # dimensao dos vetores deve ser iguais
    dimension = len(vector_1)
    norm_squared_vector_2 = sum([vector_2[index]*vector_2[index] for index in range(dimension)]) 
    alpha = sum([vector_1[index]*vector_2[index] for index in range(dimension)])
    alpha = alpha/norm_squared_vector_2
    return alpha*vector_2

