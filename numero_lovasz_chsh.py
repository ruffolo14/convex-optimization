'''
Neste programa, calcularemos o número de Loszvas para o cenario (2,2,2)
utilizando o algoritmo descrito na aula 11 do Rafael. Os passos sao
1- Definir a feasible_matrix
2- Definir a variavel normalized_orthogonal_labeling
3- Adicionar as restricoes
4- Definir a funcao objetiva
5- Maximizar '' ''    ''
'''
import numpy as np
import cvxpy as cp

#Arestas do grafo
edges = [] #lista
for vertex in range(8):
    next_vertex = (vertex+1)%8
    opposite_vertex = (vertex+4)%8
    edges.append([vertex,next_vertex])
    edges.append([vertex,opposite_vertex])


#Definindo feasible_matrix
feasible_matrix = np.ones((8,8))

#Definindo normalized_orthogonal_labeling
normalized_orthogonal_labeling = cp.Variable((8,8), PSD=True)

#Restricoes
constraints = [] #Lista
constraints.append(cp.trace(normalized_orthogonal_labeling) == 1)
for i,j in edges:
    constraints.append(normalized_orthogonal_labeling[i,j] == 0)


#Funcao objetiva
objective_function = cp.trace(feasible_matrix*normalized_orthogonal_labeling)

#Maximizando a funcao objetiva
convex_opt_problem = cp.Problem(cp.Maximize(objective_function),constraints)
convex_opt_problem.solve()

print('O numero de Lovasz e:\n', convex_opt_problem.value)
print('Status do problema:', convex_opt_problem.status)