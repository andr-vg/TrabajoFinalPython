import PySimpleGUI as sg
import csv
import sys
import string
import random
import time
from functools import reduce
import os
import json
import ScrabbleAR   #Menu del juego
absolute_path = os.path.dirname(os.path.abspath(__file__))  # Look for your absolute directory path

def guardar_info_partida(datos):
    """
    Guarda las puntuaciones, tiempo restante

    """
    arch = open(os.path.join(absolute_path, "Datos","info","datos_guardados.json"), "w")
    json.dump(datos,arch,indent = 2)
    arch.close()

def guardar_partida(window,botones):
    """
    recibe el layout saca los botones que no son del tablero y los exporta a un csv

    """
    # guardar = lista[1:16] #Aislo el tablero del layout
    # print(guardar)
    arch = open(os.path.join(absolute_path, "Datos","info","guardado.csv"), "w",newline='')
    escritor = csv.writer(arch)
    x = 0 #Pos de la lista
    for aux in range(15):
         escritor.writerow(window[(x,i)].get_text()+botones[x,i] for i in range(15))
         x+=1

    arch.close()
def cargar_config_pred():
    """
    carga la configuracion del usuario
    devuelve un diccionario
    """
    arch = open(os.path.join(absolute_path, "Datos","info","configPred.json"), "r") #os.path.join() forma un string con forma de directorio con los argumentos que le pases, con / o \ segun el sis op
    config = dict()
    config = json.load(arch)
    arch.close()
    return config

def cargar_config_usr():
    """
    carga la configuracion del usuario
    devuelve un diccionario
    """
    arch = open(os.path.join(absolute_path, "Datos","info","configUsuario.json"), "r")
    config = dict()
    config = json.load(arch)
    arch.close()

    return config

def cargar_config_guardada():
    """
    carga la configuracion de un juego guardado
    """
    arch = open(os.path.join(absolute_path, "Datos","info","datos_guardados.json"), "r")
    config = dict()
    config =  json.load(arch)
    arch.close()

    return config

def cargar_configuraciones(bolsa,puntos_por_letra,guardado):
    """
    Carga las configuraciones de usuario o predeterminadas en caso de que no existan las del usuario
    """
    config = dict()
    if not(guardado):
        if "configUsuario.json" in os.listdir(os.path.join(absolute_path, "Datos","info")):
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

def hay_fichas(necesito, bolsa):
    return necesito <= (sum(list(bolsa.values())))  # devuelve true si hay en la bolsa la cantidad de fichas que se necesitan

def dar_fichas(dic, bolsa):  # se ingresa un diccionario, y a las keys vacias se les asigna una ficha retirando esa ficha de la bolsa
    # print("bolsa = ",bolsa)
    #letras_juntas= reduce(lambda a,b: a+b , [k*bolsa[k] for k in list(bolsa.keys()) if bolsa[k] != 0]) #cada letra de bolsa y lo multiplico por su cantidad y las sumo A+A= AA, AA+BBB= AABBB
    #letras_juntas = list(map(lambda x: x[0] for k in range(x[1]), bolsa.items()))
    letras_juntas = [] # armamos una lista con todas las letras posibles
    for letra, cant in bolsa.items():
        for i in range(cant):
            letras_juntas.append(letra)
    for i in dic.keys():
        if dic[i] == "" and len(letras_juntas) > 0:
            indice = random.randint(0, len(letras_juntas) - 1)
            dic[i] = letras_juntas[indice]
            bolsa[letras_juntas[indice]] -= 1
            letras_juntas.pop(indice)
    if len(letras_juntas) == 0:
        sg.popup('Se acabaron las fichas')

def devolver_fichas(dic,keys,bolsa):
    for nro in keys:
        bolsa[dic[nro]]+=1
        dic[nro]=""
    return dic

