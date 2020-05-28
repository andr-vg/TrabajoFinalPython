import PySimpleGUI as sg
import csv
import sys
import string
import random
import time 
import IdentificarPalabra as es
from functools import reduce
import os
import json
absolute_path = os.path.dirname(os.path.abspath(__file__))  # Look for your absolute directory path



def guardar_partida(lista):  # recibe el layout saca los botones que no son del tablero y los exporta a un csv
    guardar = lista
    guardar.pop(16)
    guardar.pop(15)
    if "win" in sys.platform:
        # arch = open(".\\TrabajoFinalPython\\TrabajoFinalPython\\scrabbleAR\\Datos\\guardado.csv","w")

        arch = open(absolute_path + '\\Datos\\info\\guardado.csv',
                    "w")  # esto lo agregue porque no me encontraba el archivo
    else:
        arch = open(absolute_path + "/Datos/info/guardado.csv", "w")

    escritor = csv.writer(arch)
    for aux in lista:
        escritor.writerow(aux[i].get_text() for i in range(len(aux)))
    arch.close()

def cargar_config_pred():
    """
    carga la configuracion del usuario 
    devuelve un diccionario
    """
    if ("win" in sys.platform):        
        arch = open(absolute_path + "\\Datos\\info\\configPred.json","r")
    else:
        arch = open(absolute_path + "/Datos/info/configPred.json","r")
    config = dict()
    config = json.load(arch)
    arch.close()
    return config

def cargar_config_usr():
    """
    carga la configuracion del usuario 
    devuelve un diccionario
    """
    if ("win" in sys.platform):        
        arch = open(absolute_path + "\\Datos\\info\\configUsuario.json","r")
    else:
        arch = open(absolute_path + "/Datos/info/configUsuario.json","r")
    config = dict()
    config = json.load(arch)
    arch.close()
    return config




def cargar_configuraciones(bolsa,puntos_por_letra):
    """
    Carga las configuraciones de usuario o predeterminadas en caso de que no existan las del usuario
    """
    config = dict()
    if ("win" in sys.platform):
        if "configUsuario.json" in os.listdir(absolute_path+"\\Datos\\info"):
            print("HAY CONFIG")
            config = cargar_config_usr()
        else:
            print("NO HAY CONFIG")
            config = cargar_config_pred()
    else:
        if "configUsuario.json" in os.listdir(absolute_path+"/Datos/info"):
             print("HAY CONFIG")
             config = cargar_config_usr()
        else:
            print("NO HAY CONFIG")  
            config = cargar_config_pred()
    grupo_1 = ["A", "E", "O", "S", "I", "U", "N", "L"," R", "T"]
    grupo_2 = ["C", "D", "G"]
    grupo_3 = ["M","B","P"]
    grupo_4 = ["F","H","V","Y"]
    grupo_5 = ["J"]
    grupo_6 = ["K","LL","Ñ","Q","RR","W","X"]
    grupo_7 = ["Z"]
    cont = 1
    grupos = [grupo_1,grupo_2,grupo_3,grupo_4,grupo_5,grupo_6,grupo_7]
    for grupo in grupos:
        for letra in grupo:
            bolsa[letra] = config["grupo_"+str(cont)]
            puntos_por_letra[letra] = config["grupo_"+str(cont)]
        cont += 1
    
    tiempo =  config["tiempo"]

    return bolsa,puntos_por_letra,tiempo

def hay_fichas(necesito, bolsa):
    return necesito <= (sum(list(bolsa.values())))  # devuelve true si hay en la bolsa la cantidad de fichas que se necesitan

def dar_fichas(cuantas, bolsa):  # devuelve un diccionario con la cantidad de fichas requeridas, retirando esas fichas de la bolsa
    dar = {}
    letras_juntas= reduce(lambda a,b: a+b , [k*bolsa[k] for k in list(bolsa.keys()) if bolsa[k] != 0]) #cada letra de bolsa y lo multiplico por su cantidad y las sumo A+A= AA, AA+BBB= AABBB
    for i in range(cuantas):
        letra=random.choice(letras_juntas)
        dar['-'+str(i)+'-']= letra
        bolsa[letra]= (bolsa[letra]) -1
    return (dar)

