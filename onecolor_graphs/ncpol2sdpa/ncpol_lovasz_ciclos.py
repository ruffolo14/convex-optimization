'''
Este programa calcula o numero de lovasz
para qualquer ciclo e obtem os projetores
de medicao
'''

import numpy as np
from ncpol2sdpa import *
import re 


def get_monomial_indexes(dic):
    # dic e o dicionario de indices das variaveis da SDP sdp.monomial_index 

    #Dicionario de indices dos string(monomios)
    monomials_indexes = ({str(key):value for key,value in dic.items() if value < sdp.block_struct[0]})

    indices = {}    #Dicionario        
    for vertex in range(n_vertices):
        indices['A'+str(vertex)] = [vertex+1] #Isso e uma lista para cada key de indices. 'A'+'B' concatena strings
        for key in monomials_indexes.keys():
            padrao_encontrado = re.match(str(A[vertex])+r'(.+)', key,flags=0) #compara as keys com 'A[vertex]'+'qualquer string' 
            if padrao_encontrado and monomials_indexes[padrao_encontrado.group()] > n_vertices:  #re.match retorna type True se deu match
                indices['A'+str(vertex)].append( monomials_indexes[padrao_encontrado.group()]) 

    return indices
#----------------------------------------Resolvendo a SDP-----------------------------------
level = 2  # lvl da hierarquia NPA
n_vertices = 7 # numero de vertices do grafo associado ao cenario 
## edges
edges = []
for vertex in range(n_vertices):
    next_vertex = (vertex+1) % n_vertices
    edges.append([vertex,next_vertex])

## projetores nao comutativos
A = generate_operators('A', n_vertices, hermitian = True)
## restricoes ou substituicoes
substitutions = {} 
substitutions.update({A[vertex]**2:A[vertex] for vertex in range(n_vertices)})
for i in range(n_vertices):
    for j in range(n_vertices):
        if [i,j] in edges: 
            substitutions.update({A[i]*A[j]:0})
            substitutions.update({A[j]*A[i]:0})

## funcao objetiva
objective_function = -sum([A[i] for i in range(n_vertices)])
## relaxacao
sdp = SdpRelaxation(A, verbose = 1)
sdp.get_relaxation(level, objective = objective_function, substitutions = substitutions)
sdp.solve('mosek')
print('O numero de Lovasz:',-sdp.primal,'\n')
print('seu valor dual:',-sdp.dual,'\n')
print('status do problema:', sdp.status)

#-------------------------------Extracao dos projetores de medicao-----------------------
## indices dos monomios
variables_indexes = sdp.monomial_index
indices = get_monomial_indexes(variables_indexes)
## vetores de Gram da matriz de momentos
moment_matrix = sdp.x_mat[0]
from functions import decompose_gram_vectors
Gram = decompose_gram_vectors(moment_matrix)
## dicionario com monomio:vetores
dic_monomials_vectors = {}
for vertex in range(n_vertices):
    dic_monomials_vectors['A'+str(vertex)] =[]
    for linha in indices['A'+str(vertex)]:
        dic_monomials_vectors['A'+str(vertex)].append(Gram[linha]) 


## construindo os projetores como matrizes e alocando em uma lista
A = []
from functions import get_orthogonal_span
for key in dic_monomials_vectors.keys():
    A.append(get_orthogonal_span(dic_monomials_vectors[key]))

print(A)



