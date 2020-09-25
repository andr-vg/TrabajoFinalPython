"""
------------------------------------------------------------------------------------------
En este archivo se encuentran las funciones que guardan y cargan la informacion del juego
------------------------------------------------------------------------------------------
"""
import os
import Menu
import json
import PySimpleGUI as sg




absolute_path = os.path.join(os.path.dirname(__file__), '..')

def convertirJson(botones):
    """
    Hace un parse del diccionario para guardarlo en json
    """
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
    return dic_aux

def cargar_tablero(tablero):
    """
    Carga el tablero dependiendo la dificultad y devuelve en forma de diccionario
    """
    try:
        if tablero == "facil":
            base = open(os.path.join(absolute_path,"lib","info","boards","facil.json"),"r",encoding='utf8')
        elif tablero == "medio":
            base = open(os.path.join(absolute_path,"lib","info","boards","medio.json"),"r",encoding='utf8')
        elif tablero == "guardado":
            base = open(os.path.join(absolute_path,"lib","info","saves","guardado.json"),"r",encoding='utf8')
        else:
            base = open(os.path.join(absolute_path,"lib","info","boards","dificil.json"),"r",encoding='utf8')
        tablero = json.load(base)
        tab = convertirDic(tablero)
        return tab
    except (FileNotFoundError):
        return None


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
    jota = open(os.path.join(absolute_path, "lib","info","saves","guardado.json"), "w",encoding='utf8')
    botone = convertirJson(botones)
    json.dump(botone,jota,indent=1,ensure_ascii=False)
    jota.close()

