class Camion:
    def __init__(self, tipo, carga=0):
        self.tipo = tipo
        self.carga = carga
    
    def set_carga(self, carga):
        self.carga = carga
    
    def __str__(self):
        return f'Tipo: {self.tipo} - Carga: {self.carga}'
