import IdentificarPalabra as es
class PC():
    def __init__ (self,fichas):
        self.fichas = fichas #Fichas seria una lista de CHAR
        self.puntaje = 0
    
    def getPuntos(self):
        return self.puntaje 

    def sumPuntos(self,punt):
        self.puntaje += punt
    
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
    
    def _recursividadPalabras(self,lista,long_max,palabra,lista_palabras):
        """
        Agrega a lista_palabras las palabras que considera validas formadas por elementos de lista
        """
        for elem in lista:
            palabra = palabra + elem
            if len(palabra) > 1 and not palabra in lista_palabras and self._tiene_vocales(palabra) and self._tiene_consonantes(palabra) and es.palabra_valida(palabra):
                lista_palabras.append(palabra)
            lista_reducida =  lista.copy()
            lista_reducida.remove(elem)
            self._recursividadPalabras(lista_reducida, long_max, palabra, lista_palabras)
            palabra = palabra[:len(palabra)-1]
    
    def obtenerPalabra(self,long_max):
        palabra = ""
        lista_palabras = []
        self._recursividadPalabras(self.fichas,long_max,palabra,lista_palabras)
        return "" if len(lista_palabras) == 0 else max(lista_palabras)

    puntos = property(getPuntos,sumPuntos,doc="Setters y getters")




        
        