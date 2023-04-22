import numpy as np

def calcular_intervalor_de_confianza(
  tamanio_de_la_muestra, coeficiente_z, media, desvio_estandar
):
  extermo_superior = media + coeficiente_z * (
    (desvio_estandar * 2) / tamanio_de_la_muestra
  )
  extermo_inferior = media - coeficiente_z * (
    (desvio_estandar * 2) / tamanio_de_la_muestra
  )

  return {"extremo_superior": extermo_superior, "extermo_inferior": extermo_inferior}

muestra = np.random.uniform(low=0.0, high=1.0, size=1000)
tamanio_de_la_muestra = muestra.size
coeficiente_z = 2.33
media = np.mean(muestra)
desvio_estandar = np.std(muestra)

intervalo_de_confinanza = calcular_intervalor_de_confianza(
  tamanio_de_la_muestra, coeficiente_z, media, desvio_estandar
)

print(f"Extermo superior: {intervalo_de_confinanza.get('extremo_superior')}")
print(f"Extermo inferior: {intervalo_de_confinanza.get('extermo_inferior')}")