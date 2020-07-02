import PySimpleGUI as sg
import csv
import sys
import string
import random
import time
from functools import reduce
import os
import json
import ScrabbleAR   #-----------------> Menu del juego
import GameConfigManager as cm #---------> Manejo de configuraciones
absolute_path = os.path.dirname(os.path.abspath(__file__)) 

def hay_fichas(necesito, bolsa):
    """
    Devuelve true si hay en la bolsa la cantidad de fichas que se necesitan
    """
    return necesito <= (sum(list(bolsa.values())))  

def dar_fichas(dic, bolsa): 
    """
    se ingresa un diccionario, y a las keys vacias se les asigna una ficha retirando esa ficha de la bolsa
    """

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
    """
    Devuelve las fichas a la bolsa
    """
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

    casillero = lambda name, key: sg.Button('', border_width=3, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', colores[dificultad][name]))

    # casilleros con letras de una partida anterior:

    ficha_pc = lambda name,key: sg.Button(name, border_width = 3, size = (3,1), key = key, pad = (0,0), button_color = ("#000000","#A4E6FD"))

    # blanco = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
    #                                      pad=(0, 0), button_color=('black', 'white'))

    ficha_jugador = lambda name, key: sg.Button(name, border_width=3, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', '#BA7FB0'))
    
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
                        fichas.append(ficha_jugador(boton[0],key))  # casillas ocupadas por el jugador en una partida previa
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

    if hay_fichas(fichas_por_jugador, bolsa):
        dar_fichas(letras_jugador, bolsa)

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
       [sg.Text("Tus Puntos:"),sg.T("",key="p_j",size=(0,1))], 
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

def sacar_del_tablero(window, keys, palabra_nueva, botones, dificultad):
    """
    Sacamos las letras del tablero que no son validas y reiniciamos los parametros
    que guardan nuestras letras y la palabra
    """
    colores = {'facil' : {'' : '#FFFFFF', '+' : '#004080', '++' : '#0E6371', '-' : '#008080', '--' : '#005555', '---' : '#000000'},
               'medio' : {'': '#82b1ff', '+': 'white', '++': '#d50000', '-': '#c5cae9', '--': '#ffeb3b', '---': '#ff5722'},
               'dificil' : {'' : '#00102e', '+' : '#b7c2cc', '++' : '#57024d', '-' : '#9c037d', '--' : '#8a88b3', '---' : '#ffc27d'}
              }

    for val in keys:
        window[val].update(disabled=False)  # reactivamos las fichas
    for val in palabra_nueva:
        window[val].update("", disabled=False,button_color= ("black",colores[dificultad][botones[val]])) # eliminamos del tablero las fichas
    letras_usadas = dict()
    palabra_nueva = dict()
    return letras_usadas, palabra_nueva

def pocas_fichas(fichas):
    if len("".join(fichas.values())) < len(fichas.keys()):
        return True
    else:
        return False

def confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, puntos_por_letra, pj, posiciones_ocupadas_tablero, bolsa, primer_turno, img_nros, botones_aux, dificultad):
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
        letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones_aux,dificultad)
    return letras_usadas, palabra_nueva, turno_jugador, turno_pc, fin_juego

def cambiar_turno(turnoj, turnopc, window):
    """
    Cambio de turno del Usuario --> PC / PC --> Usuario
    """
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

