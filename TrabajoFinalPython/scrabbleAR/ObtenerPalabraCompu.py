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
    return max(lista_palabras)


# probamos con un ejemplo de 5 fichas, y la longitud maxima que cabe en el tablero 4:
# en su momento esto va a ser recibido como parametro
#fichas = ['a','b','n','o','t','c','m']
fichas = ['a','s','a','c','m']
long_max = 4
mejor_palabra = obtener_palabra_compu(fichas, long_max)
print(mejor_palabra)




