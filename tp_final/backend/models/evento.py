class Evento:
    def __init__(self, objeto, duracion, nombre):
        self.objeto = objeto
        self.duracion = duracion
        self.nombre = nombre
    
    def __str__(self):
        return f'Camion: tipo {self.objeto.tipo} - Duracion: {self.duracion} - Nombre: {self.nombre}'