import PySimpleGUI as sg
import csv
import sys
import string
import random
import time  # el problema: el tiempo si bien corre, tiene cierto delay, entonces si quiero que el programa finalice en
# 20 segundos, termina finalizando en 40 o más, porque lo hice actualizar segun los botones que va
# seleccionando, hay que encontrar otra forma de actualizarlo
from functools import reduce
import os

absolute_path = os.path.dirname(os.path.abspath(__file__))  # Look for your absolute directory path

if "win" in sys.platform:
    # arch = open(".\\TrabajoFinalPython\\TrabajoFinalPython\\scrabbleAR\\Datos\\tablero.csv","r")

    arch = open(absolute_path + '\\Datos\\info\\tablero.csv', "r")  # esto lo agregue porque no me encontraba el archivo
else:
    arch = open(absolute_path + "/Datos/info/tablero.csv", "r")
csvreader = csv.reader(arch)


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

bolsa= {"E":15,"A":11,"I":6,"O":8,"U":6,"S":7,"N":6,"R":6,"L":4,"T":4,"C":4,"D":4,"M":3,"B":3,
        "G":2,"P":2,"F":2,"H":2,"V":2,"J":2,"Y":1,"K":1,"Ñ":1,"Q":1,"W":1,"X":1,"Z":1}
# bolsa contiene las letras a usar por los 2 jugadores, con un numero limitado de letras, a medida que se van repartiendo se van descontando

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

def crear_layout():  # Creacion del Layout, interpretando los caracteres del csv traduciendo a botones

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


# Config del tablero:

layout, letras, botones = crear_layout()  # botones es un diccionario de pares (tupla, valor)

window = sg.Window("Ventana de juego", layout)

oper = ["-t", "-c", "-d,""-p"]  # Para los botones Terminar, Confirmar, Deshacer y Posponer

letras_usadas = dict()  # pares (clave, valor) de las letras seleccionadas

palabra_nueva = dict()  # pares (clave, valor) de la palabra que se va formando en el tablero

cont_tiempo = 200  # Esto deberia venir como parametro
cuenta_regresiva = int(time.time()) + cont_tiempo

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
        for val in letras.keys():
            window[val].update(disabled=False)
        for val in palabra_nueva:
            window[val].update(botones[val], disabled=False)
        letras_usadas = dict()
        palabra_nueva = dict()
    # vamos a analizar si la palabra fue posicionada correctamente (misma fila y columnas contiguas):
    if event == "-c":
        print(palabra_nueva)
        keys_ordenados = sorted(palabra_nueva.keys())  # los ordeno por columna de menor a mayor
        print(keys_ordenados)
        columna_menor = keys_ordenados[0][1]  # me guarda la columna mas chica con la cual voy a hacer una comparacion
        fila = keys_ordenados[0][0]  # me guardo la primer fila para compararla con las otras a ver si son iguales
        posiciones_validas = True
        for i in range(1, len(keys_ordenados)):
            if keys_ordenados[i][0] != fila:  # aca comparamos las filas de cada letra con la de la primera
                posiciones_validas = False
                break
            if keys_ordenados[i][
                1] - i != columna_menor:  # si son contiguas, la resta de las mayores columnas - i siempre es igual a la de la menor
                posiciones_validas = False
                break
        # ahora analizamos si es valida o no:
        if posiciones_validas:
            lista_letras_ordenadas = []
            for key in keys_ordenados:
                lista_letras_ordenadas.append(palabra_nueva[key])
            palabra_valida = ''.join(lista_letras_ordenadas)
            print(palabra_valida)
            # aca llamariamos a la funcion de pattern que analiza si la palabra es un verbo/sust/adj
            break
        else:
            sg.popup_ok('Palabra no válida, por favor ingrese otra')
            # reiniciamos todo como en deshacer: aca estoy repitiendo codigo, se puede hacer una funcion para reiniciar
            # todo esto
            for val in letras.keys():
                window[val].update(disabled=False)
            for val in palabra_nueva:
                window[val].update(botones[val], disabled=False)
            letras_usadas = dict()
            palabra_nueva = dict()

    if event in letras.keys():
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
        pass
        if event is None:
            break
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
