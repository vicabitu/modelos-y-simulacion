uniform_random_numbers <- runif(100, min=0, max=1)
mean <- mean(uniform_random_numbers)
print("Media:")
print(mean)
std_dev <- sd(uniform_random_numbers)
print("Desvio estandar:")
print(std_dev)
variance <- var(uniform_random_numbers)
print("Varianza")
print(variance)
hist(
    uniform_random_numbers,
    main="Histograma de números aleatorios con distribución Uniforme",
    xlab="Valores",
    ylab="Frecuencia"
)