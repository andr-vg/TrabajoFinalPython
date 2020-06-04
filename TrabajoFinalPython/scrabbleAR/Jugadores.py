class Jugadores:
    def __init__ (self,fichas,long_tablero,botones,puntos_por_letra,dificultad,tipo):
        self.fichas = fichas 
        self.puntaje = 0 
        self.long_tablero = long_tablero
        self._botones = botones
        self.puntos_por_letra = puntos_por_letra
        self._dificultad = dificultad
        self._tipo = tipo

    def setFichas(self, fichas_nuevas):
        self.fichas = fichas_nuevas
        print("fichas",self.fichas)

    def getFichas(self):
        return self.fichas
    
    def getPuntos(self):
        return self.puntaje 

    def sumPuntos(self,punt):
        self.puntaje += punt

    def sumar_puntos(self,palabra_nueva):
        duplicar = False
        triplicar = False
        puntos = 0
        for casillero, letra in palabra_nueva.items():
            puntaje_letra = self.puntos_por_letra[letra]
            if self._botones[casillero] == '+':  # duplicamos el puntaje por letra
                puntaje_letra = 2 * puntaje_letra
                duplicar = True
            elif self._botones[casillero] == '++':  # triplicamos el puntaje por letra
                puntaje_letra = 3 * puntaje_letra
                triplicar = True
            elif self._botones[casillero] == '-':  # se le resta 1 punto al puntaje total obtenido
                puntos += -1
            elif self._botones[casillero] == '--':  # se le resta 2 puntos al puntaje total obtenido
                puntos += -2
            elif self._botones[casillero] == '---':  # se le resta 3 puntos al puntaje total obtenido
                puntos += -3
            puntos += puntaje_letra  # sumamos el puntaje por cada letra de la palabra
        if triplicar:
            puntos = 3 * puntos
        elif duplicar:
            puntos = 2 * puntos
        print(str(puntos))
        self.sumPuntos(puntos)
    
    puntos =  property(getPuntos,sumPuntos,doc="Settet y Getter")