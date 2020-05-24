import PySimpleGUI as sg
import csv
import sys
import string
import random
import time
import pattern.text.es 
import os
absolute_path = os.path.dirname(os.path.abspath(__file__)) #busca la direccion del archivo.py

def get_vocal():    #Devuelve una vocal random
    x=random.choice('AEIOU')
    return x

def get_consonante():   #Devuelve una consonante random 

    x=random.choice('BCDFGHJKLMNÑPQRSTVWXYZ')
    return x

def abrir_arch_tablero():
    """
    Pregunta que sistema operativo esta corriendo el programa
    y abre el csv del tablero con la ruta correspondiente

    """
    if "win" in sys.platform:
        arch = open(absolute_path + '\\Datos\\info\\tablero.csv',"r")       #esto lo agregue porque no me encontraba el archivo
    else:
        arch = open(absolute_path + "/Datos/info/tablero.csv","r")
    csvreader = csv.reader(arch)

def guardar_partida (lista): 
     """
     recibe el layout saca los botones que no son del tablero y los exporta a un csv
     """
    guardar = lista
    guardar.pop(16)
    guardar.pop(15)
    if "win" in sys.platform:
        #arch = open(".\\TrabajoFinalPython\\TrabajoFinalPython\\scrabbleAR\\Datos\\guardado.csv","w")

        arch = open(absolute_path + '\\Datos\\info\\guardado.csv',"w")      #esto lo agregue porque no me encontraba el archivo
    else:
        arch = open(absolute_path + "/Datos/info/guardado.csv","w")

    escritor = csv.writer(arch)
    for aux in lista:
        escritor.writerow(aux[i].get_text() for i in range(len(aux)))
    arch.close()

def crear_layout():

    """Creacion del Layout

    interpretando los caracteres del csv traduciendo a botones

    devuelve la lista del layout un diccionario de letras y otro de botones

    """

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