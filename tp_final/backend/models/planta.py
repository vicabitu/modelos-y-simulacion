class Planta:
    def __init__(self):
        self.libre = True

    def __str__(self):
        estado = 'Libre' if self.libre else 'Ocupada'
        return f'Planta: Libre: {estado}'