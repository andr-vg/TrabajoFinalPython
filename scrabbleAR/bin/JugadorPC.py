import PySimpleGUI as sg
import random
import json
from Jugadores import Jugadores
import os
import GameConfigManager as cm
absolute_path = os.path.join(os.path.dirname(__file__), '..')

class PC(Jugadores):
    '''
    Clase PC
        
        Abstraccion de la computadora jugando, subclase de Jugadores
        
        Metodos
        ---
        
        _input_palabra(lista:list)

            Formatea la lista de palabras usadas para una mejor visualizacion en el componente
            InputCombo
        
        _cargar_palabras_usadas(window:sg.Window)
        
            Recibe la ventana del juego y carga las palabras usadas en el componente 
            InputCombo (se usa al cargar una partida)
        
        reinicioFichas(palabra)
            
            palabra: string
            
            Reinicia los valores de las fichas usadas para luego ser actualizados
            por nuevos valores en la bolsa
        
        _convertirJson

            Parsea el diccionario de botones para poder guardarlo en un
            Json
            
        _convertirDic(botones)
        
            botones: dict

            Le da forma al diccionario de botones cargado del Json
            
        convertir_lista_tupla
        
            Convierte la lista de listas a tuplas para las pos ocupadas del tablero
            
        guardar_estado

            Guarda el estado interno del jugadorPc en un json
                (se usa al posponer la partida)
                
        _cargar_estado(window)

            window: sg.Window
            
            Carga los datos del json en caso de empezar una partida guardada
        
        _obtenerPalabra(long_max)

            long_max: integer ---> long max de la palabra
            
            Itera combinaciones de fichas hasta formar una palabra valida
            
        _mapeoHorizontal(i,j)
                
                i -> filas
                j -> columnas
                
                Mapea el tablero y devuelve un diccionario de posiciones libres en el tablero
            
        _mapeoVertical
            
            Misma funcion de _mapeoHorizontal pero en posiciones verticales
            
         _agrego_posiciones
         
            Agregamos a long_y_posiciones las posiciones libres encontradas de longitud >=2
            En nivel medio -> tambien agregamos a una lista las posiciones con al menos un casillero premio
            En nivel dificil -> tambien agregamos a un dic las posiciones con al menos un casillero premio
            donde la clave es la cant de casilleros premio que tenga esa pos.
        
        _mapear_tablero
        
            Esta funcion recibe las posiciones ocupadas en el tablero, mapea lugares disponibles y los devuelve
            en un diccionario long_y_posiciones cuyas claves son la longitud del lugar disponible y valores son
            listas con listas de las posiciones disponibles para esas longitudes 
        
        _calcular_long_maxima(long_max_tablero,cant_fichas)

            Esta funcion retorna la longitud maxima segun dos cosas: la cantidad de fichas disponibles
            y el mayor numero de casilleros contiguos libres en el tablero. Tenemos dos casos:
            - si el nro de casilleros supera o es igual a la cant de fichas, con mandarle la cant de fichas
            que tengo le basta.
            - si el nro de casilleros es menor que la cantidad de fichas: ahi la palabra a formar tiene que ocupar
            como maximo esos casilleros, asique le mando ese valor
        
        _actualizar_tablero(window, posiciones_finales, mejor_palabra):

                window: sg.Window
                posiciones_finales: dict
                mejor_palabra:string ---> palabra final

                Pone las fichas en el tablero y actualiza la lista de palabras usadas
        
        _mapeo_y_palabra

            Realiza el mapeo en todo el tablero y
            devuelve la palabra obtenida y las posiciones
            
        _turno_medio
        
            nivel medio: se asegura de que las posiciones contengan al menos
            un casillero premio, se queda con el primero que encuentre
            
        _turno_dificil
        
            nivel dificil: realiza un filtrado más fino asegurandose 
            de devolver las posiciones con el mejor casillero premio posible
        
        _turno_random
        
            nivel facil o no encontro posiciones con casilleros premio: retorna posiciones aleatorias
            
        jugar
        
            Jugada del usuario: se forma la palabra más larga posible según la dificultad.
            Se mapea el tablero para obtener las posiciones libres donde puede ubicarse la palabra obtenida.
            
            Dificultad facil: Se obtiene una lista de posiciones aleatoria en la que entre en la palabra.
                          -- > Por el momento implementamos esta dificultad para los tres niveles.
                          
            Dificultad media: Se obtiene una lista de posiciones con al menos un casillero premio (de ser posible)
                          y la palabra más larga que quepe en esas posiciones. --> falta implementar 
                          
            Dificultad dificil: Se obtiene una lista con las posiciones que sumen más puntos, la palabra que sume 
                            más puntos y quepa ahí, y se ubica la letra de mayor puntaje en alguna casillero 
                            premio (de ser posible) --> falta implementar
    '''
    def __init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo, guardada,window):
        Jugadores.__init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo)
        self._palabras_usadas = []
        self._posiciones_ocupadas_tablero = []
        self._colores = cm.cargar_colores()
        if (guardada):
            self._cargar_estado(window)
            self._cargar_palabras_usadas(window)
