import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

## comportamentos dados
p_local = np.array([1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0])
p_identidade = np.full((16),1/4)
p_PR = np.array([1/2,0,0,1/2,1/2,0,0,1/2,1/2,0,0,1/2,0,1/2,1/2,0])

# variavel do problema
alpha = cp.Variable()
beta = cp.Parameter()

# definindo funcao objetiva
p = alpha*p_PR + (1 - alpha)*(beta*p_local + (1 - beta)*p_identidade)
objective = cp.Maximize(alpha)

# restricao de localidade
CHSH = np.array([[1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,-1,1,1,-1],
              [1,-1,-1,1,1,-1,-1,1,-1,1,1,-1,1,-1,-1,1],
              [1,-1,-1,1,-1,1,1,-1,1,-1,-1,1,1,-1,-1,1],
              [-1,1,1,-1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1]])

constraints = [CHSH @ p <= 2, -CHSH @ p <= 2]

# Resolvendo
problem = cp.Problem(objective,constraints)

alpha_value = []
for step in np.linspace(0,1,20):
    beta.value = step

    problem.solve()
    alpha_value.append(alpha.value)

plt.plot(np.linspace(0,1,20), alpha_value)
plt.show()
