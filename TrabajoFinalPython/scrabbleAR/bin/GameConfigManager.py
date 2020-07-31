"""
------------------------------------------------------------------------------------------
En este archivo se encuentran las funciones que guardan y cargan la informacion del juego
------------------------------------------------------------------------------------------
"""
import os
import ScrabbleAR
import json
import PySimpleGUI as sg
import csv
from pathlib import Path

absolute_path = os.path.join(os.path.dirname(__file__), '..')

def convertirJson(botones):
    dic_aux = {}
    for clave,valor in botones.items():
        dic_aux[str(clave[0])+","+str(clave[1])] = valor
    return dic_aux

def convertirDic(botones):
    """
    Vuelve a darle formato al diccionario de botones
    """
    dic_aux = {}
    for clave,valor in botones.items():
        dic_aux[tuple(map(int,clave.split(",")))] = valor
    # import pprint
    # p = pprint.PrettyPrinter(indent=4)
    # p.pprint(dic_aux)
    return dic_aux

def cargar_tablero(tablero):
    try:
        if tablero == "facil":
            base = open(os.path.join(absolute_path,"lib","info","boards","facil.json"),"r")
        elif tablero == "medio":
            base = open(os.path.join(absolute_path,"lib","info","boards","medio.json"),"r")
        elif tablero == "guardado":
            base = open(os.path.join(absolute_path,"lib","info","saves","guardado.json"),"r")
        else:
            base = open(os.path.join(absolute_path,"lib","info","boards","dificil.json"),"r")
        tablero = json.load(base)
        tab = convertirDic(tablero)
    except (FileNotFoundError):
        sg.popup("NO SE ENCONTRO TABLERO",keep_on_top=True)
    finally:
        return tab

def guardar_info_partida(datos):
    """
    Guarda las puntuaciones, tiempo restante

    """
    arch = open(os.path.join(absolute_path, "lib","info","saves","datos_guardados.json"), "w")
    json.dump(datos,arch,indent = 2)
    arch.close()

def guardar_partida(botones):
    """
    recibe el layout saca los botones que no son del tablero y los exporta a un csv

    """
    jota = open(os.path.join(absolute_path, "lib","info","saves","guardado.json"), "w")
    botone = convertirJson(botones)
    json.dump(botone,jota,indent=1)
    jota.close()

def cargar_config_pred():
    """
    carga la configuracion predeterminada
    devuelve un diccionario
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","config","configPred.json"), "r") #os.path.join() forma un string con forma de directorio con los argumentos que le pases, con / o \ segun el sis op
        config = dict()
        config = json.load(arch)
        arch.close()
    except (FileNotFoundError):
        sg.popup("No se encontro el archivo de configuraciones predetermiadas \n el juego se cerrara",keep_on_top=True)
        exit()
    return config

def cargar_configuraciones(bolsa,puntos_por_letra,guardado):
    """
    Carga las configuraciones de usuario o predeterminadas en caso de que no existan las del usuario
    """
    config = dict()
    if not(guardado):
        if "configUsuario.json" in os.listdir(os.path.join(absolute_path, "lib","info","config")):
            # print("HAY CONFIG")
            config = cargar_config_usr()
            pred = False
        else:
            # print("NO HAY CONFIG")
            config = cargar_config_pred()
            pred = True
    else:
        config = cargar_config_guardada()
        pred =  False

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
    return bolsa, puntos_por_letra, tiempo, dificultad, config, pred

def cargar_puntuaciones():
    """
    Cargamos las puntuaciones de la partida en un archivo .json
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","saves","top_10.json"), "r") #ACA PUEDE IR UNA EXCEPCION HERMOSA DE QUE PASA SI NO ESTA ;D
        top_10 = json.load(arch)
    except (FileNotFoundError):
        sg.popup("No se encontraron puntuaciones guardadas",keep_on_top=True)
        top_10 = {}
        return top_10
    return top_10

def guardar_puntuaciones(datos):
    """
    Guardamos las puntuaciones de la partida
    """
    arch= open(os.path.join(absolute_path, "lib","info","saves","top_10.json"), "w")
    json.dump(datos,arch,indent= 2)