# ---------------------------------------------------------------------
    def _input_palabra(self,lista):
        """
        Formatea la lista para el InputCombo
        """
        lista_final = list()
        for pal in lista:
            lista_final.append(pal.replace("\n",""))
        return lista_final

    def _cargar_palabras_usadas(self,window):
        """
        Carga las palabras usadas en el InputCombo de la pc
        """
        pal_final = self._input_palabra(self._palabras_usadas)
        lista_pal = [] if self._palabras_usadas == [] else self._palabras_usadas[0]
        window["-palpc-"].update(lista_pal, pal_final)

# ---------------------------------------------------------------------
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
# ---------------------------------------------------------------------   
    def actualiza_botones(self,botones):
        """
        Actualiza el diccionario botones con las pos usadas por el usuario
        """
        self._botones = botones
# ---------------------------------------------------------------------
    def _convertirJson(self):
        """
        Parsea el Json para poder guardarlo
        """
        dic_aux = {}
        for clave,valor in self._botones.items():
            dic_aux[str(clave[0])+","+str(clave[1])] = valor        
        return dic_aux
# ---------------------------------------------------------------------   
    def _convertirDic(self,botones):
        """
        Vuelve a darle formato al diccionario de botones
        """
        dic_aux = {}
        for clave,valor in botones.items():
            dic_aux[tuple(map(int,clave.split(",")))] = valor  
        return dic_aux
# ---------------------------------------------------------------------
    def convertir_lista_tupla(self,lista):
        """
        Convierte la lista de listas a tuplas para las pos ocupadas del tablero
        """
        lista_final = []
        for pos in lista:
            aux = (pos[0], pos[1]) 
            lista_final.append(aux)
        return lista_final
# ---------------------------------------------------------------------
    def guardar_estado(self):
        """
        Guarda el estado interno del jugador PC
        """
        arch = open(os.path.join(absolute_path, "lib","info","saves","datos_pc.json"), "w",encoding='utf8')
        datos = {"fichas":self.fichas,"botones":self._convertirJson(),"palabras_usadas":self._palabras_usadas,"pos_usadas":self._posiciones_ocupadas_tablero}
        json.dump(datos,arch,indent = 4,ensure_ascii=False)
        arch.close()
# ----------------------------------------------------------------------
    def _cargar_estado(self,window):
        """
        Si la partida esta guardada carga el estado guardado en un json
        """
        try:
            datos = open(os.path.join(absolute_path, "lib","info","saves","datos_pc.json"), "r",encoding='utf8')
            data = {}
            data = json.load(datos)
            self._botones = self._convertirDic(data["botones"])
            self._palabras_usadas = data["palabras_usadas"]
            self._posiciones_ocupadas_tablero = self.convertir_lista_tupla(data["pos_usadas"])
        except (FileNotFoundError):
            sg.Popup('No se encontro el archivo datos_pc.json, Inicie otra partida',title='Error')
            from Menu import main as sg_main
            window.close()
            sg_main()
            
# ----------------------------------------------------------------------
    def _obtenerPalabra(self, long_max):
        """
        obtiene una palabra a partir de las _fichas
        """
        import itertools as it
        from pattern.text.es import verbs, spelling, lexicon, parse
        
        letras = ""
        for letra in self.fichas.values():
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
                        if evaluation in s and evaluation in le and not evaluation.upper() in self._palabras_usadas:
                            l.append(evaluation)

        l = list(set(l))
        valido = False
        hay_palabras = True
        while not valido and hay_palabras:
            try:
                palabra = max(l, key=lambda x: len(x))
                l.remove(palabra)
            except:  # caso en que la lista no tiene palabras
                palabra = ""
                hay_palabras = False      
            if not palabra.upper() in self._palabras_usadas: # no puede formar palabras que ya formo antes
                valido = self.es_palabra_valida(palabra)            
        if valido:
            self._palabras_usadas.append(palabra.upper())
        return palabra.upper() if valido else ""
