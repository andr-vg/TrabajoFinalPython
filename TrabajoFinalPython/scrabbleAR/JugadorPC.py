import IdentificarPalabra as es
import PySimpleGUI as sg
import random
class PC():
    def __init__ (self,fichas,long_tablero,botones,puntos_por_letra):
        self.fichas = fichas #Fichas seria una lista de CHAR
        self.puntaje = 0 
        self.long_tablero = long_tablero
        self.botones = botones
        self.puntos_por_letra = puntos_por_letra
        #Estos 2 los tengo que acomodar cuando haga la herencia
        self._dificultad = "facil"
        self._tipo = "NN"

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

    def _tiene_vocales(self,palabra):
        for letra in palabra:
            if letra in "AEIOU":
                return True
        return False
    
    def _tiene_consonantes(self,palabra):
        for letra in palabra:
            if not letra in "AEIOU":
                return True
        return False
       
    # def _obtenerPalabra(self,long_max):
    #     palabra = ""
    #     lista_palabras = []
    #     lista_fichas = list(self.fichas.values()) #Hago lista de las fichas
    #     self._recursividadPalabras(lista_fichas,long_max,palabra,lista_palabras)
    #     return "" if len(lista_palabras) == 0 else max(lista_palabras)
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
        if not (palabra.lower() in verbs) and (not palabra.lower() in spelling) and (not(palabra.lower() in lexicon) and not(palabra.upper() in lexicon) and not(palabra.capitalize() in lexicon)):
            print("la palabra no existe")
        else:
            tipo_palabra = parse(palabra)
            if (self._dificultad == "facil"):
                valido = ("NN" in tipo_palabra) or ("VB" in tipo_palabra) or ("JJ" in tipo_palabra)
            elif (self._dificultad == "medio"):
                valido =  ("VB" in tipo_palabra) or ("JJ" in tipo_palabra)
            else:
                if self._tipo in tipo_palabra:   #Tipo seria un string que le se asigna aleatoreamente el tipo de una lista donde esta "NN" "JJ" y "VB"
                    valido = True
        #if (valido):  # le agregue else "" porque sino daba error porque retornaba None cuando no encontraba
            return palabra.upper() if valido else ""
            
    def _mapear_tablero(self,posiciones_ocupadas_tablero, long_tablero):
        """ Esta funcion recibe las posiciones ocupadas en el tablero, mapea lugares disponibles y los devuelve
            en un diccionario long_y_posiciones cuyas claves son la longitud del lugar disponible y valores son
            listas con listas de las posiciones disponibles para esas longitudes 
        """
        long_y_posiciones = dict()
        for i in range(long_tablero):
            j = 0
            while j < long_tablero:
                cant = 0
                posiciones = []
                while not (i,j) in posiciones_ocupadas_tablero and j < long_tablero:
                    cant += 1
                    posiciones.append((i,j))
                    j += 1
                if cant >= 2: 
                    if not cant in long_y_posiciones.keys():
                        long_y_posiciones[cant] = [posiciones]
                    else:
                        long_y_posiciones[cant].append(posiciones)

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

    def _recursividadPalabras(self,lista,long_max,palabra,lista_palabras):
        """
        Agrega a lista_palabras las palabras que considera validas formadas por elementos de lista
        """
        for elem in lista:
            #print("ELEMENTOOOOOO: ",elem)
            palabra = palabra + elem
            if len(palabra) > 1 and not palabra in lista_palabras and self._tiene_vocales(palabra) and self._tiene_consonantes(palabra) and es.palabra_valida(palabra):
                lista_palabras.append(palabra)
            lista_reducida =  lista.copy()
            lista_reducida.remove(elem)
            self._recursividadPalabras(lista_reducida, long_max, palabra, lista_palabras)
            palabra = palabra[:len(palabra)-1]
 
    def jugar(self,window,posiciones_ocupadas_tablero):
        long_y_posiciones = self._mapear_tablero(posiciones_ocupadas_tablero,self.long_tablero) # obtenemos las posiciones libres en el tablero
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
                window[long_y_posiciones[long_max_tablero][posiciones_random][i]].update(mejor_palabra[i-inicio_columna], disabled=True) # agregamos las letras al tablero
                # guardamos las posiciones y las letras de la palabra en palabra_nueva así despues sumamos los puntos
                palabra_nueva[long_y_posiciones[long_max_tablero][posiciones_random][i]] = mejor_palabra[i-inicio_columna]                
        
            ## llamamos a la funcion sumar_puntos de la clase padre y actualizamos los puntos:
            # self.sumPuntos(sumar_puntos(puntos_por_letra, botones, palabra_nueva)) comentada hasta formar la clase padre
            # window['p_pc'].update("Puntos PC:"+str(self.getPuntos())) # aca se actualizaria la ventana
            ## actualizamos las fichas de la pc:
            print("MEJOR PALABRA",mejor_palabra)
            self.reinicioFichas(mejor_palabra)             

        else:
            sg.popup("La PC le ha pasado el turno")


    puntos = property(getPuntos,sumPuntos,doc="Setters y getters")