import IdentificarPalabra as es 
class Jugador():
    def __init__(self,fichas):
        self.fichas = fichas
        self.puntaje = 0

    def sumPuntaje(self,punt):
        self.puntaje += punt