# ----------------------------------------------------------------------
    def _mapeoHorizontal(self, i, j):
        """
        Mapeamos el tablero fila por fila y agregamos las posiciones libres encontradas
        """
        cant = 0
        posiciones = []
        while not (i, j) in self._posiciones_ocupadas_tablero and j < self.long_tablero:
            cant += 1
            posiciones.append((i, j))
            j += 1
        return cant, posiciones
# ----------------------------------------------------------------------
    def get_pos_tablero(self):
        """
        Retorna las pos usadas del tablero
        """
        return self._posiciones_ocupadas_tablero
# ----------------------------------------------------------------------
    def actualizar_pos_tablero(self,list_pos):
        """
        Actualiza las pos usadas del tablero
        """
        self.posiciones_ocupadas_tablero = list_pos
# ----------------------------------------------------------------------
    def _mapeoVertical(self, i, j):
        """
        Mapeamos el tablero columna por columna y agregamos las posiciones libres encontradas
        """
        cant = 0
        posiciones = []
        while not (j, i) in self._posiciones_ocupadas_tablero and j < self.long_tablero:
            cant += 1
            posiciones.append((j, i))
            j += 1
        return cant, posiciones
# ----------------------------------------------------------------------
    def _agrego_posiciones(self, cant, posiciones, long_y_posiciones, mejores_posiciones, mejores_posiciones_dificil):
        """
        Agregamos a long_y_posiciones las posiciones libres encontradas de longitud >=2
        En nivel medio -> tambien agregamos a una lista las posiciones con al menos un casillero premio
        En nivel dificil -> tambien agregamos a un dic las posiciones con al menos un casillero premio
        donde la clave es la cant de casilleros premio que tenga esa pos.
        """
        if cant >= 2:
            if not cant in long_y_posiciones.keys():
                long_y_posiciones[cant] = [posiciones]
            else:
                long_y_posiciones[cant].append(posiciones)
            if self._dificultad == "medio":
                for pos in posiciones:
                    if self._botones[pos] == "++++" or self._botones[pos] == "+++" or self._botones[pos] == "++" or self._botones[pos] == "+":
                        mejores_posiciones.append(posiciones)
                        break
            elif self._dificultad == "dificil":
                cant_pos_premio = 0
                for pos in posiciones:
                    if self._botones[pos] == "++++" or self._botones[pos] == "++" or self._botones[pos] == "++" or self._botones[pos] == "++":
                        cant_pos_premio += 1
                if cant_pos_premio > 0: 
                    if not cant_pos_premio in mejores_posiciones_dificil.keys():
                        mejores_posiciones_dificil[cant_pos_premio] = [posiciones]
                    else:
                        mejores_posiciones_dificil[cant_pos_premio].append(posiciones)
# ----------------------------------------------------------------------
    def _mapear_tablero(self):
        """ 
        Esta funcion recibe las posiciones ocupadas en el tablero, mapea lugares disponibles y los devuelve
        en un diccionario long_y_posiciones cuyas claves son la longitud del lugar disponible y valores son
        listas con listas de las posiciones disponibles para esas longitudes 
        """
        long_y_posiciones = dict()
        mejores_posiciones = []
        mejores_posiciones_dificil = dict()
        for i in range(self.long_tablero):
            j = 0
            while j < self.long_tablero:
                cant, posiciones = self._mapeoHorizontal(i, j)  # mapeo horizontalmente
                self._agrego_posiciones(cant, posiciones, long_y_posiciones, mejores_posiciones, mejores_posiciones_dificil)
                cant, posiciones = self._mapeoVertical(j, i)  # mapeo verticalmente
                self._agrego_posiciones(cant, posiciones, long_y_posiciones, mejores_posiciones, mejores_posiciones_dificil)
                j += 1
        return long_y_posiciones, mejores_posiciones, mejores_posiciones_dificil