def main(guardado):
    """
    Desarrollo del juego y tablero principal
    """
    import random
    #-----------------------------------------------------------
        #Configuracion de bolsa puntos y
        #Imagen de numeros
    #-----------------------------------------------------------
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

    bolsa , puntos_por_letra, tiempo ,dificultad, config = cm.cargar_configuraciones(bolsa,puntos_por_letra,guardado)
    # ----------------------------------------------------------------------
        #Cargo dificultad para despues diferenciar que tablero cargar y mandarselo al objeto
        #Abro el tablero correspondiente a la dificultad seleccionada
        #Abre para windows y linux
    # ----------------------------------------------------------------------
    if (guardado): #Si hay partida guardada carga el tablero guardado
        arch = open(os.path.join(absolute_path, "Datos","info","guardado.csv"),newline = '')
    else:
        try:
            if(dificultad == "facil"):
                arch = open(os.path.join(absolute_path, "Datos","info","tablero-nivel-1.csv"), "r")
            elif (dificultad == "medio"):
                arch = open(os.path.join(absolute_path, "Datos","info","tablero-cohete.csv"), "r")
            else:
                arch = open(os.path.join(absolute_path, "Datos","info","tablero-21x21.csv"), "r")
        except (FileNotFoundError):
            sg.popup("No se ha encontrado el tablero")
    csvreader = csv.reader(arch)
    # ----------------------------------------------------------------------
        # Opciones de dificultad --> lista de tags
    # ----------------------------------------------------------------------
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
    #Instanciacion de objetos y creacion del layout
    layout, letras, letras_pc, botones, long_tablero = crear_layout(bolsa, csvreader, dificultad, tipo_palabra, img_nros, puntos_por_letra)  # botones es un diccionario de pares (tupla, valor)
    from JugadorPC import PC
    from Jugador import Jugador
    pj = Jugador(letras,long_tablero,botones,puntos_por_letra,dificultad,tipo)
    pc = PC(letras_pc,long_tablero,botones,puntos_por_letra,dificultad,tipo,guardado)
    botones_aux = botones.copy() #-----> Botones_aux lo uso para el boton deshacer
    # ----------------------------------------------------------------------
        # Manejo de puntajes, si hay partida guardada setea los puntos
        #Sino es 0
    # ----------------------------------------------------------------------
    if (guardado):
            pj.puntos = config["puntos_j"]
            pc.puntos = config["puntos_pc"]
    # ----------------------------------------------------------------------
        #Configuracion de ventana y turnos
    # ----------------------------------------------------------------------
    window = sg.Window("Ventana de juego", layout)
    letras_usadas = {}  # pares (clave, valor) de las letras seleccionadas del atril
    palabra_nueva = {}  # pares (clave, valor) de las letras colocadas en el tablero
    puntos_jugador = dict()
    puntos_jugador = cm.cargar_puntuaciones()
    if (guardado):
        primer_turno = False
    else:
        primer_turno = True
    cambios_de_fichas = 0
    posiciones_ocupadas_tablero = []  # aca vamos almacenando las posiciones (i,j) ocupadas en el tablero
    fin_fichas = False
    fin_juego = False
    #Configuracion del tiempo
    cont_tiempo_min_config = tiempo  
    cont_tiempo_min = round(cont_tiempo_min_config / 60)
    if (cont_tiempo_min > 1):
        cont_tiempo_seg = 59
        cont_tiempo_min -= 1
    else:
        cont_tiempo_seg = 0
    arch.close()
    window.finalize()
    # se decide de forma aleatoria quien comienza la partida
    turno = random.randint(0,1)
    if turno == 1: # empieza el jugador
        turno_jugador = True
        turno_pc = False
    else:  # empieza la compu
        turno_jugador = False
        turno_pc = True
    # ----------------------------------------------------------------------
        #Loop de ventana
    # ----------------------------------------------------------------------
    while True: 
        event, values = window.read(timeout=1000)
        if (cont_tiempo_seg == 0):
            cont_tiempo_seg = 59
            cont_tiempo_min -= 1
        else:
            cont_tiempo_seg -= 1
        if (cont_tiempo_seg < 10):
            tiempo_seg_final = "0" + str(cont_tiempo_seg)
        else:
            tiempo_seg_final = cont_tiempo_seg
        tiempo_str = "{}:{}".format(cont_tiempo_min,tiempo_seg_final)
        window["tiempo"].update(tiempo_str)
        if (cont_tiempo_min == 0) and (cont_tiempo_seg == 0):
            sg.popup("Se termino el tiempo")
            fin_juego = True
        #------------------------------------------------------
            # mientras sea el turno del jugador, podrá realizar 
            # todos los eventos del tablero
        #------------------------------------------------------
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
                if (cont_tiempo_seg == 0):
                    cont_tiempo_seg = 59
                    cont_tiempo_min -= 1
                else:
                    cont_tiempo_seg -= 1
                event, values = window.read()
                window[box].update(button_color=('white', '#CE5A57'))      #se le devuelve el color
                if event in botones.keys():
                # refresco la tabla en la casilla seleccionada con la letra elegida antes
                    ind = event  # casilla seleccionada
                    palabra_nueva[ind] = letras[box]
                    if len(palabra_nueva.keys()) > 1:
                        window["-c"].update(disabled=False) # recien ahora puede confirmar
                    window[ind].update(letras[box], disabled=True, button_color = ("black","#BA7FB0"))  # actualizo la casilla y la desactivo
                    botones = pc.get_botones().copy()
                    botones[ind] = "" + "/"
                    pc.actualiza_botones(botones)
                    for val in letras.keys():
                        if val not in letras_usadas.keys():
                            window[val].update(disabled=False)  # refresco la tabla B
            # boton de deshacer las palabras puestas en el tablero
            elif event == "-d":
                letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones_aux, dificultad)
            # boton de pasar el turno a la pc
            elif event == "-paso":
                turno_jugador, turno_pc= cambiar_turno(turno_jugador ,turno_pc, window)
                letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones_aux, dificultad)
            #boton cambio de fichas
            elif (event == "-cf") and (cambios_de_fichas < 3):
                letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones_aux, dificultad) #si ya hay fichas jugadas en el tablero volveran al atril
                letras_a_cambiar=[]
                window["-c"].update(disabled=True)  #los desactivo para que no se toque nada que no sean las fichas a cambiar
                window["-d"].update(disabled=True)  #-c y -d no los vuelvo a activar porque los quiero desactivados cuando empiece el sigueinte turno
                window["-paso"].update(disabled=True)
                window["-p"].update(disabled=True)
                window["-t"].update(disabled=True)
                sg.Popup('Cambio de fichas:',
                             'Seleccione clickeando las letras que quiere cambiar y ',
                             'vuelva a clickear en \"Cambiar fichas\" para confirmar ',
                             'el cambio')
                while True:
                    event = window.read()[0]
                    if event is None:
                        break   #ver
                    elif event in letras.keys():
                        letras_a_cambiar.append(event)
                        window[event].update(disabled=True)
                    elif event == "-cf":
                        if letras_a_cambiar:
                            letras=devolver_fichas(letras,letras_a_cambiar,bolsa)
                            dar_fichas(letras,bolsa)
                            pj.setFichas(letras)
                            for f in letras_a_cambiar:
                                window[f].update(letras[f], image_size=(50, 50), image_subsample=21, image_filename=img_nros[puntos_por_letra[letras[f]]], disabled=False)
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
                boton = pc.get_botones()
                cm.guardar_partida(window,boton)
                datos = dict()
                datos = config
                datos["tiempo"] = tiempo_str
                datos["puntos_j"] = pj.puntos
                datos["puntos_pc"] = pc.puntos
                pc.guardar_estado()
                cm.guardar_info_partida(datos)
                break
            # boton de terminar partida
            elif event == "-t" or fin_fichas or fin_juego:  
                if (pj.puntos > pc.puntos):
                    sg.popup_no_frame("Termino el juego \n Ganaste!")
                elif (pj.puntos == pc.puntos):
                    sg.popup("EMPATE!")
                else:
                    sg.popup_no_frame("Termino el juego \n Perdiste :( ")
                from datetime import datetime
                fecha =  datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                puntos_jugador[fecha] = pj.puntos
                cm.guardar_puntuaciones(puntos_jugador)
                sg.popup_no_frame("Volveras al menu",auto_close=True,auto_close_duration=5,button_type=None)
                break
            # boton de confirmar palabra
            elif event == "-c":
                window["-c"].update(disabled=True)
                # vamos a analizar si la palabra fue posicionada correctamente (misma fila y columnas contiguas):
                letras_usadas, palabra_nueva, turno_jugador, turno_pc, fin_fichas = confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, puntos_por_letra, pj, posiciones_ocupadas_tablero, bolsa, primer_turno, img_nros, botones_aux, dificultad)
                if primer_turno and turno_pc:  # si le da confirmar y está mal la palabra, no deja de ser su primer turno
                    primer_turno = False
                window["p_j"].update(str(pj.puntos))
        if turno_pc:
            # time.sleep(2)   #maquina pensando la jugarreta
            primer_turno = pc.jugar(window,posiciones_ocupadas_tablero,primer_turno)
            fichas_pc = pc.getFichas()
            dar_fichas(fichas_pc, bolsa)
            pc.setFichas(fichas_pc)
            fin_fichas = pocas_fichas(pc.getFichas())
            # finaliza y actualizamos los turnos: turno_pc = False, turno_jugador = True
            turno_jugador, turno_pc = cambiar_turno(turno_jugador ,turno_pc, window)

    window.close()