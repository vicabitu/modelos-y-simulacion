class Evento:
    def __init__(self, objeto, duracion, nombre):
        self.objeto = objeto
        self.duracion = duracion
        self.nombre = nombre
    
    def __str__(self):
        info_camion = self.objeto.__str__()
        return f'Camion: {info_camion} - Duracion: {self.duracion} - Nombre: {self.nombre}'