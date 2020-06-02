import IdentificarPalabra as es
import PySimpleGUI as sg
import random
class PC():
    def __init__ (self,fichas,long_tablero,botones,puntos_por_letra,dificultad,tipo):
        self.fichas = fichas #Fichas seria una lista de CHAR
        self.puntaje = 0 
        self.long_tablero = long_tablero
        self._botones = botones
        self.puntos_por_letra = puntos_por_letra
        self._dificultad = dificultad
        self._tipo = tipo
        self._palabras_usadas = []

    def setFichas(self, fichas_nuevas):
        self.fichas = fichas_nuevas
        print("fichas",self.fichas)

    def getFichas(self):
        return self.fichas
    
    def getPuntos(self):
        return self.puntaje 

    def sumPuntos(self,punt):
        self.puntaje += punt

    def reinicioFichas(self,palabra):
        cant = len(palabra)
        for clave in self.fichas.keys():
            if cant > 0:
                if self.fichas[clave] in palabra:
                    self.fichas[clave] = ""
                    cant += -1
            else: 
                break
    def _sumar_puntos(self,palabra_nueva):
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

    def _obtenerPalabra(self):
        import itertools as it
        from pattern.text.es import verbs, spelling, lexicon , parse
        """
        obtiene una palabra a partir de las _fichas
        """
        letras = ""
        for letra in self.fichas.values():
            print("LETRA;",letra)
            letras += letra
        letras = letras.lower()
        l=[]
        s=spelling.keys()
        le=lexicon.keys()
        for opcion in range(2,len(letras)+1): #iterar por la combinación
            pals = it.combinations(letras,opcion)
            for combinacion in pals:
                for pal in combinacion:
                    p = list(it.permutations(combinacion))
                    for f in p:
                        evaluation = "".join(f)
                        if evaluation in s and evaluation in le:
                            l.append(evaluation)

        l=list(set(l))
        print("LISTA",l)
        valido = False
        
        try:
            palabra=max(l,key=lambda x: len(x))
        except:
            palabra = ""
        if not (palabra.lower() in verbs) and (not palabra.lower() in spelling) and (not(palabra.lower() in lexicon) and not(palabra.upper() in lexicon) and not(palabra.capitalize() in lexicon))and (palabra in self._palabras_usadas):
            print("la palabra no existe")
        else:
            tipo_palabra = parse(palabra)
            if (self._dificultad == "facil"):
                valido = ("NN" in tipo_palabra) 
            elif (self._dificultad == "medio"):
                valido =  ("VB" in tipo_palabra) or ("JJ" in tipo_palabra)
            else:
                if self._tipo in tipo_palabra:   #Tipo seria un string que le se asigna aleatoreamente el tipo de una lista donde esta "NN" "JJ" y "VB"
                    valido = True
            self._palabras_usadas.append(palabra)
            return palabra.upper() if valido else ""

    def _mapeoHorizontal(self, i, j, posiciones_ocupadas_tablero):
        cant = 0
        posiciones = []
        while not (i,j) in posiciones_ocupadas_tablero and j < self.long_tablero:
            cant += 1
            posiciones.append((i,j))
            j += 1
        return cant, posiciones

    def _mapeoVertical(self, i, j, posiciones_ocupadas_tablero):
        cant = 0
        posiciones = []
        while not (j,i) in posiciones_ocupadas_tablero and j < self.long_tablero:
            cant += 1
            posiciones.append((j,i))
            j += 1
        return cant, posiciones

    def _agrego_posiciones(self, cant, posiciones, long_y_posiciones):
        if cant >= 2: 
            if not cant in long_y_posiciones.keys():
                long_y_posiciones[cant] = [posiciones]
            else:
                long_y_posiciones[cant].append(posiciones)

    def _mapear_tablero(self,posiciones_ocupadas_tablero):
        """ Esta funcion recibe las posiciones ocupadas en el tablero, mapea lugares disponibles y los devuelve
            en un diccionario long_y_posiciones cuyas claves son la longitud del lugar disponible y valores son
            listas con listas de las posiciones disponibles para esas longitudes 
        """
        long_y_posiciones = dict()
        for i in range(self.long_tablero):
            j = 0  
            while j < self.long_tablero: 
                cant, posiciones = self._mapeoHorizontal(i, j, posiciones_ocupadas_tablero) # mapeo horizontalmente
                self._agrego_posiciones(cant, posiciones, long_y_posiciones)
                cant, posiciones = self._mapeoVertical(j, i, posiciones_ocupadas_tablero) # mapeo verticalmente
                self._agrego_posiciones(cant, posiciones, long_y_posiciones)
                j += 1
        return long_y_posiciones 

    def _calcular_long_maxima(self,long_max_tablero, cant_fichas):
        """Esta funcion retorna la longitud maxima segun dos cosas: la cantidad de fichas disponibles
         y el mayor numero de casilleros contiguos libres en el tablero. Tenemos dos casos:
         - si el nro de casilleros supera o es igual a la cant de fichas, con mandarle la cant de fichas
        que tengo le basta.
        - si el nro de casilleros es menor que la cantidad de fichas: ahi la palabra a formar tiene que ocupar
        como maximo esos casilleros, asique le mando ese valor
        """
        if long_max_tablero >= cant_fichas:
            return cant_fichas
        else:
            return long_max_tablero    

    def jugar(self,window,posiciones_ocupadas_tablero):
        long_y_posiciones = self._mapear_tablero(posiciones_ocupadas_tablero) # obtenemos las posiciones libres en el tablero
        long_max_tablero = max(long_y_posiciones.keys()) # calculamos la long maxima entre todas esas posiciones libres
        long_max = self._calcular_long_maxima(long_max_tablero, len(self.fichas)) # nos quedamos con la max entre casillas y cant fichas
        mejor_palabra = self._obtenerPalabra()  # obtenemos la mejor palabra posible
        if mejor_palabra != "":  # caso en que encuentra una palabra valida
            posiciones_random = random.randint(0, len(long_y_posiciones[long_max_tablero])-1)
            inicio_columna = random.randint(0,(long_max_tablero-len(mejor_palabra)))
            fin_columna = inicio_columna + len(mejor_palabra)
            palabra_nueva = dict()
            for i in range(inicio_columna,fin_columna):   # agregamos las posiciones a la lista de posiciones ocupadas
                posiciones_ocupadas_tablero.append(long_y_posiciones[long_max_tablero][posiciones_random][i])
                print(long_y_posiciones[long_max_tablero][posiciones_random][i])
                window[long_y_posiciones[long_max_tablero][posiciones_random][i]].update(mejor_palabra[i-inicio_columna], disabled=True,button_color=("black","#A4E6FD")) # agregamos las letras al tablero
                # guardamos las posiciones y las letras de la palabra en palabra_nueva así despues sumamos los puntos
                palabra_nueva[long_y_posiciones[long_max_tablero][posiciones_random][i]] = mejor_palabra[i-inicio_columna]                
        
            ## llamamos a la funcion sumar_puntos de la clase padre y actualizamos los puntos:
            # self.sumPuntos(sumar_puntos(puntos_por_letra, botones, palabra_nueva)) comentada hasta formar la clase padre
            # window['p_pc'].update("Puntos PC:"+str(self.getPuntos())) # aca se actualizaria la ventana
            ## actualizamos las fichas de la pc:
            print("MEJOR PALABRA",mejor_palabra)
            print("PALABRA NUEVA",palabra_nueva)
            self._sumar_puntos(palabra_nueva)
            self.reinicioFichas(mejor_palabra)
            print("SELF PUNTOS",self.puntos)
            window["p_pc"].update(str(self.puntos))        

        else:
            sg.popup("La PC le ha pasado el turno")
            letras = ""
            self.reinicioFichas(letras.join(self.fichas.values()))


    puntos = property(getPuntos,sumPuntos,doc="Setters y getters")