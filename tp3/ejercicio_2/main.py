import numpy as np
import matplotlib.pyplot as plt

# a

# Generar 1000 numeros aleatorios con distribucion uniforme entre 0 y 1
uniform_random_numbers = np.random.uniform(low=0.0, high=1.0, size=1000)

# Mostrar los numeros aleatorios generados
print('1000 números aleatorios con distribucion uniforme')
print(uniform_random_numbers)

# Crear el histograma con Matplotlib
plt.hist(uniform_random_numbers, bins=10, edgecolor='black')

# Configurar los nombres de los ejes y el titulo del grafico
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de números aleatorios con distribución Uniforme')

# Mostrar el grafico
plt.show()

# b

# Generar 1000 numeros aleatorios con distribucion normal con media 0 y desvio 1
normal_random_numbers = np.random.normal(loc=0, scale=1, size=1000)

# Mostrar los numeros aleatorios generados
print('1000 números aleatorios con distribucion normal')
print(normal_random_numbers)

# Crear el histograma con Matplotlib
plt.hist(normal_random_numbers, bins=40, density=False, alpha=0.75, edgecolor='black')

# Configurar los nombres de los ejes y el titulo del grafico
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de números aleatorios con distribución normal')

# Mostrar el grafico
plt.show()

# c

# Generar 1000 numeros aleatorios con distribucion Poisson con lambda = 6
poisson_random_numbers = np.random.poisson(lam=6, size=1000)
# Mostrar los numeros aleatorios generados
print('1000 números aleatorios con distribucion Poisson')
print(poisson_random_numbers)

# Crear el histograma con Matplotlib
plt.hist(poisson_random_numbers, bins=10, edgecolor='black')

# Configurar los nombres de los ejes y el titulo del grafico
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de números aleatorios con distribución de Poisson')

# Mostrar el grafico
plt.show()

# d

# Generar 1000 numeros aleatorios con distribucion exponencial con beta = 3/4
exponential_random_numbers = np.random.exponential(scale=3/4, size=1000)

# Mostrar los numeros aleatorios generados
print('1000 números aleatorios con distribucion exponencial')
print(exponential_random_numbers)

# Create the histogram with Matplotlib
plt.hist(exponential_random_numbers, bins=20, edgecolor='black')

# Set the names of the axes and the chart title
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de números aleatorios con distribución Exponencial')

# Mostrar el grafico
plt.show()