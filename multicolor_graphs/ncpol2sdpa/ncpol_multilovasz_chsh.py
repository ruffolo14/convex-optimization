'''
Este programa implementa o algoritmo NPA
utilizando a biblioteca NCPOL2SDPA 
para calcular o numero de Lovasz de
multigrafos coloridos (duas cores)

Em seguida, obtemos os operadores de medicao de cada parte
'''

import numpy as np
from ncpol2sdpa import *
import re

def get_monomials_index_A(dic):
    #dic e o dicionario de indices das variaveis

    monomials_indexes = ({str(key):value for key,value in dic.items() if value < sdp.block_struct[0]})
    indices = {}
    for vertex in range(n_vertices):
        indices['A'+str(vertex)] = [vertex+1]
        for key in monomials_indexes.keys():
            match_pattern = re.match(str(A[vertex])+r'(.+)', key, flags=0)
            if match_pattern and monomials_indexes[match_pattern.group()] > n_vertices:
                indices['A'+str(vertex)].append(monomials_indexes[match_pattern.group()])
    
    return indices

def get_monomials_index_B(dic):
    #dic e o dicionario de indices das variaveis

    monomials_indexes = ({str(key):value for key,value in dic.items() if value < sdp.block_struct[0]})
    indices = {}
    for vertex in range(n_vertices):
        indices['B'+str(vertex)] = [vertex+n_vertices+1]
        for key in monomials_indexes.keys():
            match_pattern = re.match(str(B[vertex])+r'(.+)', key, flags=0)
            if match_pattern and monomials_indexes[match_pattern.group()] > n_vertices:
                indices['B'+str(vertex)].append(monomials_indexes[match_pattern.group()])

    return indices
#------------------------------Resolvendo a SDP------------------------------------
level = 2
n_vertices = 8

#Definindo os vertices que fazem parte de cada subgrafo (A e B)
A_edges = []   #Lista de vertices da Alice
B_edges = []   #Lista de vertices do Bob
for i in range(4):
    A_edges.append((2*i,2*i+1))
    A_edges.append((i,i+4))
    B_edges.append((2*i+1,(2*i+2)%8)) #(2*i+2)%8 considera os vertices modulo 8
    B_edges.append((i,i+4))

#Definindo as matrizes de adjascencia
'''
As matrizes de adjascencia possuem M_uv = 1 se u e v sao vertices adjascentes no grafo
associado e 0 se nao sao adjascentes
Serao utilizadas para indexar as constraints no proximo passo
'''
adj_A = np.zeros((n_vertices,n_vertices))
adj_B = np.zeros((n_vertices,n_vertices))

for i in range(n_vertices):
    for j in range(n_vertices):
        if (i,j) in A_edges:
            adj_A[i,j] = 1

        if (i,j) in B_edges:
            adj_B[i,j] = 1


#Definindo as variaveis da SDP
A = generate_operators('A', n_vars=n_vertices, hermitian=True)
B = generate_operators('B', n_vars=n_vertices, hermitian=True)

#Restricoes e simetrias da SDP
constraints = {} #Dicionario
constraints.update({A[_]**2:A[_] for _ in range(n_vertices)}) #Todas as variaveis sao projetores
constraints.update({B[_]**2:B[_] for _ in range(n_vertices)})

#A e B sao atribuicoes ortogonais de G_A e G_B complementares

for i in range(n_vertices):
    for j in range(n_vertices):
        constraints.update({A[i]*B[j]:B[j]*A[i]}) #Os projetores A e B comutam
        if adj_A[i,j] == 1:
            constraints.update({A[i]*A[j]:0})
            constraints.update({A[j]*A[i]:0})  

        if adj_B[i,j] == 1:
            constraints.update({B[i]*B[j]:0})
            constraints.update({B[j]*B[i]:0})
            

#Funcao objetiva
obj = - sum([A[_]*B[_] for _ in range(n_vertices)])

#Relaxacao da SDP por NCPOL2SDPA
sdp = SdpRelaxation(A+B, verbose = 0)
sdp.get_relaxation(level, objective=obj, substitutions = constraints)
sdp.solve('mosek')

print('O numero de Lovasz colorido deste grafo e:', -sdp.primal)
print('\n O valor dual e: ', -sdp.dual)
print('\n O status da SDP e:', sdp.status)

#--------------------------------------Obtendo os operadores de medicao--------------------
## Obter o dicionario de indices das variaveis
variables_indexes = sdp.monomial_index
A_indices = get_monomials_index_A(variables_indexes)
B_indices = get_monomials_index_B(variables_indexes)

## Obtendo os vetores de Gram da matriz de momentos
moment_matrix = sdp.x_mat[0]
from functions import decompose_gram_vectors
Gram = decompose_gram_vectors(moment_matrix)

## Construindo o dicionario de vetores para cada monomio
Alice_monomials_vectors = {}
Bob_monomials_vectors = {}
for vertex in range(n_vertices):
    Alice_monomials_vectors['A'+str(vertex)] = []
    Bob_monomials_vectors['B'+str(vertex)] = []
    for linha in A_indices['A'+str(vertex)]:
        Alice_monomials_vectors['A'+str(vertex)].append(Gram[linha])

    for linha in B_indices['B'+str(vertex)]:
        Bob_monomials_vectors['B'+str(vertex)].append(Gram[linha])

## Construindo os projetores de medicao
A = []
B = []
from functions import get_orthogonal_span
for key in Alice_monomials_vectors:
    A.append(get_orthogonal_span(Alice_monomials_vectors[key]))

for key in Bob_monomials_vectors:
    B.append(get_orthogonal_span(Bob_monomials_vectors[key]))

matrix = sum([A[i]@B[i] for i in range(len(A))])
val, vec = np.linalg.eigh(matrix)

## estado quantico
handle = Gram[0] / np.linalg.norm(Gram[0])
density_matrix = np.outer(handle.transpose(), handle)
print(density_matrix)
