#------------------------------------------------------------------------------------
#
#En este archivo estan todas las funciones que cargan / guardan configuraciones del juego
#
#------------------------------------------------------------------------------------
import os
import ScrabbleAR 
import json
import PySimpleGUI as sg
import csv
from pathlib import Path

absolute_path = os.path.join(os.path.dirname(__file__), '..')

def guardar_info_partida(datos):
    """
    Guarda las puntuaciones, tiempo restante

    """
    arch = open(os.path.join(absolute_path, "lib","info","datos_guardados.json"), "w")
    json.dump(datos,arch,indent = 2)
    arch.close()

def guardar_partida(window,botones):
    """
    recibe el layout saca los botones que no son del tablero y los exporta a un csv

    """
    arch = open(os.path.join(absolute_path, "lib","info","guardado.csv"), "w",newline='')
    escritor = csv.writer(arch)
    x = 0 #Pos de la lista
    for aux in range(15):
         escritor.writerow(window[(x,i)].get_text()+botones[x,i] for i in range(15))        
         x+=1
    arch.close()

def cargar_config_pred():
    """
    carga la configuracion predeterminada
    devuelve un diccionario
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","configPred.json"), "r") #os.path.join() forma un string con forma de directorio con los argumentos que le pases, con / o \ segun el sis op
        config = dict()
        config = json.load(arch)
        arch.close()
    except (FileNotFoundError):
        sg.popup("No se encontro el archivo de configuraciones predetermiadas \n el juego se cerrara")
        exit()
    return config

def cargar_configuraciones(bolsa,puntos_por_letra,guardado):
    """
    Carga las configuraciones de usuario o predeterminadas en caso de que no existan las del usuario
    """
    config = dict()
    if not(guardado):
        if "configUsuario.json" in os.listdir(os.path.join(absolute_path, "lib","info")):
            # print("HAY CONFIG")
            config = cargar_config_usr()
        else:
            # print("NO HAY CONFIG")
            config = cargar_config_pred()
    else:
        config = cargar_config_guardada()

    grupo_1 = ["A", "E", "O", "S", "I", "U", "N", "L","R", "T"]
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
            bolsa[letra] = config["grupo_"+str(cont)+"_cant"]
            puntos_por_letra[letra] = config["grupo_"+str(cont)]
        cont += 1

    tiempo =  config["tiempo"]
    dificultad = config["dificultad"]
    return bolsa,puntos_por_letra,tiempo,dificultad,config

def cargar_puntuaciones():
    """
    Cargamos las puntuaciones de la partida en un archivo .json
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","top_10.json"), "r") #ACA PUEDE IR UNA EXCEPCION HERMOSA DE QUE PASA SI NO ESTA ;D
        top_10 = json.load(arch)
    except (FileNotFoundError):
        sg.popup("No se encontraron puntuaciones guardadas")
        top_10 = {}
        return top_10
    return top_10

def guardar_puntuaciones(datos):
    """
    Guardamos las puntuaciones de la partida
    """
    arch= open(os.path.join(absolute_path, "lib","info","top_10.json"), "w")
    json.dump(datos,arch,indent= 2)

def cargar_config_usr():
    """
    carga la configuracion del usuario
    devuelve un diccionario
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","configUsuario.json"), "r")
        config = dict()
        config = json.load(arch)
        arch.close()
    except (FileNotFoundError):
        sg.popup("No se encontro la configuracion de usuario \n se usara la predeterminada")
        config = cargar_config_pred()

    return config

def cargar_config_guardada():
    """
    carga la configuracion de un juego guardado
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","datos_guardados.json"), "r")
        config = dict()
        config =  json.load(arch)
        arch.close()
        return config
    except (FileNotFoundError):
        sg.popup("No se encontraron datos de una partida guardada, inicie una nueva partida")
        ScrabbleAR.main()
        # Se me quedan 2 menus abiertos y no es la idea...