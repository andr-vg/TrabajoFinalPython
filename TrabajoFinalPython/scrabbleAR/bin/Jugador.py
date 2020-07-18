import PySimpleGUI as sg
from Jugadores import Jugadores
import os
import json
absolute_path = os.path.join(os.path.dirname(__file__), '..')
# ----------------------------------------------------------------------
#Clase Jugador
# ----------------------------------------------------------------------

class Jugador(Jugadores):
    def __init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo, guardado):
        Jugadores.__init__(self, fichas, long_tablero, botones, puntos_por_letra, dificultad, tipo)
        if(guardado):
            self._cargar_datos()
        else:
            self._palabras_usadas = []

    def guardar_info(self):
        """
        Guarda la lista de palabras que formo el jugador
        """
        datos = open(os.path.join(absolute_path, "lib","info","saves","palabras_jugador.json"),"w")
        json.dump(self._palabras_usadas,datos)

    def _cargar_datos(self):
        """
        Carga la lista de palabras usadas por el jugador
        """
        try:
            datos = open(os.path.join(absolute_path, "lib","info","saves","palabras_jugador.json"),"r")
            self._palabras_usadas = json.load(datos)
        except (FileNotFoundError):
            sg.popup("No se encontro archivo con palabras del usuario",keep_on_top=True)
            self._palabras_usadas = []


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
                self._palabras_usadas.append(palabra_obtenida)
                al_centro = self._estan_en_el_centro(keys_ordenados)
                if (not primer_turno) or (primer_turno and al_centro):
                    posiciones_ocupadas_tablero.extend(palabra_nueva.keys())
                    ## funcion que suma los puntos por letra y segun cada boton duplica o resta puntos:
                    self.sumar_puntos(palabra_nueva)
                    actualizar_juego = True  # con esto despues se actualiza la ventana
                    for k in letras_usadas.keys():  # saco fichas de la bolsa para ponerlas en letras
                        self.fichas[k] = ""
                elif primer_turno and not al_centro:
                    sg.popup('La primer palabra debe ir en el centro',keep_on_top=True)
            else:
                sg.popup_ok('Palabra no válida, por favor ingrese otra',keep_on_top=True)

        return letras_usadas, palabra_nueva, actualizar_juego, posiciones_ocupadas_tablero, self._palabras_usadas