def crear_layout(bolsa,csvreader):  # Creacion del Layout, interpretando los caracteres del csv traduciendo a botones

    blanco = lambda name, key: sg.Button(name, border_width=1, size=(5, 2), key=key,
                                         pad=(0, 0), button_color=('black', '#FFFFFF')) # BLANCO FCFCFA

    descuento = lambda name, key: sg.Button(name, border_width=1, size=(5, 2), key=key,
                                            pad=(0, 0), button_color=('black', '#ED5752')) # ROJO

    premio = lambda name, key: sg.Button(name, border_width=1, size=(5, 2), key=key,
                                         pad=(0, 0), button_color=('black', '#C1E1DC')) # VERDE 

    sg.theme("DarkAmber")

    layout = []

    botones = {}  # dict() == {}
    key = 0
    # vamos a tratar a los botones como una matriz nxn, donde cada elem tiene asociada una posicion (i,j) 
    # 0<=i<=n-1 y 0<=j<=n-1
    i = 0  # i lleva la posicion de fila
    for fila in csvreader:
        fichas = []
        j = 0  # j lleva la posicion de columna
        for boton in fila:
            key = (i, j)  # por lo tanto las key ahora son elementos de una matriz
            if boton == "":  # esto antes eran 4 if, los cambie por un if y 3 elif
                fichas.append(blanco("", key))
                botones[key] = ""
            elif boton == "+":
                fichas.append(premio("+", key))
                botones[key] = "+"
            elif boton == "-":
                fichas.append(descuento("-", key))
                botones[key] = "-"
            elif boton in string.ascii_uppercase and boton != "":
                fichas.append(blanco(boton, key))
                botones[key] = ""
            j += 1
        layout.append(fichas)
        i += 1

    fichas_por_jugador = 7
    if hay_fichas(fichas_por_jugador, bolsa):  # si en la bolsa hay suficentes fichas las reparto, si no no porque puede dar error
        letras = dar_fichas(fichas_por_jugador, bolsa)
        print("se entregaron las fichas: ", letras)

    fila_fichas = [sg.Button(button_text=list(letras.values())[i], key=list(letras.keys())[i], size=(4, 2),
                             button_color=('white', 'blue')) for i in range(fichas_por_jugador)]
    fila_botones = [sg.Button("Confirmar", key="-c"), sg.Button("Deshacer", key="-d"), sg.Button("Terminar", key="-t"),
                    sg.Button("Posponer", key="-p"), sg.Text(str(time.process_time() * 10) + " seg", key='tiempo')]
    layout.append(fila_botones)
    layout.append(fila_fichas)
    return layout, letras, botones

def agregar_palabra_al_tablero(palabra_nueva, keys_ordenados, window):
    for key in keys_ordenados:
        window[key].update(palabra_nueva[key])

def sacar_del_tablero(window, keys, palabra_nueva, botones):
    """
    Sacamos las letras del tablero que no son validas y reiniciamos los parametros
    que guardan nuestras letras y la palabra
    """
    for val in keys:
        window[val].update(disabled=False)  # reactivamos las fichas 
    for val in palabra_nueva:
        window[val].update(botones[val], disabled=False) # eliminamos del tablero las fichas
    letras_usadas = dict()
    palabra_nueva = dict()
    return letras_usadas, palabra_nueva 

def confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, palabras_formadas):
    """
    Funcion que analiza si la palabra ingresada es una palabra valida y si no lo es 
    actualiza el tablero y los parametros 
    """
    keys_ordenados = sorted(palabra_nueva.keys())  # los ordeno por columna de menor a mayor
    print(keys_ordenados)
    columna_menor = keys_ordenados[0][1]  # me guarda la columna mas chica con la cual voy a hacer una comparacion
    fila = keys_ordenados[0][0]  # me guardo la primer fila para compararla con las otras a ver si son iguales
    posiciones_validas = True
    for i in range(1, len(keys_ordenados)):
        if keys_ordenados[i][0] != fila:  # aca comparamos las filas de cada letra con la de la primera
            posiciones_validas = False
            break
        if keys_ordenados[i][1] - i != columna_menor:  # si son contiguas, la resta de las mayores columnas - i siempre es igual a la de la menor
            posiciones_validas = False
            break
    # ahora analizamos si es valida o no:
    if not posiciones_validas:
        sg.popup_ok('Palabra no válida, por favor ingrese otra')
        letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones)
    else:
        lista_letras_ordenadas = []
        for key in keys_ordenados:
            lista_letras_ordenadas.append(palabra_nueva[key])
        palabra_obtenida = ''.join(lista_letras_ordenadas)
        print(palabra_obtenida)
        if es.palabra_valida(palabra_obtenida):
            palabras_formadas.append(palabra_obtenida)
            window['-d'].update(disabled=True)
            letras_usadas = dict()
            palabra_nueva = dict()
        else:
            sg.popup_ok('Palabra no válida, por favor ingrese otra')
            letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones)

    return letras_usadas, palabra_nueva, palabras_formadas

