import numpy as np
import matplotlib.pyplot as plt

# Generar 100 numeros aleatorios con distribucion exponencial con beta = 3
exponential_random_numbers = np.random.exponential(scale=3, size=100)

# Calcular la media de los valores aleatorios generados
mean = np.mean(exponential_random_numbers)
print(f'Media muestral de 100 valores: {mean}')

# Calcular el desvio estandar de los valores aleatorios generados
std_dev = np.std(exponential_random_numbers)
print(f'Desvio standar de 100 valores: {std_dev}')

# Calcular la varianza de los valores aleatorios generados
variance = np.var(exponential_random_numbers)
print(f'Varianza de 100 valores: {variance}')

# ----------------------------------------- #
print('\n')

# Generar 1000 numeros aleatorios con distribucion exponencial con beta = 3
exponential_random_numbers = np.random.exponential(scale=3, size=100)

# Calcular la media de los valores aleatorios generados
mean = np.mean(exponential_random_numbers)
print(f'Media muestral de 1000 valores: {mean}')

# Calcular el desvio estandar de los valores aleatorios generados
std_dev = np.std(exponential_random_numbers)
print(f'Desvio standar de 1000 valores: {std_dev}')

# Calcular la varianza de los valores aleatorios generados
variance = np.var(exponential_random_numbers)
print(f'Varianza de 1000 valores: {variance}')
