class Jugador():
    def __init__(self):
        self.puntaje = 0

    def sumPuntos(self,punt):
        self.puntaje += punt

    def getPuntos(self):
        return self.puntaje

    puntos =  property(getPuntos,sumPuntos,doc="Settet y Getter")