def cargar_config_pred():
    """
    carga la configuracion predeterminada
    devuelve un diccionario
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","config","configPred.json"), "r") #os.path.join() forma un string con forma de directorio con los argumentos que le pases, con / o \ segun el sis op
        config = json.load(arch)
        arch.close()
    except (FileNotFoundError):
       config = {
             "tiempo": "3:00",
             "dificultad": "facil",
             "grupo_1": 1,
             "grupo_2": 2,
             "grupo_3": 3,
             "grupo_4": 4,
             "grupo_5": 6,
             "grupo_6": 8,
             "grupo_7": 10,
             "grupo_1_cant": 11,
             "grupo_2_cant": 4,
             "grupo_3_cant": 3,
             "grupo_4_cant": 2,
             "grupo_5_cant": 2,
             "grupo_6_cant": 1,
             "grupo_7_cant": 1
       }
       arch = open(os.path.join(absolute_path, "lib","info","config","configPred.json"), "w")
       json.dump(config,arch,indent=2)
    return config

def cargar_configuraciones(bolsa,puntos_por_letra,guardado):
    """
    Carga las configuraciones de usuario o predeterminadas en caso de que no existan las del usuario
    """
    config = dict()
    if not(guardado):
        if "configUsuario.json" in os.listdir(os.path.join(absolute_path, "lib","info","config")):
            config = cargar_config_usr()
            pred = False
        else:
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
        arch = open(os.path.join(absolute_path, "lib","info","saves","top_10.json"), "r",encoding='utf8') #ACA PUEDE IR UNA EXCEPCION HERMOSA DE QUE PASA SI NO ESTA ;D
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
    arch= open(os.path.join(absolute_path, "lib","info","saves","top_10.json"), "w",encoding='utf8')
    json.dump(datos,arch,indent= 2,ensure_ascii=False)

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
        sg.popup("No se encontraron datos de una partida guardada, reinicie el juego",keep_on_top=True)


def cargar_colores():
    """
    Carga los colores del archivo colores.json
    """
    try:
        col = open(os.path.join(absolute_path, "lib", "info","config" ,"colores.json"),"r")
        dic_col = json.load(col)
        col.close()
    except (FileNotFoundError):
        sg.popup("No se encontro colores.json \n usando colores predeterminados",keep_on_top=True)
        dic_col = {
                 "facil": {
                        "": "#FFFFFF",
                        "+": "#ff6699",
                        "++": "#ff99cc",
                        "+++": "#efcfe8",
                        "++++": "#c1a4ff",
                        "-": "#9999ff",
                        "--": "#9966cc",
                        "---": "#6633cc"
                    },
                    "medio": {
                        "": "#82b1ff",
                        "+": "white",
                        "++": "#d50000",
                        "+++": "#efcfe8",
                        "++++": "#c1a4ff",
                        "-": "#c5cae9",
                        "--": "#ffeb3b",
                        "---": "#ff5722"
                    },
                    "dificil": {
                        "": "#e4f3fa",
                        "+": "#f89d89",
                        "++": "#e59e72",
                        "+++": "#9986a9",
                        "++++": "#ce5a57",
                        "-": "#efd692",
                        "--": "#5386a6",
                        "---": "#4fadac"
                    },
                    "atril":"#006699",
                    "letra_jugador": "#8da8b7",
                    "letra_pc": "#fed0b9"
                }
    finally:
        return (dic_col)

def empezando_la_partida():  
    """
    Popup para inicio de partida
    """
      #estas 2 funciones las importo al menu y al juego
    texto = ' Una vez empezada la partida se encuentran a disposición del jugador el tablero \n'+\
            'y el atril con las fichas para poder jugar, simplemente dando click en la ficha\n'+\
            'deseada y el casillero del tablero deseado podemos ir armando letra a letra la \n'+\
            'palabra de nuestro turno, de esta forma, formando palabras válidas, aprovechando\n'+\
            'los casilleros de bonus y evitando los casilleros de penalización, el jugador va\n'+\
            'sumando puntos.\n'+\
            ' El objetivo del juego es obtener más puntos que la maquina antes de que se acabe\n'+\
            'el tiempo, se acaben las fichas del juego o que ya no se puedan formar palabras.'
    return texto

def botones_especiales():
    """
    Popup de botones especiales
    """
    texto = '• CONFIRMAR: Una vez colocada una palabra sobre el tablero, verifica si esa \n'+\
            'palabra es válida, en caso de serlo se sumarán puntos al puntaje del jugador,\n'+\
            'de lo contrario las fichas usadas volverán al atril.\n'+\
            '\n• DESHACER: Permite devolver al atril las fichas que se hayan puesto en el \n'+\
            'tablero en este turno.\n\n• TERMINAR: Finaliza la partida.\n'+\
            '\n• CAMBIAR FICHAS: Permite seleccionar las fichas.\n'+\
            '\n• POSPONER: Guarda el estado del juego hasta el momento (fichas, puntos,\n'+\
            'palabras jugadas, etc) para poder continuar la partida luego.\n'+\
            '\n• PASAR TURNO: Permite cederle el turno a la máquina.'
    return texto 

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
            datos = open(os.path.join(absolute_path, "lib","info","saves","datos_guardados.json"), "r",encoding='utf8')

        data = json.load(datos)
        table_data = [['A,E,O,S,I,U,N,L,R,T', data["grupo_1_cant"],data["grupo_1"]], ['C,D,G', data["grupo_2_cant"], data["grupo_2"]],
            ['M,B,P', data["grupo_3_cant"], data["grupo_3"]], ['F,H,V,Y', data["grupo_4_cant"], data["grupo_4"]],
            ['J',data["grupo_5_cant"],data["grupo_5"]],['K,LL,Ñ,Q,RR,W,X',data["grupo_6_cant"],data["grupo_6"]],
            ['Z',data["grupo_7_cant"],data["grupo_7"]]
            ]

        headings = ['        LETRAS        ', ' CANTIDAD ', ' PUNTOS ']
        frame = [[sg.T("Dificultad: "+data["dificultad"].capitalize()),sg.T("Tiempo: "+data["tiempo"]+" minutos")]]
        layout = [
        [sg.Frame("",layout=frame)],
        [sg.Table(values=table_data, headings=headings, max_col_width=400,
          auto_size_columns=True, text_color='black',font='Courier 14',
          justification='center', num_rows=7,
          alternating_row_color='#8fa8bf', key='table', def_col_width=35,
          header_text_color='white', header_background_color='#8fa8bf')
          ],
          [sg.B("OK",key="ok",pad=(170,None))]]

        window = sg.Window('Configuraciones del juego', layout, grab_anywhere=False)

        while True:
            event, values = window.Read()
            if event is None or event == "ok":
                break

        window.close()

    except (FileNotFoundError):
        sg.Popup("No se encontro arch de configuraciones")
