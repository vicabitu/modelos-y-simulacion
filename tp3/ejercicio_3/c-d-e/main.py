import numpy as np
import matplotlib.pyplot as plt

# c

# Generar 100 numeros aleatorios con distribucion exponencial con beta = 3
one_hundred_exponential_random_numbers = np.random.exponential(scale=3, size=100)
print(one_hundred_exponential_random_numbers)

# d

# Generar 1000 numeros aleatorios con distribucion exponencial con beta = 3
thousand_exponential_random_numbers = np.random.exponential(scale=3, size=1000)
print(thousand_exponential_random_numbers)

# e

# Crear el histograma con Matplotlib
plt.hist(one_hundred_exponential_random_numbers, bins=12, edgecolor='black')

# Configurar los nombres de los ejes y el titulo del grafico
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de 100 números aleatorios con distribución exponencial')

# Mostrar el grafico
plt.show()

# Crear el histograma con Matplotlib
plt.hist(thousand_exponential_random_numbers, bins=12, edgecolor='black')

# Configurar los nombres de los ejes y el titulo del grafico
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de 1000 números aleatorios con distribución exponencial')

# Mostrar el grafico
plt.show()