def crear_layout(bolsa, csvreader, dificultad, tipo, img_nros, puntos_por_letra):
    """
    Creacion del Layout, interpretando los caracteres del csv traduciendo a botones
    """
    ################ Texto a mostrar en pantalla según dificultad ###################
    tipo_palabra = {"sust" : 'Solo sustantivos' , "adj" : 'Solo adjetivos', "verbo" : 'Solo verbos'}

    if dificultad == 'dificil':
        tipo = tipo_palabra[tipo]
    elif dificultad == 'facil':
        tipo = 'Sustantivos, adjetivos y verbos'
    else:
        tipo = 'Adjetivos y verbos'

    ################ Colores segun el nivel ######################

    colores = {'facil' : {'' : '#FFFFFF', '+' : '#004080', '++' : '#0E6371', '-' : '#008080', '--' : '#005555', '---' : '#000000'},
               'medio' : {'': '#82b1ff', '+': 'white', '++': '#d50000', '-': '#c5cae9', '--': '#ffeb3b', '---': '#ff5722'},
               'dificil' : {'' : '#00102e', '+' : '#b7c2cc', '++' : '#57024d', '-' : '#9c037d', '--' : '#8a88b3', '---' : '#ffc27d'}
              }

    ################ Tipos de casilleros #########################

    # casilleros de name = --- : restan 3 ptos
    # casilleros de name =  -- : restan 2 ptos
    # casilleros de name =  - : restan 1 ptos
    # casilleros de name =  ++ : triplican ptos
    # casilleros de name = '' : no suman ni restan ptos
    # casilleros de name =  + : duplican ptos

    casillero = lambda name, key: sg.Button('', border_width=1, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', colores[dificultad][name]))

    # casilleros con letras de una partida anterior:

    ficha_pc = lambda name,key: sg.Button(name, border_width = 1, size = (3,1), key = key, pad = (0,0), button_color = ("#000000","#A4E6FD"))

    blanco = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', 'white'))

    sg.theme("lightblue")
    #sg.theme_background_color('#488A99')

    ############### Lectura del archivo del tablero .csv ###############

    layout = []
    botones = {}
    key = 0

    # vamos a tratar a los botones como una matriz nxn, donde cada elem tiene asociada una posicion (i,j)
    # 0<=i<=n-1 y 0<=j<=n-1

    columna_casilleros = []

    i = 0  # i lleva la posicion de fila
    for fila in csvreader:
        fichas = []
        j = 0  # j lleva la posicion de columna
        for boton in fila:
            key = (i, j)  # por lo tanto las key ahora son elementos de una matriz
            if boton == "":
                fichas.append(casillero('', key))
                botones[key] = ""
            elif boton == "+":
                fichas.append(casillero('+', key))
                botones[key] = "+"
            elif boton == "++":
                fichas.append(casillero('++', key))
                botones[key] = "++"
            elif boton == "-":
                fichas.append(casillero('-', key))
                botones[key] = "-"
            elif boton == "--":
                fichas.append(casillero('--', key))
                botones[key] = "--"
            elif boton == "---":
                fichas.append(casillero('---', key))
                botones[key] = "---"
            # casilleros que ya están ocupados por letras (caso de partida previamente guardada)
            elif (boton[0] in string.ascii_uppercase) and (boton != " "):
                if (len(boton)> 1):
                    if boton[1] == "*":
                        fichas.append(ficha_pc(boton[0],key)) # casillas ocupadas por la maquina en una partida previa fueron guardadas con *
                    else:
                        fichas.append(blanco(boton,key))  # casillas ocupadas por el jugador en una partida previa
                botones[key] = ""
            j += 1
        columna_casilleros.append(fichas)
        i += 1

    long_tablero  = len(columna_casilleros) #Esto lo necesita la clase PC para las palabras
    fichas_por_jugador = 7

    ######### entrega de fichas al jugador y a la maquina ##############

    letras_jugador= {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: ''}
    letras_maquina= {10: '', 11: '', 12: '',13: '', 14: '', 15: '',16: ''}
    if hay_fichas(fichas_por_jugador, bolsa):
        dar_fichas(letras_maquina, bolsa)
        # print("se entregaron las fichas a la maquina: ", letras_maquina)

    if hay_fichas(fichas_por_jugador, bolsa):
        dar_fichas(letras_jugador, bolsa)
        # print("se entregaron las fichas al jugador: ", letras_jugador)

    ############## Creacion del tablero y datos a mostrar #####################

    premio_y_descuento = {'': 'Simple', '+': 'Duplica puntaje', '++': 'Triplica puntaje', '-': 'Resta 1 pto', '--': 'Resta 2 ptos', '---': 'Resta 3 ptos'}

    columna_datos = [[sg.Text('Nivel: '+dificultad)],
                     [sg.Text('Tipos de palabras a formar: '+tipo)],
                    ]

    info_colores = list(map(lambda x: [sg.Button(button_color=('white',colores[dificultad][x]), size=(3,1), disabled=True), sg.Text(premio_y_descuento[x])], colores[dificultad].keys()))

    for i in range(len(info_colores)):
        columna_datos.append(info_colores[i])

    colum = [
        [sg.T("Tiempo: "),sg.Text('00:00', key='tiempo')],
       [sg.Text("Tus Puntos:"),sg.T("",key="p_j",size=(0,1))], #Puse (0,1) porque sino no entraban numeros de 2 digitos
       [sg.Text("Puntos Pc:"),sg.T("",key="p_pc",size=(0,1))],
       [sg.Text("Turno actual:",size=(13,1)),sg.Text("",key="turno",size=(10,1))]
    ]

    columna_datos.extend(colum)

    frame_colum = [
        [sg.Frame("Info del juego",layout=columna_datos, element_justification='left')]
    ]

    columna_principal = [sg.Column(columna_casilleros, background_color='grey'), sg.Column(frame_colum)]

    layout.append(columna_principal)

    frame_fichas_jugador = [[sg.Button(button_text=list(letras_jugador.values())[i], key=list(letras_jugador.keys())[i], font=('Gadugi', 25),
                             button_color=('white', '#CE5A57'),border_width=0, image_filename=img_nros[puntos_por_letra[letras_jugador[i]]], image_size=(50, 50), image_subsample=21) for i in range(fichas_por_jugador)]]
    frame_fichas_maquina = [[sg.Button(button_text="", key=(list(letras_maquina.keys())[i]), size=(6, 3),border_width=0,
                             button_color=('white', '#CE5A57'),disabled=True) for i in range(fichas_por_jugador)]]
    fila_fichas_jugador = [sg.Frame("Fichas jugador",layout=frame_fichas_jugador)]+ [sg.Text("",key="turnoj", size=(15, 1))]
    fila_fichas_maquina = [sg.Frame("Fichas maquina",layout=frame_fichas_maquina)]+ [sg.Text("",key="turnopc", size=(15, 1))]
    fila_botones = [sg.Button("Confirmar", key="-c", disabled=True), sg.Button("Deshacer", key="-d", disabled=True), sg.Button("Terminar", key="-t"),
                    sg.Button("Cambiar fichas", key="-cf",tooltip='Click aqui para seleccionar las letras a cambiar\n si ya hay fichas jugadas en el tablero volveran al atril.'),
                    sg.Button("Posponer", key="-p"),sg.Button("Pasar Turno",key="-paso")]
    layout.append(fila_botones)
    layout.append(fila_fichas_jugador)
    layout.insert(0,fila_fichas_maquina)

    return layout, letras_jugador, letras_maquina, botones , long_tablero

def sacar_del_tablero(window, keys, palabra_nueva, botones):
    """
    Sacamos las letras del tablero que no son validas y reiniciamos los parametros
    que guardan nuestras letras y la palabra
    """
    for val in keys:
        window[val].update(disabled=False)  # reactivamos las fichas
    for val in palabra_nueva:
        window[val].update("", disabled=False) # eliminamos del tablero las fichas
    letras_usadas = dict()
    palabra_nueva = dict()
    return letras_usadas, palabra_nueva

def pocas_fichas(fichas):
    if len("".join(fichas.values())) < len(fichas.keys()):
        return True
    else:
        return False

def confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, puntos_por_letra, pj, posiciones_ocupadas_tablero, bolsa, primer_turno, img_nros):
    """
    Funcion que analiza si la palabra ingresada es una palabra valida y si no lo es
    actualiza el tablero y los parametros
    """
    turno_jugador = True
    turno_pc = False
    fin_juego = False
    letras_usadas, palabra_nueva, actualizar_juego, posiciones_ocupadas_tablero = pj.jugar(palabra_nueva, letras_usadas, posiciones_ocupadas_tablero, primer_turno)
    if actualizar_juego:
        window['-d'].update(disabled=True)
        letras = pj.getFichas()
        dar_fichas(letras, bolsa)
        pj.setFichas(letras)
        fin_juego = pocas_fichas(pj.getFichas())
        if not fin_juego:
            for f in letras_usadas.keys():  #en el lugar de las fichas que se usaron pongo las letras nuevas en el tablero
                window[f].update(letras[f], image_size=(50, 50), image_subsample=21, image_filename=img_nros[puntos_por_letra[letras[f]]], disabled=False)
            letras_usadas = dict()
            palabra_nueva = dict()
            turno_jugador, turno_pc = cambiar_turno(turno_jugador, turno_pc, window)
    else:
        letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones)
    return letras_usadas, palabra_nueva, turno_jugador, turno_pc, fin_juego


