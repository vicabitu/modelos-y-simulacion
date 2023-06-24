class Evento:
    def __init__(self, objeto, duracion, nombre):
        self.objeto = objeto
        self.duracion = duracion
        self.nombre = nombre
    
    def __str__(self):
        info_camion = self.objeto.__str__()
        return f'Evento {self.nombre} | Recurso: {info_camion} - Nuevo reloj: {self.duracion}'