# ---------------------------------------------------------------------
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
# ---------------------------------------------------------------------
    def _actualizar_tablero(self, window, posiciones_finales, mejor_palabra):
        """
        Pone las fichas en el tablero y actualiza la lista de palabras usadas
        """
        palabra_nueva = dict()
        letra = 0
        window['-palpc-'].update(self._palabras_usadas[0],self._input_palabra(self._palabras_usadas))
        for pos in posiciones_finales:
            self._posiciones_ocupadas_tablero.append(pos)
            window[pos].update(mejor_palabra[letra], disabled=True,button_color=("black",self._colores["letra_pc"])) 
            palabra_nueva[pos] = mejor_palabra[letra]
            self._botones[pos] = mejor_palabra[letra] + "*"
            letra += 1
        return palabra_nueva
# ---------------------------------------------------------------------  
    def get_botones(self):
        """
        Devuelve el diccionario botones para el guardado de la partida
        """
        return self._botones
# ---------------------------------------------------------------------
    def _primer_turno(self, window):
        """
        Realiza el primer turno de la pc
        """

        long_max = len(self.fichas.values())
        mejor_palabra = self._obtenerPalabra(long_max)  # obtenemos la mejor palabra posible

        # momento de ubicar la mejor palabra obtenida
        if mejor_palabra != "":  # caso en que encuentra una palabra valida    
            ## primer turno de la compu: ubicamos la palabra en el centro del tablero
            primer_turno = False
            palabra_nueva = dict()
            centro = self.long_tablero // 2
            indice_letra_centro = random.randint(0, len(mejor_palabra) - 1)
            orientacion = random.randint(0, 1)  ## orientacion = 1 : vertical, 0: horizontal
            # antes del centro
            for i in range(centro - indice_letra_centro, centro):  
                pos = (centro, i) if orientacion == 0 else (i, centro)
                self._posiciones_ocupadas_tablero.append(pos)
                window[pos].update(mejor_palabra[indice_letra_centro - (centro - i)], disabled=True,
                                   button_color=("black", self._colores["letra_pc"]))  # agregamos las letras al tablero
                self._botones[pos] = mejor_palabra[indice_letra_centro - (centro - i)] + "*"
                palabra_nueva[pos] = mejor_palabra[indice_letra_centro - (centro - i)]
            # agregamos el centro
            self._posiciones_ocupadas_tablero.append((centro, centro))  
            window[(centro, centro)].update(mejor_palabra[indice_letra_centro], disabled=True,
                                        button_color=("black",self._colores["letra_pc"]))  # agregamos las letras al tablero
            self._botones[(centro,centro)] = mejor_palabra[indice_letra_centro] + "*"
            palabra_nueva[(centro, centro)] = mejor_palabra[indice_letra_centro]
            # despues del centro
            for i in range(centro + 1, centro + len(mejor_palabra) - indice_letra_centro): 
                pos = (centro, i) if orientacion == 0 else (i, centro)    
                self._posiciones_ocupadas_tablero.append(pos)
                window[pos].update(mejor_palabra[indice_letra_centro + i - centro], disabled=True,
                                   button_color = ("black", self._colores["letra_pc"]))  # agregamos las letras al tablero
                self._botones[pos] = mejor_palabra[indice_letra_centro + i - centro] + "*"
                palabra_nueva[pos] = mejor_palabra[indice_letra_centro + i - centro]
                    

            ## actualizamos tablero fichas y puntos:
            self._calculamos_puntos(palabra_nueva, mejor_palabra, window)
            window["-palpc-"].update(self._palabras_usadas[0],self._input_palabra(self._palabras_usadas))     

        else:
            self._pasar_turno()
            primer_turno = True
            
        return primer_turno
