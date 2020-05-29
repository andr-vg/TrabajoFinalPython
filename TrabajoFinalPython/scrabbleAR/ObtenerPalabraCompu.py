import PySimpleGUI as sg

def obtener_palabra_compu(fichas, long_max):
    """
    Esta funcion recibe una lista de fichas de la compu, la longitud maxima que puede tener
    la palabra, y retorna una palabra valida para esos parametros.
    """
    import IdentificarPalabra as es

    def tiene_vocales(palabra):
        for letra in palabra:
            if letra in 'aeiou':
                return True
        return False        

    def tiene_consonantes(palabra):
        for letra in palabra:
            if not letra in 'aeiou':
                return True
        return False

    def recursividadPalabras(lista, long_max, palabra, lista_palabras):
        """
        Agrega a lista_palabras las palabras que considera validas formadas por elementos de lista
        """
        for elem in lista:
            palabra = palabra + elem # agrego letra a letra 
            if len(palabra) <= long_max:  # solo analizo las palabras que caben en las casillas disponibles
                if len(palabra) > 1 and not palabra in lista_palabras and tiene_vocales(palabra) and tiene_consonantes(palabra) and es.palabra_valida(palabra):
                    lista_palabras.append(palabra) 
                lista_reducida = lista.copy()
                lista_reducida.remove(elem)
                recursividadPalabras(lista_reducida, long_max, palabra, lista_palabras) # la recursividad corta cuando llega a una lista reducida vacia       
                palabra = palabra[:len(palabra)-1] # voy eliminando la ultima letra
    
    palabra = '' # inicialmente no tenemos caracteres 
    lista_palabras = [] # aca almacenaremos las palabras que la compu vaya encontrando entre todas las permutaciones
    recursividadPalabras(fichas, long_max, palabra, lista_palabras)
    print(lista_palabras) 
    return '' if len(lista_palabras) == 0 else max(lista_palabras) # retornamos la mejor palabra o '' si no formo ninguna

def mapear_tablero(posiciones_ocupadas_tablero, long_tablero):
    """ Esta funcion recibe las posiciones ocupadas en el tablero, mapea lugares disponibles y los devuelve
        en un diccionario long_y_posiciones cuyas claves son la longitud del lugar disponible y valores son
        listas con las posiciones disponibles de esas longitudes
        Observar que el diccionario solo se queda con las primeras longitudes que encuentre, es decir,
        si la fila i tiene 2 zonas con 3 lugares disponibles, se queda con la primera. Lo mismo por filas. 
    """
    long_y_posiciones = dict()
    for i in range(long_tablero):
        j = 0
        while j < long_tablero:
            if not (i,j) in posiciones_ocupadas_tablero:
                long = 1
                posiciones = [(i,j)]
                while not (i,j) in posiciones_ocupadas_tablero and j < long_tablero:
                    long += 1
                    posiciones.append((i,j))
                    j += 1
                if long >= 2 and not long in long_y_posiciones.keys():
                    long_y_posiciones[long] = posiciones
            j += 1
    return long_y_posiciones

def agregar_palabra_al_tablero(long_max, long_y_posiciones, mejor_palabra, window):
    for i in range(long_max):
        window[long_y_posiciones[long_max][i]].update(mejor_palabra[i]) # agregamos las letras al tablero

def calcular_long_maxima(long_y_posiciones.keys(), len(fichas))

# probamos con un ejemplo de 5 fichas, y la longitud maxima que cabe en el tablero 4:
# en su momento esto va a ser recibido como parametro
#fichas = ['a','b','n','o','t','c','m']
fichas = ['a','s','a','c','m']
posiciones_ocupadas_tablero =  [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5), # esto se recibira como parametro desde el archivo de nivel_1
                                                  (1,3),(1,4),
                                (2,0),(2,1),(2,2),
                                                        (3,4),(3,5),
                                (4,0),(4,1),            (4,4),(4,5),
                                
                                           ,(6,2),(6,3),      (6,5),(6,6)] 

long_y_posiciones = mapear_tablero(posiciones_ocupadas_tablero)
long_max = calcular_long_maxima(long_y_posiciones.keys(), len(fichas))
mejor_palabra = obtener_palabra_compu(fichas, long_max)
if mejor_palabra != '':  # caso en que encuentra una palabra valida
    posiciones_ocupadas_tablero.extend(long_y_posiciones[long_max])  # agregamos las posiciones a la lista de posiciones ocupadas
    agregar_palabra_al_tablero(long_max, long_y_posiciones, mejor_palabra, window) # actualizamos el tablero
else:
    sg.popup("La PC le ha pasado el turno")

print(mejor_palabra)




