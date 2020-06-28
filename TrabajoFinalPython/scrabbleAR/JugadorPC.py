import PySimpleGUI as sg
import random
import json
from Jugadores import Jugadores
import os

absolute_path = os.path.dirname(os.path.abspath(__file__))

###################### Clase Jugador PC ##############################

class PC(Jugadores):
    def __init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo, guardada):
        Jugadores.__init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo)
        self._palabras_usadas = []
        self._pos_usadas_tablero = []
        self._partida_guardada = guardada
        if (guardada):
            self._cargar_estado()

    def reinicioFichas(self, palabra):
        """
        Reinicia los valores de las fichas usadas en "" para luego ser actualizadas por nuevos valores de la bolsa
        """
        cant = len(palabra)
        for clave in self.fichas.keys():
            if cant > 0:
                if self.fichas[clave] in palabra:
                    self.fichas[clave] = ""
                    cant += -1
            else:
                break
    
    def actualiza_botones(self,botones):
        """
        Actualiza el diccionario botones con las pos usadas por el usuario
        """

        self._botones = botones

    def _convertirJson(self):
        """
        Parsea el Json para poder guardarlo
        """
        import pprint
        p = pprint.PrettyPrinter(indent = 2)
        p.pprint(self._botones)
        dic_aux = {}
        for clave,valor in self._botones.items():
            dic_aux[str(clave[0])+","+str(clave[1])] = valor        
        return dic_aux
    
    def _convertirDic(self,botones):
        """
        Vuelve a darle formato al diccionario de botones
        """
        dic_aux = {}
        for clave,valor in botones.items():
            dic_aux[tuple(map(int,clave.split(",")))] = valor  
        import pprint
        # p = pprint.PrettyPrinter(indent=4)
        # p.pprint(dic_aux)
        return dic_aux

    def guardar_estado(self):
        """
        Guarda el estado interno del jugador PC
        """

        arch = open(os.path.join(absolute_path, "Datos","info","datos_pc.json"), "w")
        datos = {"fichas":self.fichas,"botones":self._convertirJson(),"palabras_usadas":self._palabras_usadas,"pos_usadas":self._pos_usadas_tablero}
        json.dump(datos,arch,indent = 4)
        arch.close()

    def _cargar_estado(self):
        """
        Si la partida esta guardada carga el estado guardado en un json
        """
        datos = open(os.path.join(absolute_path, "Datos","info","datos_pc.json"), "r")
        data = {}
        data = json.load(datos)
        self._fichas = data["fichas"]
        self._botones = self._convertirDic(data["botones"])
        self._palabras_usadas = data["palabras_usadas"]
        self._pos_usadas_tablero = data["pos_usadas"]
    def _obtenerPalabra(self, long_max):
        """
        obtiene una palabra a partir de las _fichas
        """
        import itertools as it
        from pattern.text.es import verbs, spelling, lexicon, parse
        
        letras = ""
        for letra in self.fichas.values():
            print("LETRA;", letra)
            letras += letra
        letras = letras.lower()
        l = []
        s = spelling.keys()
        le = lexicon.keys()

        for opcion in range(2, long_max + 1):  # iterar por la combinación
            pals = it.combinations(letras, opcion)
            for combinacion in pals:
                for pal in combinacion:
                    p = list(it.permutations(combinacion))
                    for f in p:
                        evaluation = "".join(f)
                        if evaluation in s and evaluation in le:
                            l.append(evaluation)

        l = list(set(l))
        valido = False

        try:
            palabra = max(l, key=lambda x: len(x))
        except:
            palabra = ""
        if not palabra in self._palabras_usadas:
            valido = self.es_palabra_valida(palabra)
            if valido:
                self._palabras_usadas.append(palabra)
        return palabra.upper() if valido else ""

    def _mapeoHorizontal(self, i, j, posiciones_ocupadas_tablero):
        """
        Mapeamos el tablero fila por fila y agregamos las posiciones libres encontradas
        """
        cant = 0
        posiciones = []
        while not (i, j) in posiciones_ocupadas_tablero and j < self.long_tablero:
            cant += 1
            posiciones.append((i, j))
            j += 1
        return cant, posiciones

    def _mapeoVertical(self, i, j, posiciones_ocupadas_tablero):
        """
        Mapeamos el tablero columna por columna y agregamos las posiciones libres encontradas
        """
        cant = 0
        posiciones = []
        while not (j, i) in posiciones_ocupadas_tablero and j < self.long_tablero:
            cant += 1
            posiciones.append((j, i))
            j += 1
        return cant, posiciones

    def _agrego_posiciones(self, cant, posiciones, long_y_posiciones):
        """
        Agregamos a long_y_posiciones las posiciones libres encontradas de longitud >=2
        """
        if cant >= 2:
            if not cant in long_y_posiciones.keys():
                long_y_posiciones[cant] = [posiciones]
            else:
                long_y_posiciones[cant].append(posiciones)

    def _mapear_tablero(self, posiciones_ocupadas_tablero):
        """ 
        Esta funcion recibe las posiciones ocupadas en el tablero, mapea lugares disponibles y los devuelve
        en un diccionario long_y_posiciones cuyas claves son la longitud del lugar disponible y valores son
        listas con listas de las posiciones disponibles para esas longitudes 
        """
        long_y_posiciones = dict()
        for i in range(self.long_tablero):
            j = 0
            while j < self.long_tablero:
                cant, posiciones = self._mapeoHorizontal(i, j, posiciones_ocupadas_tablero)  # mapeo horizontalmente
                self._agrego_posiciones(cant, posiciones, long_y_posiciones)
                cant, posiciones = self._mapeoVertical(j, i, posiciones_ocupadas_tablero)  # mapeo verticalmente
                self._agrego_posiciones(cant, posiciones, long_y_posiciones)
                j += 1
        return long_y_posiciones

    def _calcular_long_maxima(self, long_max_tablero, cant_fichas):
        """
        Esta funcion retorna la longitud maxima segun dos cosas: la cantidad de fichas disponibles
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

    def jugar(self, window, posiciones_ocupadas_tablero, primer_turno):
        """
        Jugada del usuario: se forma la palabra más larga posible según la dificultad.
        Se mapea el tablero para obtener las posiciones libres donde puede ubicarse la palabra obtenida.
        Dificultad facil: Se obtiene una lista de posiciones aleatoria en la que entre en la palabra.
                          -- > Por el momento implementamos esta dificultad para los tres niveles.
        Dificultad media: Se obtiene una lista de posiciones con al menos un casillero premio (de ser posible)
                          y la palabra más larga que quepe en esas posiciones. --> falta implementar 
        Dificultad dificil: Se obtiene una lista con las posiciones que sumen más puntos, la palabra que sume 
                            más puntos y quepa ahí, y se ubica la letra de mayor puntaje en alguna casillero 
                            premio (de ser posible) --> falta implementar
        """

        long_y_posiciones = self._mapear_tablero(
            posiciones_ocupadas_tablero)  # obtenemos las posiciones libres en el tablero
        long_max_tablero = max(long_y_posiciones.keys())  # calculamos la long maxima entre todas esas posiciones libres
        long_max = self._calcular_long_maxima(long_max_tablero, len(
            self.fichas.values()))  # nos quedamos con la max entre casillas y cant fichas
        mejor_palabra = self._obtenerPalabra(long_max)  # obtenemos la mejor palabra posible
        if mejor_palabra != "":  # caso en que encuentra una palabra valida
            if not primer_turno:
                posiciones_random = random.randint(0, len(
                    long_y_posiciones[long_max_tablero]) - 1)  # me quedo con una lista de posiciones valida
                inicio = random.randint(0, (long_max_tablero - len(mejor_palabra)))
                fin = inicio + len(mejor_palabra)
                palabra_nueva = dict()
                for i in range(inicio, fin):  # agregamos las posiciones a la lista de posiciones ocupadas
                    posiciones_ocupadas_tablero.append(long_y_posiciones[long_max_tablero][posiciones_random][i])
                    # print(long_y_posiciones[long_max_tablero][posiciones_random][i])
                    pos_aux =long_y_posiciones[long_max_tablero][posiciones_random][i]
                    print("MAX: ",long_max_tablero,"Pos random: ",posiciones_random,"Pos de palabra: ",pos_aux)
                    window[pos_aux].update(mejor_palabra[i - inicio], disabled=True,button_color=("black","#A4E6FD"))  # agregamos las letras al tablero
                    # guardamos las posiciones y las letras de la palabra en palabra_nueva así despues sumamos los puntos
                    palabra_nueva[long_y_posiciones[long_max_tablero][posiciones_random][i]] = mejor_palabra[i - inicio]
                    self._botones[long_y_posiciones[long_max_tablero][posiciones_random][i]] = "" + "*"
            else:  ## primer turno de la compu: ubicamos la palabra en el centro del tablero
                primer_turno = False
                palabra_nueva = dict()
                centro = self.long_tablero // 2
                indice_letra_centro = random.randint(0, len(mejor_palabra) - 1)
                orientacion = random.randint(0, 1)  ## orientacion = 1 : vertical, 0: horizontal
                print(mejor_palabra)
                print(mejor_palabra[indice_letra_centro])
                for i in range(centro - indice_letra_centro, centro):  # antes del centro
                    pos = (centro, i) if orientacion == 0 else (i, centro)
                    posiciones_ocupadas_tablero.append(pos)
                    print(pos)
                    print(mejor_palabra[indice_letra_centro - (centro - i)])
                    window[pos].update(mejor_palabra[indice_letra_centro - (centro - i)], disabled=True,
                                       button_color=("black", "#A4E6FD"))  # agregamos las letras al tablero
                    self._botones[pos] = "" + "*"
                    palabra_nueva[pos] = mejor_palabra[indice_letra_centro - (centro - i)]
                posiciones_ocupadas_tablero.append((centro, centro))  # agregamos el centro
                window[(centro, centro)].update(mejor_palabra[indice_letra_centro], disabled=True,
                                                button_color=("black", "#A4E6FD"))  # agregamos las letras al tablero
                self._botones[(centro,centro)] = "" + "*"
                palabra_nueva[(centro, centro)] = mejor_palabra[indice_letra_centro]
                print((centro, centro))
                print(mejor_palabra[indice_letra_centro])
                for i in range(centro + 1, centro + len(mejor_palabra) - indice_letra_centro):  # despues del centro
                    pos = (centro, i) if orientacion == 0 else (i, centro)
                    print(pos)
                    print(mejor_palabra[indice_letra_centro - (centro - i)])
                    posiciones_ocupadas_tablero.append(pos)
                    window[pos].update(mejor_palabra[indice_letra_centro + i - centro], disabled=True,
                                       button_color = ("black", "#A4E6FD"))  # agregamos las letras al tablero
                    self._botones[pos] = "" + "*"
                    palabra_nueva[pos] = mejor_palabra[indice_letra_centro + i - centro]
                    

            ## llamamos a la funcion sumar_puntos de la clase padre y actualizamos los puntos:
            self.sumar_puntos(palabra_nueva)
            ## actualizamos las fichas de la pc:        
            self.reinicioFichas(mejor_palabra)
            ## se actualizan los puntos         
            window["p_pc"].update(str(self.getPuntos()))
            self._pos_usadas_tablero = posiciones_ocupadas_tablero

        else:
            sg.popup("La PC le ha pasado el turno")
            letras = ""
            self.reinicioFichas(letras.join(self.fichas.values()))
        return primer_turno
    
    def get_botones(self):
        """
        Devuelve el diccionario botones para el guardado de la partida
        """
        return self._botones
