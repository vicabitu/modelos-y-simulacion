import numpy as np
import matplotlib.pyplot as plt

# Generar 100 numeros aleatorios con distribucion uniforme entre 0 y 1
uniform_random_numbers = np.random.uniform(low=0.0, high=1.0, size=100)
print('100 números aleatorios con distribucion uniforme')
print(uniform_random_numbers)

# Calcular la media de los numeros aleatorios generados
mean = np.mean(uniform_random_numbers)
print(f'Media: {mean}')

# Calcular la desviacion standar de los numeros aleatorios generados
std_dev = np.std(uniform_random_numbers)
print(f'Desvio standar: {std_dev}')

# Calcular varianza de los numeros aleatorios generados
variance = np.var(uniform_random_numbers)
print(f'Varianza: {variance}')

# Crear el histograma con Matplotlib
plt.hist(uniform_random_numbers, bins=10, edgecolor='black')

# Configurar los nombre de los ejes y el titulo del grafico
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de números aleatorios con distribución Uniforme')

# Mostrar el grafico
plt.show()