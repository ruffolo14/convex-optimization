# convex-optimization
Este repositório contém alguns dos principais programas que construi durante meu aprendizado em solução de problemas de otimização convexa.

O primeiro programa encontra do número de Lovasz para um grafo de 8 vértices.

## onecolor_graphs
Dentro do diretório onecolor_graphs/ncpol2sdpa/ encontra-se um programa para determinar o número de Lovasz de qualquer ciclo de uma cor, chamado ncpol_lovasz_ciclos.py. Este programa também retorna os projetores de medição como matrizes, em um dicionário cuja as entradas são 'monomio':matrix. 

Algumas funções foram definidas para auxiliar na execução das tarefas. Estas estão descritas na seção funções.

## multicolor_graphs
Neste diretório, encontra-se um programa para determinar o número de multilovasz para um multigrafo colorido, neste caso, aquele que representa o cenário CHSH em multigrafos.

## funções
**decompose_gram_vectors(matrix**: Recebe como entrada *matrix*, uma matriz positiva-semidefinida e retorna como saida uma lista dos vetores de Gram associados a essa matriz.

**get_orthogonal_span(list_vectors)**: Recebe como entrada *list_vectors*, uma lista de vetores quaisquer e retorna uma lista de vetores ortogonais entre si que geram o mesmo subspaço vetorial da lista de entrada (processo de Gram-Schmidt).