# ---------------------------------------------------------------------
    def _mapeo_y_palabra(self):
        """
        Realiza el mapeo en todo el tablero y
        devuelve la palabra obtenida y las posiciones
        """
        # obtenemos las posiciones libres en el tablero
        long_y_posiciones, mejores_posiciones, mejores_posiciones_dificil = self._mapear_tablero()          
        if self._dificultad == "medio" and len(mejores_posiciones) > 0:
            # ordenamos las posiciones por su long de casilleros de mayor a menor
            posiciones = sorted(mejores_posiciones, key=lambda x: len(x), reverse=True)[0] # posiciones con las que nos quedaremos del tablero
            long_max_tablero = len(posiciones)
            opcion = "medio"
        elif self._dificultad == "dificil" and len(mejores_posiciones_dificil.values()) > 0:
            cant_casilleros_premio_max = max(mejores_posiciones_dificil.keys()) # filtramos las posiciones con mayor cant de casillas premio
            # nos quedamos con las posiciones con mayor cant de casilleros dentro de los que tienen mayor cant de casillas premios
            posiciones = sorted(mejores_posiciones_dificil[cant_casilleros_premio_max], key=lambda x: len(x), reverse=True)[0]
            opcion = "dificil"
            long_max_tablero = len(posiciones)
        else:
            long_max_tablero = max(long_y_posiciones.keys())  # calculamos la long maxima entre todas esas posiciones libres    
            opcion = "random"
            posiciones = long_y_posiciones # en este caso en vez de retornar una lista de pos retorna un diccionario con todas las que encontro
        # nos quedamos con la long max entre casillas y cant fichas  
        long_max = self._calcular_long_maxima(long_max_tablero, 7)    
        # obtenemos la mejor palabra posible
        mejor_palabra = self._obtenerPalabra(long_max)  
        return posiciones, long_max_tablero, mejor_palabra, opcion
# ---------------------------------------------------------------------
    def _turno_medio(self, posiciones, mejor_palabra):
        """
        nivel medio: se asegura de que las posiciones contengan al menos
        un casillero premio, se queda con el primero que encuentre
        """
        posiciones_finales = []
        contiene_premio = False  # las posiciones a ocupar tienen que incluir la casilla premio
        for i in range(len(posiciones)-len(mejor_palabra)+1):
            inicio = i
            fin = i + len(mejor_palabra) - 1
            posiciones_finales = posiciones[inicio:fin+1]
            for pos in posiciones_finales:
                if self._botones[pos] in ("++++","+++","++","+"):
                    contiene_premio = True
                    break
            if contiene_premio:
                break
        return posiciones_finales
# ---------------------------------------------------------------------
    def _turno_dificil(self, posiciones, mejor_palabra):
        """
        nivel dificil: realiza un filtrado más fino asegurandose 
        de devolver las posiciones con el mejor casillero premio posible
        """
        posiciones_finales_pal  = []
        pos_premio_letra = -1
        encontro_el_mejor_1 = encontro_el_mejor_2 = False
        # realizamos un primer filtrado buscando casilleros premio 
        for i in range(len(posiciones)-len(mejor_palabra)+1):
            inicio = i
            fin = i + len(mejor_palabra) - 1
            posiciones_finales = posiciones[inicio:fin+1]
            indice_lista_posiciones = 0
            for pos in posiciones_finales:
                if self._botones[pos] == "++++": # nos guardamos las posiciones que contienen una que duplica o triplica palabra
                    encontro_el_mejor_1 = True
                    posiciones_finales_pal = posiciones_finales
                    break
                elif self._botones[pos] == "+++" and len(posiciones_finales_pal)==0:
                    encontro_el_mejor_1 = True
                    posiciones_finales_pal = posiciones_finales
                    break
                elif self._botones[pos] == "++": # nos guardamos la pos que contienen una que duplique o triplique el valor de la letra
                    encontro_el_mejor_2 = True
                    pos_premio_letra = indice_lista_posiciones
                elif self._botones[pos] == "+" and pos_premio_letra == -1:
                    pos_premio_letra = indice_lista_posiciones
                indice_lista_posiciones += 1
            # si ademas de posiciones que tripliquen/dupliquen puntos encuentra
            # una que triplica/duplica alguna letra corta la busqueda
            if encontro_el_mejor_1 and encontro_el_mejor_2:
                break
        # nos guardamos los puntos actuales por si hay que comparar    
        puntos_actuales = self.getPuntos()
        # calculemos puntaje y posiciones alrededor
        # si encontro casillero que duplique letra
        if pos_premio_letra != -1:
            max_ptos = 0
            max_i = 0
            # veamos qué letra tiene mayor puntaje
            for i in range(len(mejor_palabra)):
                if self.puntos_por_letra[mejor_palabra[i]] > max_ptos:
                    max_ptos = self.puntos_por_letra[mejor_palabra[i]]
                    max_i = i
            # veamos si la palabra entra ubicando la mejor letra ahi
            inicio = pos_premio_letra - len(mejor_palabra[:max_i])
            fin = pos_premio_letra + len(mejor_palabra[max_i+1:])
            if inicio >= 0 and fin < len(posiciones):
                palabra_nueva = dict()
                j = 0
                for i in range(inicio, fin+1):
                    palabra_nueva[posiciones[i]] = mejor_palabra[j]
                    j += 1
                self.sumar_puntos(palabra_nueva)
                puntos_con_mejor_letra = self.getPuntos()
                self.setPuntos(puntos_actuales)
            else:
                puntos_con_mejor_letra = 0
                pos_premio_letra = 0        

        # calculemos puntaje si encontro casillero que duplique/triplique palabra
        if len(posiciones_finales_pal) > 0:
            palabra_nueva = dict()
            j = 0
            for pos in posiciones_finales_pal:
                palabra_nueva[pos] = mejor_palabra[j]
                j += 1
            self.sumar_puntos(palabra_nueva)
            puntos_con_mejor_pal = self.getPuntos()
            self.setPuntos(puntos_actuales)
                    
        # en caso de haber encontrado ambos tipos de casilleros nos quedamos con el mejor
        if pos_premio_letra != -1 and len(posiciones_finales_pal) > 0:
            if puntos_con_mejor_letra > puntos_con_mejor_pal:
                posiciones_finales = posiciones[inicio:fin+1]
            else:
                posiciones_finales = posiciones_finales_pal
        # caso en que solo encontramos casillero que duplique/triplique letra
        elif pos_premio_letra != -1:
            posiciones_finales = posiciones[inicio:fin+1]
        elif (pos_premio_letra == 0):
            posiciones_finales = posiciones[0:len(mejor_palabra)] 
        # caso en que solo encontramos casillero que duplique/triplique palabra
        else:
            posiciones_finales = posiciones_finales_pal
        return posiciones_finales
