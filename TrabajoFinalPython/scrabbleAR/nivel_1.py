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

    return csvreader,arch

def guardar_partida (lista): 
     """
     recibe el layout saca los botones que no son del tablero y los exporta a un csv
     """

     guardar = lista
     guardar.pop(len(guardar)-1)
     guardar.pop(len(guardar)-2) #Elimina las ultimas 2 filas de botones que no son del tablero
     if "win" in sys.platform:
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
    csvreader,arch = abrir_arch_tablero()

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
    fila_botones = [sg.Button("Confirmar",key="-c"), sg.Button("Deshacer",key="-d"),sg.Button("Terminar",key="-t"),sg.Button("Posponer",key="-p"),
     sg.Text(" ", key = 'tiempo',pad=(150,None),)]
    layout.append(fila_botones)
    layout.append(fila_fichas)
    arch.close() #Cierro el "tablero.csv"
    return layout, letras, botones

def main(args):
    #Layout
    layout,letras,botones = crear_layout()
    #Ventana
    window = sg.Window("Nivel 1",layout)

    #Dicts
    letras_usadas = {}
    palabra_nueva = {}
    #====TIEMPO====
    cont_tiempo = 20 #Esto deberia venir como parametro
    cuenta_regresiva = time.time() + cont_tiempo

    while True:
        restar_tiempo =  time.time()
        event, values = window.read(timeout=1000)
        print(event,values)
        if (event == None):
            break

        if (restar_tiempo < cuenta_regresiva):
            window["tiempo"].update(str(round(cuenta_regresiva - restar_tiempo)))
        else:
            #Implementar final de partida           
            pass
        if (event == "-p"):
            guardar_partida(layout)       
  
        if event == "-t": #Y no se termino el tiempo..
            #Implementar
            pass
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

        if event in botones.keys():
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




if __name__ == "__main__":
    main(sys.argv)
