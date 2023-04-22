import numpy as np
import matplotlib.pyplot as plt

def exponencial(beta, u):
    # Aplicar la transformacion inversa
    x = -beta * np.log(1 - u)
    return x

# Generar 1000 numeros aleatorios con distribucion uniforme entre 0 y 1
uniform_random_numbers = np.random.uniform(low=0.0, high=1.0, size=1000)
# Definir valor de beta
beta = 12

exponential_numbers = exponencial(beta, uniform_random_numbers)
print(exponential_numbers)

# Crear el histograma con Matplotlib
plt.hist(exponential_numbers, bins=10, edgecolor='black')

# Configurar los nombres de los ejes y el titulo del grafico
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de números aleatorios con distribución exponencial')

# Mostrar el grafico
plt.show()