# ---------------------------------------------------------------------
    def _turno_random(self, long_y_posiciones, mejor_palabra, long_max_tablero):
        """ 
        nivel facil o no encontro posiciones con casilleros premio: retorna posiciones aleatorias
        """
        # me quedo con una lista de posiciones valida
        posiciones_random = random.randint(0, len(long_y_posiciones[long_max_tablero]) - 1)  
        inicio = random.randint(0, (long_max_tablero - len(mejor_palabra)))
        fin = inicio + len(mejor_palabra)
        posiciones_finales = long_y_posiciones[long_max_tablero][posiciones_random][inicio:fin]
        return posiciones_finales
# ---------------------------------------------------------------------
    def _calculamos_puntos(self, palabra_nueva, mejor_palabra, window):
        """ 
        llamamos a la funcion sumar_puntos de la clase padre y actualizamos los puntos:
        """
        self.sumar_puntos(palabra_nueva)
        ## actualizamos las fichas de la pc:        
        self.reinicioFichas(mejor_palabra)
        ## se actualizan los puntos         
        window["p_pc"].update(str(self.getPuntos())) 
# ---------------------------------------------------------------------
    def _pasar_turno(self):
        sg.popup_no_border("La PC le ha pasado el turno",keep_on_top=True)
        letras = ""
        self.reinicioFichas(letras.join(self.fichas.values()))
# ---------------------------------------------------------------------
    def jugar(self, window, primer_turno):
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
        fichas_a_devolver_a_bolsa = ''
        if primer_turno:
            primer_turno = self._primer_turno(window)
        else:
            posiciones, long_max_tablero, mejor_palabra, opcion = self._mapeo_y_palabra()
            # momento de ubicar la mejor palabra obtenida
            if mejor_palabra != "": # caso en que encuentra una palabra valida
                if opcion == "medio":
                    posiciones_finales = self._turno_medio(posiciones, mejor_palabra)
                elif opcion == "dificil":
                    posiciones_finales = self._turno_dificil(posiciones, mejor_palabra)
                else:
                    posiciones_finales = self._turno_random(posiciones, mejor_palabra, long_max_tablero)
                # agregamos las letras al tablero
                palabra_nueva = self._actualizar_tablero(window, posiciones_finales, mejor_palabra)
                ## actualizamos fichas y puntos:
                self._calculamos_puntos(palabra_nueva, mejor_palabra, window)
            else:
                fichas_a_devolver_a_bolsa = self.fichas.copy()
                self._pasar_turno()
        return primer_turno, fichas_a_devolver_a_bolsa