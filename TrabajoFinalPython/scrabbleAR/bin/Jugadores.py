# ----------------------------------------------------------------------
#Clase padre de Jugador y JugadorPC
# ----------------------------------------------------------------------
class Jugadores:
    def __init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo):
        self.fichas = fichas
        self.puntaje = 0
        self.long_tablero = long_tablero
        self._botones = botones
        self.puntos_por_letra = puntos_por_letra
        self._dificultad = dificultad
        self._tipo = tipo  # tipo es una lista de tags en los que se pueden clasificar a los verbos, sustantivos y adjetivos

    def setFichas(self, fichas_nuevas):
        self.fichas = fichas_nuevas
        print("fichas", self.fichas)

    def getFichas(self):
        return self.fichas

    def getPuntos(self):
        return self.puntaje

    def sumPuntos(self, punt):
        self.puntaje += punt

    def es_palabra_valida(self, palabra):
        """
        Verifica si la palabra formada existe y devuelve true y es un Sustantivo, Adjetivo o Verbo segun a dificultad
        """
        from pattern.text.es import verbs, spelling, lexicon, parse
        import string
        if (palabra.lower() in verbs) or (palabra.lower() in spelling) or (palabra.lower() in lexicon) or (
                palabra.upper() in lexicon) or (palabra.capitalize() in lexicon):
            tipo_palabra = parse(palabra).split('/')[1] # devuelve un string de tipo 'mario/NN/B-NP/O', nos quedamos con el elem 'NN'
            print(tipo_palabra)
            print(tipo_palabra in self._tipo)
            return (tipo_palabra in self._tipo)
        else:
            return False

    def sumar_puntos(self, palabra_nueva):
        """
        Calculamos y actualizamos los puntos del jugador 
        """
        duplicar_palabra = False
        triplicar_palabra = False
        restar_uno = False
        restar_dos = False
        restar_tres = False
        puntos = 0
        for casillero, letra in palabra_nueva.items():
            puntaje_letra = self.puntos_por_letra[letra]
            if self._botones[casillero] == '++++':
                duplicar_palabra = True
            elif self._botones[casillero] == '+++':
                triplicar_palabra = True
            elif self._botones[casillero] == '+':  # duplicamos el puntaje por letra
                puntaje_letra = 2 * puntaje_letra
            elif self._botones[casillero] == '++':  # triplicamos el puntaje por letra
                puntaje_letra = 3 * puntaje_letra
            elif self._botones[casillero] == '---':  # se le resta 3 puntos al puntaje total obtenido
                restar_tres = True
            elif self._botones[casillero] == '--':  # se le resta 2 puntos al puntaje total obtenido
                restar_dos = True
            elif self._botones[casillero] == '-':  # se le resta 1 punto al puntaje total obtenido
                restar_uno = True
            puntos += puntaje_letra  # sumamos el puntaje por cada letra de la palabra
        if triplicar_palabra:
            puntos = 3 * puntos
        elif duplicar_palabra:
            puntos = 2 * puntos
        if restar_tres and puntos >= 3:  # restamos el puntaje si hay algun casillero descuento y el puntaje no queda negativo
            puntos -= 3
        elif restar_dos and puntos >= 2:
            puntos -= 2
        elif restar_uno and puntos >= 1:
            puntos -= 1

        print(str(puntos))
        self.sumPuntos(puntos)

    def restar_puntos_finales(self):
        for letra in self.fichas.values():
            if (letra != ''):
                if (self.puntaje != 0) and (self.puntaje - self.puntos_por_letra[letra] > 0):
                    self.puntaje -= self.puntos_por_letra[letra]
                else:
                    self.puntaje = 0

    puntos = property(getPuntos, sumPuntos, doc="Setter y Getter")