def cambiar_turno(turnoj, turnopc, window):#
    turnoj= not(turnoj)
    turnopc= not(turnopc)
    if turnoj:
        window["turno"].update("¡Es tu turno!")
    else:
        window["turno"].update("Turno del la maquina")
    window["turnoj"].update("¡Es tu turno!",visible= turnoj)
    window["turnopc"].update("Turno del la maquina",visible= turnopc)
    window.Refresh()    #la window solo se actualiza con read() o refresh(), prefiero poner un refresh aca asi no tengo que esperar a que se actualice el turno en pantalla cuando se haga el read del timeout
    return turnoj,turnopc

def cargar_puntuaciones():
    arch = open(os.path.join(absolute_path, "Datos","info","top_10.json"), "r") #ACA PUEDE IR UNA EXCEPCION HERMOSA DE QUE PASA SI NO ESTA ;D
    top_10 = json.load(arch)
    return top_10

def guardar_puntuaciones(datos):
    arch= open(os.path.join(absolute_path, "Datos","info","top_10.json"), "w")
    json.dump(datos,arch)

def main(guardado):
    import random

    bolsa = {"E":0,"A":0,"I":0,"O":0,"U":0,"S":0,"N":0,"R":0,"L":0,"T":0,"C":0,"D":0,"M":0,"B":0,
        "G":0,"P":0,"F":0,"H":0,"V":0,"J":0,"Y":0,"K":0,"Ñ":0,"Q":0,"W":0,"X":0,"Z":0,"LL":0,"RR":0}
    puntos_por_letra = {"E":0,"A":0,"I":0,"O":0,"U":0,"S":0,"N":0,"R":0,"L":0,"T":0,"C":0,"D":0,"M":0,"B":0,
        "G":0,"P":0,"F":0,"H":0,"V":0,"J":0,"Y":0,"K":0,"Ñ":0,"Q":0,"W":0,"X":0,"Z":0,"LL":0,"RR":0}
    img_nros = {1: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'uno.png'),
                2: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'dos.png'),
                3: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'tres.png'),
                4: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'cuatro.png'),
                5: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'cinco.png'),
                6: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'seis.png'),
                7: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'siete.png'),
                8: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'ocho.png'),
                9: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'nueve.png'),
                10: os.path.join(absolute_path, 'Datos', 'media', 'nros_png', 'diez.png')}

    # Config del tablero:
    bolsa , puntos_por_letra, tiempo ,dificultad, config = cargar_configuraciones(bolsa,puntos_por_letra,guardado)

    #Cargo dificultad para despues diferenciar que tablero cargar y mandarselo al objeto
    #Abro el tablero correspondiente a la dificultad seleccionada
    #Abre para windows y linux
    if (guardado): #Si hay partida guardada carga el tablero guardado
        arch = open(os.path.join(absolute_path, "Datos","info","guardado.csv"),newline = '')
    else:
        if(dificultad == "facil"):
            arch = open(os.path.join(absolute_path, "Datos","info","tablero-nivel-1.csv"), "r")
        elif (dificultad == "medio"):
            arch = open(os.path.join(absolute_path, "Datos","info","tablero-cohete.csv"), "r")
        else:
            arch = open(os.path.join(absolute_path, "Datos","info","tablero-21x21.csv"), "r")

    csvreader = csv.reader(arch)

    #Opciones de dificultad --> lista de tags
    dificultad_random = {'sust': ["NC", "NN", "NCS", "NCP", "NNS", "NP", "NNP", "W"],
                         'adj': ["JJ", "AO", "AQ", "DI", "DT"],
                         'verbo': ["VAG", "VBG", "VAI", "VAN", "MD", "VAS", "VMG", "VMI",
                          "VB", "VMM", "VMN", "VMP", "VBN", "VMS", "VSG", "VSI", "VSN", "VSP", "VSS"]
                        }

    if dificultad == "dificil":
        tipo_palabra = random.choice(list(dificultad_random.keys()))
        tipo = dificultad_random[tipo_palabra]
    elif dificultad == 'facil':
        tipo_palabra = ""
        tipo = dificultad_random['sust'] + dificultad_random['adj'] + dificultad_random['verbo']
    else:
        tipo_palabra = ""
        tipo = dificultad_random['adj'] + dificultad_random['verbo']

    # print(tipo)

    layout, letras, letras_pc, botones, long_tablero = crear_layout(bolsa, csvreader, dificultad, tipo_palabra, img_nros, puntos_por_letra)  # botones es un diccionario de pares (tupla, valor)
    from JugadorPC import PC
    from Jugador import Jugador

    pj = Jugador(letras,long_tablero,botones,puntos_por_letra,dificultad,tipo)
    pc = PC(letras_pc,long_tablero,botones,puntos_por_letra,dificultad,tipo,guardado)
    ###################puntos##################
    if (guardado):
            pj.puntos = config["puntos_j"]
            pc.puntos = config["puntos_pc"]

    window = sg.Window("Ventana de juego", layout)

    letras_usadas = {}  # pares (clave, valor) de las letras seleccionadas del atril

    palabra_nueva = {}  # pares (clave, valor) de las letras colocadas en el tablero

    puntos_jugador = dict()
    puntos_jugador = cargar_puntuaciones()

    if (guardado):
        primer_turno = False
    else:
        primer_turno = True

    cambios_de_fichas = 0

    posiciones_ocupadas_tablero = []  # aca vamos almacenando las posiciones (i,j) ocupadas en el tablero

    fin_fichas = False

    fin_juego = False

    cont_tiempo = tiempo  # Esto deberia venir como parametro
    cuenta_regresiva = int(time.time()) + cont_tiempo
    #Cierro el archivo del tablero
    arch.close()
    window.finalize()

    # se decide de forma aleatoria quien comienza la partida
    #turno = random.randint(0,1) # comentado por ahora
    turno = random.randint(0,1)
    if turno == 1: # empieza el jugador
        turno_jugador = True
        turno_pc = False
    else:  # empieza la compu
        turno_jugador = False
        turno_pc = True
    print(config)

    while True:  # Event Loop
        # Actualizamos el tiempo en pantalla
        restar_tiempo = int(time.time())
        event, values = window.read(timeout=1000)
        print(event,values)
        # print(event)
        window["tiempo"].update(str(round(cuenta_regresiva - restar_tiempo)))
        if restar_tiempo > cuenta_regresiva:
            sg.popup("Se termino el tiempo")
            # Implementar final de partida
            fin_juego = True
        # mientras sea el turno del jugador, podrá realizar todos los eventos del tablero
        if turno_jugador:
            if event is None:
                break
            # botones del atril del jugador
            if event in letras.keys():
                window['-d'].update(disabled=False)
                box = event  # letra seleccionada
                letras_usadas[box] = letras[box]
                window[box].update(button_color=('white', '#FFBEBD'))    #al seleccionado se le cambia el color
                for val in letras.keys():
                    window[val].update(disabled=True)  # desactivo los botones de las fichas
                restar_tiempo = int(time.time())
                event, values = window.read()
                window[box].update(button_color=('white', '#CE5A57'))      #se le devuelve el color

                if event in botones.keys():
                # refresco la tabla en la casilla seleccionada con la letra elegida antes
                    ind = event  # casilla seleccionada
                    if botones[ind] == "+":
                        print("boton mas")
                    elif botones[ind] == "-":
                        print("boton menos")
                    palabra_nueva[ind] = letras[box]
                    if len(palabra_nueva.keys()) > 1:
                        window["-c"].update(disabled=False) # recien ahora puede confirmar
                    window[ind].update(letras[box], disabled=True)  # actualizo la casilla y la desactivo
                    for val in letras.keys():
                        if val not in letras_usadas.keys():
                            window[val].update(disabled=False)  # refresco la tabla B
            # boton de deshacer las palabras puestas en el tablero
            elif event == "-d":
                letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones)
            # boton de pasar el turno a la pc
            elif event == "-paso":
                turno_jugador, turno_pc= cambiar_turno(turno_jugador ,turno_pc, window)
                letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones)
            #boton cambio de fichas
            elif (event == "-cf") and (cambios_de_fichas < 3):
                letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones) #si ya hay fichas jugadas en el tablero volveran al atril
                letras_a_cambiar=[]
                window["-c"].update(disabled=True)  #los desactivo para que no se toque nada que no sean las fichas a cambiar
                window["-d"].update(disabled=True)  #-c y -d no los vuelvo a activar porque los quiero desactivados cuando empiece el sigueinte turno
                window["-paso"].update(disabled=True)
                window["-p"].update(disabled=True)
                window["-t"].update(disabled=True)
                sg.Popup('Cambio de fichas:',
                             'Seleccione clickeando las letras que quiere cambiar y vuelva a clickear en \"Cambiar fichas\" para confirmar el cambio')
                while True:
                    event = window.read()[0]
                    if event is None:
                        break   #ver
                    elif event in letras.keys():
                        letras_a_cambiar.append(event)
                        window[event].update(disabled=True)
                    elif event == "-cf":
                        if letras_a_cambiar:
                            # print(letras)
                            letras=devolver_fichas(letras,letras_a_cambiar,bolsa)
                            dar_fichas(letras,bolsa)
                            pj.setFichas(letras)
                            # print(letras)
                            for f in letras_a_cambiar:
                                window[f].update(letras[f], disabled=False)
                            cambios_de_fichas+=1
                            if cambios_de_fichas == 3:
                                window["-cf"].update(disabled=True)
                                window["-cf"].set_tooltip('Ya realizaste 3 cambios de fichas.')
                            print("Cambio de letras realizado.")
                        else:
                            print("No se selecciono ninguna letra, no se realizo ningun cambio.")
                        break
                turno_jugador,turno_pc= cambiar_turno(turno_jugador,turno_pc, window)
                window["-paso"].update(disabled=False)
                window["-p"].update(disabled=False)
                window["-t"].update(disabled=False)
            # boton de guardar partida
            elif event == "-p":
                boton = pc.getBotones()
                guardar_partida(window,boton)
                datos = dict()
                datos = config
                datos["tiempo"] = round(cuenta_regresiva - restar_tiempo)
                datos["puntos_j"] = pj.puntos
                datos["puntos_pc"] = pc.puntos
                pc.guardar_estado()
                guardar_info_partida(datos)
                break
            # boton de terminar partida
            elif event == "-t" or fin_fichas or fin_juego:  # Y no se termino el tiempo..
                if (pj.puntos > pc.puntos):
                    sg.popup_no_frame("Termino el juego \n Ganaste!")
                else:
                    sg.popup_no_frame("Termino el juego \n Perdiste :( ")
                from datetime import date
                fecha =  str(date.today())
                puntos_jugador[fecha] = pj.puntos
                guardar_puntuaciones(puntos_jugador)
                sg.popup_no_frame("Volveras al menu",auto_close=True,auto_close_duration=5,button_type=None)

                break


            # boton de confirmar palabra
            elif event == "-c":
                window["-c"].update(disabled=True)
                print(palabra_nueva)
                # vamos a analizar si la palabra fue posicionada correctamente (misma fila y columnas contiguas):
                letras_usadas, palabra_nueva, turno_jugador, turno_pc, fin_fichas = confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, puntos_por_letra, pj, posiciones_ocupadas_tablero, bolsa, primer_turno, img_nros)
                if primer_turno and turno_pc:  # si le da confirmar y está mal la palabra, no deja de ser su primer turno
                    primer_turno = False
                window["p_j"].update(str(pj.puntos))
                # botones del atril del jugador
        # turno de la pc: implementar
        if turno_pc:
           #aca va un if o un elif??
            time.sleep(2)   #maquina pensando la jugarreta
            primer_turno = pc.jugar(window,posiciones_ocupadas_tablero,primer_turno)
            fichas_pc = pc.getFichas()
            # print("FICHAS de la pc antes:",fichas_pc)
            dar_fichas(fichas_pc, bolsa)
            # print("Fichas de la pc despues:",fichas_pc)
            pc.setFichas(fichas_pc)
            fin_fichas = pocas_fichas(pc.getFichas())
            # aca tendriamos que llamar al modulo de jugadorPC
            # finaliza y actualizamos los turnos: turno_pc = False, turno_jugador = True
            turno_jugador, turno_pc = cambiar_turno(turno_jugador ,turno_pc, window)

    window.close()

if __name__ == "__main__":
    main(False) #Para testear le puse un True al parametro cuando el juego se ejecute desde el menu
    #si se hace nuevo juego el main se ejecutaria con un True y si es continuar con un False
#Tambien cuando este finalizado el juego se ejecutaria del menu.. entonces este if se iria
#False no hay guardada
#True hay guardada