def main():
    if "win" in sys.platform:
        arch = open(absolute_path + '\\Datos\\info\\tablero-nivel-1.csv', "r")  # esto lo agregue porque no me encontraba el archivo
    else:
        arch = open(absolute_path + "/Datos/info/tablero-nivel-1.csv", "r")
    csvreader = csv.reader(arch)

    # bolsa contiene las letras a usar por los 2 jugadores, con un numero limitado de letras, a medida que se van repartiendo se van descontando
    bolsa = {"E":0,"A":0,"I":0,"O":0,"U":0,"S":0,"N":0,"R":0,"L":0,"T":0,"C":0,"D":0,"M":0,"B":0,
        "G":0,"P":0,"F":0,"H":0,"V":0,"J":0,"Y":0,"K":0,"Ñ":0,"Q":0,"W":0,"X":0,"Z":0,"LL":0,"RR":0}
    #Puntos
    puntos_por_letra = {"E":0,"A":0,"I":0,"O":0,"U":0,"S":0,"N":0,"R":0,"L":0,"T":0,"C":0,"D":0,"M":0,"B":0,
        "G":0,"P":0,"F":0,"H":0,"V":0,"J":0,"Y":0,"K":0,"Ñ":0,"Q":0,"W":0,"X":0,"Z":0,"LL":0,"RR":0}
    # Config del tablero:
    bolsa , puntos_por_letra, tiempo = cargar_configuraciones(bolsa,puntos_por_letra)
    # print(bolsa)
    # print(puntos_por_letra)
    layout, letras, botones = crear_layout(bolsa,csvreader)  # botones es un diccionario de pares (tupla, valor)

    window = sg.Window("Ventana de juego", layout)

    letras_usadas = dict()  # pares (clave, valor) de las letras seleccionadas

    palabra_nueva = dict()  # pares (clave, valor) de la palabra que se va formando en el tablero

    palabras_formadas = [] # lista de palabras formadas por el jugador



    cont_tiempo = tiempo  # Esto deberia venir como parametro
    cuenta_regresiva = int(time.time()) + cont_tiempo
    #Cierro el archivo del tablero
    arch.close()
    while True:  # Event Loop
        restar_tiempo = int(time.time())
        event, values = window.read(timeout=1000)
        window["tiempo"].update(str(round(cuenta_regresiva - restar_tiempo)))
        print(event, values) 
        if restar_tiempo > cuenta_regresiva:
            print("Se termino el tiempo")
            # Implementar final de partida
            pass  
        if event is None:
            break
        if event == "-p":
            guardar_partida(layout)
        if event == "-t":  # Y no se termino el tiempo..
            # Implementar
            pass
        if event == "-d":
            # deshacer las palabras puestas en el tablero
            letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones)
        # vamos a analizar si la palabra fue posicionada correctamente (misma fila y columnas contiguas):
        if event == "-c":
            # boton de confirmar palabra
            print(palabra_nueva)
            letras_usadas, palabra_nueva, palabras_formadas = confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, palabras_formadas)
        if event in letras.keys():
            window['-d'].update(disabled=False)
            box = event  # letra seleccionada
            letras_usadas[box] = letras[box]
            for val in letras.keys():
                window[val].update(disabled=True)  # desactivo los botones de las fichas
            restar_tiempo = int(time.time())
            event, values = window.read()
        # no pude agregar que actualice aca porque sino mueren las fichas
        if restar_tiempo > cuenta_regresiva:
            print("Se termino el tiempo")
        # Implementar final de partida
        if event in botones.keys():
            # refresco la tabla en la casilla seleccionada con la letra elegida antes
            ind = event  # casilla seleccionada
            if botones[ind] == "+":
                print("boton mas")
            elif botones[ind] == "-":
                print("boton menos")
            palabra_nueva[ind] = letras[box]
            window[ind].update(letras[box], disabled=True)  # actualizo la casilla y la desactivo
            for val in letras.keys():
                if val not in letras_usadas.keys():
                    window[val].update(disabled=False)  # refresco la tabla B

    start_time = time.process_time()
    print(start_time)
    window.close()

if __name__ == "__main__":
    main()
