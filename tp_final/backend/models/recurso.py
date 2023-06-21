class Recurso:
    def __init__(self, tipo='Puesto', libre=True, camion=None, cola=[]):
        self.tipo = tipo
        self.libre = libre
        self.camion = camion
        self.cola = cola
    
    def eliminar_camion(self, camion):
        self.cola.remove(camion)
    
    def __str__(self):
        info_camion = self.camion.__str__()
        return f'Tipo: {self.tipo} - Libre: {self.libre} - Cola: {len(self.cola)} - Camion: {info_camion}'