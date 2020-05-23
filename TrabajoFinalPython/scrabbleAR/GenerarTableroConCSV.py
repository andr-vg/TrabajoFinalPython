import PySimpleGUI as sg
import csv
import sys
import string
import random
import time # el problema: el tiempo si bien corre, tiene cierto delay, entonces si quiero que el programa finalice en
            # 20 segundos, termina finalizando en 40 o más, porque lo hice actualizar segun los botones que va 
            # seleccionando, hay que encontrar otra forma de actualizarlo

import os
absolute_path = os.path.dirname(os.path.abspath(__file__))      # Look for your absolute directory path

def get_vocal():    #Devuelve una vocal random
    x=random.choice('AEIOU')
    return x

def get_consonante():   #Devuelve una consonante random
    x=random.choice('BCDFGHJKLMNÑPQRSTVWXYZ')
    return x

if "win" in sys.platform:
    #arch = open(".\\TrabajoFinalPython\\TrabajoFinalPython\\scrabbleAR\\Datos\\tablero.csv","r")

    arch = open(absolute_path + '/Datos/tablero.csv',"r")       #esto lo agregue porque no me encontraba el archivo
else:
    arch = open("./TrabajoFinalPython/TrabajoFinalPython/scrabbleAR/Datos/tablero.csv","r")
csvreader = csv.reader(arch)

def guardar_partida (lista):    #recibe el layout saca los botones que no son del tablero y los exporta a un csv
    guardar = lista
    guardar.pop(16)
    guardar.pop(15)
    if "win" in sys.platform:
        #arch = open(".\\TrabajoFinalPython\\TrabajoFinalPython\\scrabbleAR\\Datos\\guardado.csv","w")

        arch = open(absolute_path + '/Datos/guardado.csv',"w")      #esto lo agregue porque no me encontraba el archivo
    else:
        arch = open("./TrabajoFinalPython/TrabajoFinalPython/scrabbleAR/Datos/guardado.csv","w")

    escritor = csv.writer(arch)
    for aux in lista:
        escritor.writerow(aux[i].get_text() for i in range(len(aux)))
    arch.close()

def crear_layout():

    #Creacion del Layout

    blanco = lambda name,key: sg.Button(name,border_width=1, size=(5, 2), key=key,
    pad=(0,0),button_color=('black','white'))

    descuento = lambda name,key: sg.Button(name,border_width=1, size=(5, 2), key=key,
    pad=(0,0),button_color=('black','red'))

    premio = lambda name,key: sg.Button(name,border_width=1, size=(5, 2), key=key,
    pad=(0,0),button_color=('black','green'))

    sg.theme("DarkAmber")

    layout = []

    botones = {}       #dict() == {}
    key = 0
    for fila in csvreader:
        fichas = []
        for boton in fila:
            if boton == "":         #esto antes eran 4 if, los cambie por un if y 3 elif
                fichas.append(blanco("",key))
                botones[key] = ""
            elif boton == "+":
                fichas.append(premio("+",key))
                botones[key] = "+"
            elif boton == "-":
                fichas.append(descuento("-",key))
                botones[key] = "-"
            elif boton in string.ascii_uppercase and boton != "":
                fichas.append(blanco(boton,key))
                botones[key] = ""
            key+=1
        layout.append(fichas)
    letras = {}
    for i in range(4):                      #con range() elegis cuantas vocales queres
        val = get_vocal()
        letras['-'+str(i)+'-'] = val
    for i in range(3):                          #si hay mas vocales que consonantes es mas facil armar palabras
        val = get_consonante()
        letras['-'+str(i+4)+'-'] = val

    #letras_valores = list(map(lambda x: x[1], letras.items()))         list(map(lambda x: x[1], letras.items())) == list(letras.values())
    letras_valores = list(letras.values())
    letras_keys = list(letras.keys())
    fila_fichas =[sg.Button(button_text= letras_valores[i], key = letras_keys[i], size=(4, 2), button_color=('white','blue')) for i in range(7)]
    fila_botones = [sg.Button("Confirmar",key="-c"), sg.Button("Deshacer",key="-d"),sg.Button("Terminar",key="-t"),sg.Button("Posponer",key="-p"), sg.Text(str(time.process_time()*10)+" seg", key = 'tiempo')]
    layout.append(fila_botones)
    layout.append(fila_fichas)
    return layout, letras, botones


#Config del tablero:

layout, letras, botones = crear_layout()

window = sg.Window("Ventana de juego",layout)

oper = ["-t","-c","-d,""-p"] #Para los botones Terminar, Confirmar, Deshacer y Posponer

letras_usadas = dict()  # pares (clave, valor) de las letras seleccionadas

palabra_nueva = dict()  # pares (clave, valor) de la palabra que se va formando en el tablero

start_time = time.process_time()  # tiempo inicial del juego en segundos -> 0.1 = 1 seg real, supongamos que tiene que durar maximo 2.0 = 20 segs
print(start_time)
while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    window['tiempo'].update(str(time.process_time()*10)+" seg") # actualizo el tiempo en segundos
    if time.process_time() > 2:  # corto la ejecucion a los "20" segundos
        break   
    if event is None:
        break
    if event == "-p":
        guardar_partida(layout)
    if event == "-t": #Y no se termino el tiempo..
        #Implementar
        pass
    if event == "-d":
        window['tiempo'].update(str(time.process_time()*10)+" seg") # actualizo el tiempo en segundos
        if time.process_time() > 2:
            break   
        for val in letras.keys():
            window[val].update(disabled=False)
        for val in palabra_nueva:
            window[val].update(palabra_nueva[val], disabled=False)
        letras_usadas = dict()
        palabra_nueva = dict()
    if event in letras.keys():
        window['tiempo'].update(str(time.process_time()*10)+" seg") # actualizo el tiempo en segundos
        if time.process_time() > 2:
            break   
        box = event # letra seleccionada
        letras_usadas[box] = letras[box]
        for val in letras.keys():
            window[val].update(disabled=True) # desactivo los botones
        event, values = window.read()
        window['tiempo'].update(str(time.process_time()*10)+" seg") # actualizo el tiempo en segundos
        if time.process_time() > 2:
            break   
        if event is None:
            break
        if event in botones.keys():
            window['tiempo'].update(str(time.process_time()*10)+" seg") # actualizo el tiempo en segundos
            if time.process_time() > 2:
                break   
        # refresco la tabla en la casilla seleccionada con la letra elegida antes
            ind = event # casilla seleccionada
            if botones[ind] == "+":
                print("boton mas")
            elif botones[ind] == "-":
                print("boton menos")
            palabra_nueva[ind] = botones[ind]
            window[ind].update(letras[box], disabled=True) # actualizo la casilla y la desactivo
            for val in letras.keys():
                if val not in letras_usadas.keys():
                    window[val].update(disabled=False) # refresco la tabla B

start_time = time.process_time()
print(start_time)