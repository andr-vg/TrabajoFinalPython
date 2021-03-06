import PySimpleGUI as sg
from Jugadores import Jugadores
import os
import json
absolute_path = os.path.join(os.path.dirname(__file__), '..')

class Jugador(Jugadores):
    '''
    Clase Jugador

       Abstraccion de un jugador, subclase de Jugadores
        
    Metodos
    ---
    
    _input_palabra(lista:list)

        Formatea la lista de palabras usadas para una mejor visualizacion en el componente
        InputCombo
        
    _cargar_palabras_usadas(window:sg.Window)
    
        Recibe la ventana del juego y carga las palabras usadas en el componente 
        InputCombo (se usa al cargar una partida)
        
    _guardar_fichas
    
        Guarda en un Json las fichas del jugador
            clave -> pos en el atril 
             valor -> letra

    guardar_info

        Guarda en un Json la lista de palabras que logro formar el jugador
        
    _cargar_datos
    
        Carga la lista de palabras formadas del jugador
            (se usa al cargar una partida guardada)
            
    _analizo(keys_ordenados,menor_1,menor_2,j,k)

        Analiza si las posiciones ocupadas fueron contiguas y sobre la misma columna
        o fila
        menor_1 = fila_menor o columna menor
        
        menor_2 = columna_menor (caso horizontal) o fila_menor (caso vertical)
    
        k = 1 si es la columna (horizontal) o 0 si es la fila (vertical)
    
    _esta_en_el_centro(keys_ordenados)

        keys_ordenados: dict

        Retorna si la posicion del centro fue ocupada en el primer turno

    jugar(palabra_nueva,letras_usadas,posiciones_ocupadas_tablero,primer_turno)
        
        palabra_nueva: string
        letras_usadas: dict
        posiciones_ocupadas_tablero: dict
        primer_turno: boolean
        
        Jugada del usuario: analiza si la palabra fue colocada de forma correcta 
        y si esta incluida en pattern
    


    '''
    def __init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo, guardado, window):
        Jugadores.__init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo)
        if(guardado):
            self._cargar_datos(window)
            self._cargar_palabras_usadas(window)
        else:
            self._palabras_usadas = []

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
        Carga las palabras usadas en el InputCombo
        """
        pal_final = self._input_palabra(self._palabras_usadas)
        lista_pal = [] if self._palabras_usadas == [] else self._palabras_usadas[0] 
        window["-pal-"].update(lista_pal, pal_final)

    def _guardar_fichas(self):
        """
        Guarda las fichas del jugador en .json
        """
        fichas = open(os.path.join(absolute_path,"lib","info","saves","fichas_jugador.json"),"w")
        json.dump(self.fichas,fichas)

    def guardar_info(self):
        """
        Guarda la lista de palabras que formo el jugador
        """
        self._guardar_fichas()
        datos = open(os.path.join(absolute_path, "lib","info","saves","palabras_jugador.json"),"w",encoding='utf8')
        json.dump(self._palabras_usadas,datos,ensure_ascii=False)

    def get_palabras_usadas(self):
        """
        Retorna lista de palabras usadas
        """
        return self._palabras_usadas

    def _cargar_datos(self,window):
        """
        Carga la lista de palabras usadas por el jugador
        """
        try:
            datos = open(os.path.join(absolute_path, "lib","info","saves","palabras_jugador.json"),"r",encoding='utf8')
            self._palabras_usadas = list(json.load(datos))
        except (FileNotFoundError):
            from Menu import main as sc_main
            sg.popup('No se encontro archivo palabras_jugador.json, inicie otra partida.',title='Error')
            window.close()
            sc_main()

    def _analizo(self, keys_ordenados, menor_1, menor_2, j,
                 k):  # menor_1 = fila_menor (caso horizontal) o columna_menor (caso vertical)
        """
        Retorna si las posiciones ocupadas fueron contiguas y sobre la misma columna/fila o no
        """
        for i in range(1,
                       len(keys_ordenados)):  # menor_2 = columna_menor (caso horizontal) o fila_menor (caso vertical)
            if keys_ordenados[i][j] != menor_1:  # j = 0 si es la fila (horizontal) o 1 si es columna (vertical)
                return False  # aca comparamos las filas/columnas de cada letra con la de la primera
            if keys_ordenados[i][k] - i != menor_2:  # k = 1 si es la columna (horizontal) o 0 si es la fila (vertical)
                return False  # si son contiguas, la resta de las mayores columnas/filas - i siempre es igual a la de la menor
        return True

    def _estan_en_el_centro(self, keys_ordenados):
        """
        Retorna si la posicion del centro fue ocupada en el primer turno del usuario
        """
        centro = self.long_tablero // 2
        if (centro, centro) in keys_ordenados:
            return True
        else:
            return False

    def jugar(self, palabra_nueva, letras_usadas, posiciones_ocupadas_tablero,
              primer_turno):
        """
        Jugada del usuario: se analiza si la palabra fue puesta de forma correcta y si
        está incluida en pattern, según la dificultad.
        """
        keys_ordenados = sorted(palabra_nueva.keys())  # los ordeno por columna de menor a mayor
        columna_menor = keys_ordenados[0][1]  # me guarda la columna mas chica con la cual voy a hacer una comparacion
        fila_menor = keys_ordenados[0][0]  # me guardo la primer fila para compararla con las otras a ver si son iguales
        actualizar_juego = False
        # ahora analizamos si es valida o no:
        if not self._analizo(keys_ordenados, fila_menor, columna_menor, 0, 1) and not self._analizo(keys_ordenados,
                                                                                                    columna_menor,
                                                                                                    fila_menor, 1, 0):
            sg.popup_ok('Palabra no válida, por favor ingrese en forma horizontal o vertical',keep_on_top=True)
        else:
            lista_letras_ordenadas = []
            for key in keys_ordenados:
                lista_letras_ordenadas.append(palabra_nueva[key])
            palabra_obtenida = ''.join(lista_letras_ordenadas)
            palabra_obtenida.strip()
            if self.es_palabra_valida(palabra_obtenida) and not(palabra_obtenida in self._palabras_usadas):
                al_centro = self._estan_en_el_centro(keys_ordenados)
                if (not primer_turno) or (primer_turno and al_centro):
                    self._palabras_usadas.append(palabra_obtenida)
                    posiciones_ocupadas_tablero.extend(palabra_nueva.keys())
                    ## funcion que suma los puntos por letra y segun cada boton duplica o resta puntos:
                    puntos_sumados = self.sumar_puntos(palabra_nueva)                    
                    sg.popup_timed(f'Sumaste {puntos_sumados} puntos!',auto_close_duration=3,no_titlebar=True,keep_on_top=True)
                    actualizar_juego = True  # con esto despues se actualiza la ventana
                    for k in letras_usadas.keys():  # saco fichas de la bolsa para ponerlas en letras
                        self.fichas[k] = ""
                elif primer_turno and not al_centro:
                    sg.popup('La primer palabra debe ir en el centro',keep_on_top=True)
            else:
                sg.popup_ok('Palabra no válida, por favor ingrese otra',keep_on_top=True)

        return letras_usadas, palabra_nueva, actualizar_juego, posiciones_ocupadas_tablero, self._palabras_usadas
