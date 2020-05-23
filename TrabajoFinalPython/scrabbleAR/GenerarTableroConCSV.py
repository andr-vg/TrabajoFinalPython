import PySimpleGUI as sg 
import csv
import sys
import string
import random

def get_vocal():    
    x=random.choice('AEIOU')
    return x
def get_consonante():
    x=random.choice('BCDFGHJKLMNÑPQRSTVWXYZ')
    return x

if ("win" in sys.platform):
    arch = open("C:/Users/Usuario/1_SeminarioPython/scrabbleAR/tablero.csv","r")
else:
    arch = open("./scrabbleAR/tablero.csv","r")
csvreader = csv.reader(arch)

def guardar_partida (lista):
    """
    recibe el layout saca los botones que no son del tablero y los exporta a un csv
    """
    guardar = lista
    guardar.pop(16)
    guardar.pop(15)
    arch = open("C:/Users/Usuario/1_SeminarioPython/scrabbleAR/guardado.csv","w")
    escritor = csv.writer(arch)
    for aux in lista:
        escritor.writerow(aux[i].get_text() for i in range(len(aux)))
    arch.close()

def crear_layout():
    
    """
    Creacion del Layout
    """
    blanco = lambda name,key: sg.Button(name,border_width=1, size=(5, 2), key=key, 
    pad=(0,0),button_color=('black','white'))

    descuento = lambda name,key: sg.Button(name,border_width=1, size=(5, 2), key=key, 
    pad=(0,0),button_color=('black','red'))

    premio = lambda name,key: sg.Button(name,border_width=1, size=(5, 2), key=key, 
    pad=(0,0),button_color=('black','green'))

    sg.theme("DarkAmber")

    layout = []

    botones = dict()
    key = 0
    for fila in csvreader:
        fichas = []
        for boton in fila:
            if boton == "":
                fichas.append(blanco("",key))
                botones[key] = ""
            if boton == "+":
                fichas.append(premio("+",key))
                botones[key] = "+"
            if boton == "-":
                fichas.append(descuento("-",key))
                botones[key] = "-"
            if boton in string.ascii_uppercase and boton != "":
                fichas.append(blanco(boton,key))
                botones[key] = ""
            key+=1
        layout.append(fichas)
    letras = dict()
    for i in range(4):                      #aca elegis con la funcion cuantas vocales queres
        val = get_vocal()
        letras['-'+str(i)+'-'] = val        
    for i in range(3):                              #y cuantas consonantes queres, la idea es que haya mas vocales que consonantes para que se puedan armar palabras
        val = get_consonante()              #funciones arriba de todo*
        letras['-'+str(i+4)+'-'] = val 
        
    letras_valores = list(map(lambda x: x[1], letras.items()))
    letras_keys = list(map(lambda x: x[0], letras.items()))
    fila_fichas =[sg.Button(button_text=letras_valores[i], key = letras_keys[i], size=(4, 2), button_color=('white','blue')) for i in range(7)]
    fila_botones = [sg.Button("Confirmar",key="-c"), sg.Button("Deshacer",key="-d"),sg.Button("Terminar",key="-t"),sg.Button("Posponer",key="-p")]
    layout.append(fila_botones)
    layout.append(fila_fichas)
    return layout, letras, botones

"""

Config del tablero

"""

layout, letras, botones = crear_layout()

window = sg.Window("Ventana de juego",layout)

oper = ["-t","-c","-d,""-p"] #Para los botones Terminar Confirmar, Deshacer y Posponer



letras_usadas = dict()  # pares (clave, valor) de las letras seleccionadas

palabra_nueva = dict()  # pares (clave, valor) de la palabra que se va formando en el tablero

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event is None:
        break
    if event == "-p":
        guardar_partida(layout)
    if event == "-t":
        window.FindElement(40,5).Update(button_color=("red","blue"))
    if event == "-d":
        for val in letras.keys():
            window[val].update(disabled=False)
        for val in palabra_nueva:
            window[val].update(palabra_nueva[val], disabled=False)
        letras_usadas = dict()
        palabra_nueva = dict()
    if event in letras.keys():   
        box = event # letra seleccionada
        letras_usadas[box] = letras[box]
        for val in letras.keys():
            window[val].update(disabled=True) # desactivo los botones
        event, values = window.read()
        if event is None:
            break
        if event in botones.keys():
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
            
            

