def recursividadPalabras(lista, palabra, lista_palabras):
    """
    Agrega a lista_palabras las palabras que considera validas formadas por elementos de lista
    """
    import IdentificarPalabra as es
    for elem in lista:
        palabra = palabra + elem # agrego letra a letra 
        if len(palabra) > 1 and palabra not in lista_palabras and es.palabra_valida(palabra):
            lista_palabras.append(palabra) 
        lista_reducida = lista.copy()
        lista_reducida.remove(elem)
        recursividadPalabras(lista_reducida, palabra, lista_palabras) # la recursividad corta cuando llega a una lista reducida vacia       
        palabra = palabra[:len(palabra)-1] # voy eliminando la ultima letra


# probamos con un ejemplo de 7 letras, en su momento esto va a ser recibido como parametro
#lista = ['a','b','n','o','t','c','m']
lista = ['a','s','a','c','m']
palabra = '' # inicialmente no tenemos caracteres
lista_palabras = [] # aca almacenaremos las palabras que la compu vaya encontrando entre todas las permutaciones
recursividadPalabras(lista, palabra, lista_palabras) 
print(lista_palabras)
print(len(lista_palabras))

