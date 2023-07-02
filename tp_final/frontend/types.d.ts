type Anio = {
  cantidadProducidaPorDia: { name: number; value: number }[];
  cantidadDeProduccionTotal: number;
  promedioDeProduccion: number;
  tiempoViajandoCamiones: number;
  tiempoSinViajarCamiones: number;
  promedioMinutosSinMateriaPrimaPorDia: number;
  minutosSinMateriaPrimaPorDia: { name: number; value: number }[];
  anio: number;
  tiemposDeOcupacionBalanzas: {
    id: number;
    ocupacion: string;
    ociosos: string;
  }[];
}