def cargar_config_usr():
    """
    carga la configuracion del usuario
    devuelve un diccionario
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","config","configUsuario.json"), "r")
        config = dict()
        config = json.load(arch)
        arch.close()
    except (FileNotFoundError):
        sg.popup("No se encontro la configuracion de usuario \n se usara la predeterminada",keep_on_top=True)
        config = cargar_config_pred()
    return config

def cargar_config_guardada():
    """
    carga la configuracion de un juego guardado
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","saves","datos_guardados.json"), "r")
        config = dict()
        config =  json.load(arch)
        arch.close()
        return config
    except (FileNotFoundError):
        sg.popup("No se encontraron datos de una partida guardada, inicie una nueva partida",keep_on_top=True)
        ScrabbleAR.main()
        # Se me quedan 2 menus abiertos y no es la idea...

def cargar_colores():
    try:
        col = open(os.path.join(absolute_path, "lib", "info","config" ,"colores.json"),"r")
        dic_col = json.load(col)
        col.close()
    except (FileNotFoundError):
        sg.popup("No se encontro colores.json \n usando colores predeterminados",keep_on_top=True)
        dic_col = {'facil' : {'' : '#FFFFFF', '+' : '#004080', '++' : '#0E6371', "+++": "#efcfe8", "++++": "#c1a4ff", '-' : '#008080', '--' : '#005555', '---' : '#000000'},
               'medio' : {'': '#82b1ff', '+': 'white', '++': '#d50000', "+++": "#efcfe8", "++++": "#c1a4ff", '-': '#c5cae9', '--': '#ffeb3b', '---': '#ff5722'},
               'dificil' : {'' : '#00102e', '+' : '#b7c2cc', '++' : '#57024d', "+++": "#efcfe8", "++++": "#c1a4ff", '-' : '#9c037d', '--' : '#8a88b3', '---' : '#ffc27d'}
              }
    finally:
        return (dic_col)

def empezando_la_partida():     #estas 2 funciones las importo al menu y al juego
    return """Una vez empezada la partida se encuentran a disposicion del jugador el tablero
y el atril con las fichas para poder jugar, para armar las palabras simplemente dando
un click en la ficha deseada y el casillero del tablero deseado podemos ir armando
letra a letra la palabra de nuestro turno, de esta forma, formando palabras validas, aprovechando
los casilleros de bonus y evitando los casilleros de penalizacion, el jugador va sumando puntos.
El objetivo del juego es obtener mas puntos que la maquina antes de que se acabe el tiempo, se
acaben las fichas del juego o que ya no se puedan formar palabras"""

def botones_especiales():
    return """•"Confirmar": Una vez colocada una palabra sobre el tablero, verifica si esa palabra es valida,
en caso de ser valida se sumaran puntos al puntaje del jugador, de lo contrario las fichas usadas volveran al atril.
•"Deshacer": Permite devolver al atril las fichas que se hayan puesto en el tablero en este turno.
•"Terminar": Finaliza la partida
•"Cambiar Fichas": Permite seleccionar las fichas
•"Posponer": Guarda el estado del juego hasta el momento (fichas, puntos, palabras jugadas, etc)
para poder continuar la partida en otro momento
•"Pasar Turno": Permite cederle el turno a la maquina"""

def get_config_actual(guardado,pred):
    """
    Retorna en forma de string las configuaciones del juego actual
    """
    try:
        if not(guardado):
            if (pred):
                datos = open(os.path.join(absolute_path, "lib","info","config","configPred.json"), "r")
            else:
                datos = open(os.path.join(absolute_path, "lib","info","config","configUsuario.json"), "r")
        else:
            datos = open(os.path.join(absolute_path, "lib","info","saves","datos_guardados.json"), "r")

        data = json.load(datos)
        cadena = """Dificultad: {}
Tiempo: {} minutos
Cantidad de letras y puntos
A,E,O,S,I,U,N,L,R,T || cant: {} || punt: {} ||
C,D,G || cant: {} || punt: {} ||
M,B,P || cant: {} || punt: {} ||
F,H,V,Y || cant: {} || punt: {} ||
J || cant: {} || punt: {} ||
K,LL,Ñ,Q,RR,W,X || cant: {} punt: {} ||
Z || cant: {} || punt: {} ||""".format(data["dificultad"],str(round(int(data["tiempo"])/60)),
                    data["grupo_1"],data["grupo_1_cant"],data["grupo_2"],data["grupo_2_cant"],
                    data["grupo_3"],data["grupo_3_cant"],data["grupo_4"],data["grupo_4_cant"],
                    data["grupo_5"],data["grupo_5_cant"],data["grupo_6"],data["grupo_6_cant"],
                    data["grupo_7"],data["grupo_7_cant"])
        return cadena
    except (FileNotFoundError):
        return "No se encontro arch de configuraciones"
