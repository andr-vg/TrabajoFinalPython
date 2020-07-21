"""
------------------------------------------------------------------------------------------

En este archivo se encuentran las funciones que se usan durante el juego

------------------------------------------------------------------------------------------
"""
import os
import ScrabbleAR
import json
import PySimpleGUI as sg
import random
import math
import GameConfigManager as cm
import string

absolute_path = os.path.join(os.path.dirname(__file__), '..')

def crear_layout(bolsa,tab, dificultad, tipo, img_nros, puntos_por_letra, nombre, palabras_usadas, guardado):
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

    colores = cm.cargar_colores()

    ################ Tipos de casilleros #########################

    # casilleros de name = --- : restan 3 ptos
    # casilleros de name =  -- : restan 2 ptos
    # casilleros de name =  - : restan 1 ptos
    # casilleros de name =  + : duplican ptos por letra
    # casilleros de name =  ++ : triplican ptos por letra
    # casilleros de name =  +++ : duplican ptos por palabra
    # casilleros de name =  ++++ : triplican ptos por palabra
    # casilleros de name = '' : no suman ni restan ptos


    casillero = lambda name, key: sg.Button('', border_width=3, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', colores[dificultad][name]))

    # casilleros con letras de una partida anterior:

    ficha_pc = lambda name,key: sg.Button(name, disabled=True, border_width = 3, size = (3,1), key = key, pad = (0,0), button_color = ("#000000",colores["letra_pc"]),
                                            disabled_button_color = ("#000000",colores["letra_pc"]))

    # blanco = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
    #                                      pad=(0, 0), button_color=('black', 'white'))

    ficha_jugador = lambda name, key: sg.Button(name, disabled=True,border_width=3, size=(3, 1), key=key,
                                         pad=(0, 0), disabled_button_color=('black', colores["letra_jugador"]),button_color=('black', colores["letra_jugador"]))


    sg.LOOK_AND_FEEL_TABLE['MyNewTheme'] = {'BACKGROUND': '#c5dbf1',
                                        'TEXT': '#000000',
                                        'INPUT': '#2a6daf',
                                        'TEXT_INPUT': '#000000',
                                        'SCROLL': '#2a6daf',
                                        'BUTTON': ('white', '#2a6daf'),
                                        'PROGRESS': ('#2a6daf', '#2a6daf'),
                                        'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                                        }

    sg.theme("MyNewTheme")
    layout = []
    botones = {}

    # vamos a tratar a los botones como una matriz nxn, donde cada elem tiene asociada una posicion (i,j)
    # 0<=i<=n-1 y 0<=j<=n-1

    columna_casilleros = []

    i = 0  # i lleva la posicion de fila

    # import pprint
    # p = pprint.PrettyPrinter(indent=2)
    # p.pprint(tab)
    layout = []
    botones = dict()
    largo = int(math.sqrt(len(tab)))
    for x in range(largo):
        fichas = []
        for y in range(largo):
            key = (x,y)
            if tab[key] == "":
                fichas.append(casillero('', key))
                botones[key] = ""
            elif tab[key] == "+":
                fichas.append(casillero('+', key))
                botones[key] = "+"
            elif tab[key] == "++":
                fichas.append(casillero('++', key))
                botones[key] = "++"
            elif tab[key] == '+++':
                fichas.append(casillero('+++', key))
                botones[key] = '+++'
            elif tab[key] == '++++':
                fichas.append(casillero('++++', key))
                botones[key] = '++++'
            elif tab[key] == "-":
                fichas.append(casillero('-', key))
                botones[key] = "-"
            elif tab[key] == "--":
                fichas.append(casillero('--', key))
                botones[key] = "--"
            elif tab[key] == "---":
                fichas.append(casillero('---', key))
                botones[key] = "---"
            # casilleros que ya están ocupados por letras (caso de partida previamente guardada)
            elif (tab[key][0] in string.ascii_uppercase) and (tab[key] != " "):
                if (len(tab[key])> 1):
                    if tab[key][1] == "*":
                        fichas.append(ficha_pc(tab[key][0],key)) # casillas ocupadas por la maquina en una partida previa fueron guardadas con *
                    else:
                        fichas.append(ficha_jugador(tab[key][0],key))  # casillas ocupadas por el jugador en una partida previa
                botones[key] = ""
        columna_casilleros.append(fichas)

    long_tablero  = len(columna_casilleros) #Esto lo necesita la clase PC para las palabras
    fichas_por_jugador = 7

    ######### entrega de fichas al jugador y a la maquina ##############

    letras_jugador= {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: ''}
    letras_maquina= {10: '', 11: '', 12: '',13: '', 14: '', 15: '',16: ''}
    if guardado:
        fichas_jugador = cargar_fichas_jugador()
        fichas_maquina = cargar_fichas_maquina()
        if fichas_jugador != None and fichas_maquina != None:
            for nro, letra in letras_jugador.items():
                letras_jugador[nro] = fichas_jugador[str(nro)]
                letras_maquina[nro+10] = fichas_maquina[str(nro+10)]
        else:
            guardado = False # si no existieran los archivos 
    if not guardado:
        if hay_fichas(fichas_por_jugador, bolsa):
            dar_fichas(letras_maquina, bolsa)

        if hay_fichas(fichas_por_jugador, bolsa):
            dar_fichas(letras_jugador, bolsa)

    ############## Creacion del tablero y datos a mostrar #####################

    premio_y_descuento = {'': 'Simple', '+': 'Duplica puntaje por letra', '++': 'Triplica puntaje por letra', '+++': 'Duplica puntaje por palabra', '++++': 'Triplica puntaje por palabra', '-': 'Resta 1 pto', '--': 'Resta 2 ptos', '---': 'Resta 3 ptos'}

    columna_datos = [[sg.Text('Nivel: '+dificultad)],
                     [sg.Text('Tipos de palabras a formar: '+tipo)],
                    ]

    info_colores = list(map(lambda x: [sg.Button(button_color=('white',colores[dificultad][x]), size=(3,1), disabled=True), sg.Text(premio_y_descuento[x])], colores[dificultad].keys()))

    for i in range(len(info_colores)):
        columna_datos.append(info_colores[i])

    colum = [
        [sg.T("Tiempo: "),sg.Text('00:00', key='tiempo')],
        [sg.T("Cambios de fichas"),sg.T("3",key="cfichas")],
       [sg.Text("Tus Puntos:"),sg.T("0",key="p_j",size=(0,1))],
       [sg.Text("Puntos Pc:"),sg.T("0",key="p_pc",size=(0,1))],
       [sg.Text("Turno actual:",size=(13,1)),sg.Text("",key="turno",size=(10,1))],
       [sg.Button("Como jugar", key="como_jugar"),sg.Button("Botones especiales", key="botonera"),sg.Button("Ver configuracion", key="ver_config")]]

    columna_datos.extend(colum)

    frame_colum = [[sg.Frame("Info del juego",layout=columna_datos, element_justification='left')]]
    columna_principal = [sg.Column(columna_casilleros, background_color='grey'), sg.Column(frame_colum)]

    layout.append(columna_principal)
    frame_palabras_usadas = [[sg.InputCombo(palabras_usadas,key="-pal-",size=(15,1))]]
    frame_fichas_jugador = [[sg.Button(button_text=list(letras_jugador.values())[i], key=list(letras_jugador.keys())[i], font=('Gadugi', 25),
                             button_color=('white', colores["atril"]),border_width=0, image_filename=img_nros[puntos_por_letra[letras_jugador[i]]], image_size=(50, 50), image_subsample=21) for i in range(fichas_por_jugador)]]
    frame_fichas_maquina = [[sg.Button(button_text=" ", key=(list(letras_maquina.keys())[i]),border_width=0, font=('Gadugi', 25), image_filename=img_nros[11],  image_size=(50, 50), image_subsample=21,
                             button_color=('white', colores["atril"]),disabled=True) for i in range(fichas_por_jugador)]]
    fila_fichas_jugador = [sg.Frame("Fichas de "+nombre, layout=frame_fichas_jugador,key="nombre")] + [sg.Frame("Palabras Usadas",layout=frame_palabras_usadas)]
    fila_fichas_maquina = [sg.Frame("Fichas de la Maquina",layout=frame_fichas_maquina)]+ [sg.Text("",key="turnopc", size=(15, 1))]
    fila_botones = [sg.Button("Confirmar", key="-c", disabled=True), sg.Button("Deshacer", key="-d", disabled=True),sg.Button("Pasar Turno",key="-paso"),
                    sg.Button("Cambiar fichas", key="-cf",tooltip='Click aqui para seleccionar las letras a cambiar\n si ya hay fichas jugadas en el tablero volveran al atril.'),
                    sg.Button("Posponer", key="-p"), sg.Button("Terminar", key="-t"), sg.Button("Seleccionar todas las fichas", key="-selec", visible=False), sg.Button("Deshacer selección", key="-deshacer-selec", visible=False)]
    layout.append(fila_botones)
    layout.append(fila_fichas_jugador)
    layout.insert(0,fila_fichas_maquina)
    return layout, letras_jugador, letras_maquina, botones , long_tablero

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
        sg.popup('Se acabaron las fichas',keep_on_top=True)

def devolver_fichas(dic,keys,bolsa):
    """
    Devuelve las fichas a la bolsa
    """
    for nro in keys:
        bolsa[dic[nro]]+=1
        dic[nro]=""
    return dic

def sacar_del_tablero(window, keys, palabra_nueva, botones, dificultad):
    """
    Sacamos las letras del tablero que no son validas y reiniciamos los parametros
    que guardan nuestras letras y la palabra
    """
    colores = cm.cargar_colores()

    for val in keys:
        window[val].update(disabled=False, button_color=('white', '#006699'))  # reactivamos las fichas
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

def input_palabra(lista):
    lista_final = list()
    for pal in lista:
        lista_final.append(pal.replace("\n",""))
    return lista_final

def confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, puntos_por_letra, pj, posiciones_ocupadas_tablero, bolsa, primer_turno, img_nros, botones_aux, dificultad, pc):
    """
    Funcion que analiza si la palabra ingresada es una palabra valida y si no lo es
    actualiza el tablero y los parametros
    """
    turno_jugador = True
    turno_pc = False
    fin_juego = False
    posiciones_ocupadas_tablero = pc.get_pos_tablero()
    letras_usadas, palabra_nueva, actualizar_juego, posiciones_ocupadas_tablero, palabras_usadas = pj.jugar(palabra_nueva, letras_usadas, posiciones_ocupadas_tablero, primer_turno)
    pc.actualizar_pos_tablero(posiciones_ocupadas_tablero)
    if actualizar_juego:

        # aca actualizamos el tablero de botones con las letras que formo el jugador para despues guardarlas si se pospone la partida
        posiciones_tablero_actualizar = pc.get_botones().copy()
        print("botones",posiciones_tablero_actualizar)
        print(palabra_nueva)
        for posicion, letra in palabra_nueva.items():
            posiciones_tablero_actualizar[posicion] = letra + "/"
        pc.actualiza_botones(posiciones_tablero_actualizar)

        window['-d'].update(disabled=True)
        window["-pal-"].update(None,input_palabra(palabras_usadas)) # actualizamos el listbox de palabras si lo ubico correctamente
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
    window["turnopc"].update("Turno del la maquina",visible= turnopc)
    window.Refresh()    #la window solo se actualiza con read() o refresh(), prefiero poner un refresh aca asi no tengo que esperar a que se actualice el turno en pantalla cuando se haga el read del timeout
    return turnoj,turnopc

def mostrar_fichas_compu(window, dic_fichas, img_nros, puntos_por_letra):
    """
    Visualiza las fichas de la compu
    """
    for clave, letra in dic_fichas.items():
        if letra != '':
            window[clave].update(letra, image_filename=img_nros[puntos_por_letra[letra]],
            disabled=False, image_size=(50, 50), image_subsample=21)

def salir_del_juego():
    """
    Ventana que pregunta si salir y guardar el juego, retorna booleanos segun la respuesta del jugador
    """

    layout2 = [[sg.Text('Está saliendo del juego, desea guardarlo?')],
               [sg.Button('Guardar y Salir', key='-guardar'), sg.Button('Salir sin guardar', key='-noguardar')]]
    window_salir = sg.Window('Abandonar partida actual', layout2, no_titlebar = True)

    event, values = window_salir.read()
    if event == '-guardar':
        window_salir.close()
        return True
    else:
        window_salir.close()
        return False

def preguntar_si_sigue_el_juego():
    """
    Ventana que pregunta si finalizar realmente el juego, retorna booleanos segun la respuesta del jugador
    """
    seguir = False

    layout2 = [[sg.Text('Está seguro que desea finalizar la partida?')],
               [sg.Button('Si', key='-si'), sg.Button('Continuar partida', key='-no')]]
    window_salir = sg.Window('Finalizar partida actual', layout2, modal=True)

    while True:
        event, values = window_salir.read()
        if event in (None, '-no'):
            seguir = True
            break
        if event == '-si':
            break
    window_salir.close()
    return seguir

def cargar_fichas_maquina():
    try:
        datos = open(os.path.join(absolute_path, "lib","info","saves","datos_pc.json"), "r")
        data = {}
        data = json.load(datos)
        fichas = data["fichas"]
        return fichas
    except (FileNotFoundError):
        return None


def cargar_fichas_jugador():
    try:
        fichas = open(os.path.join(absolute_path,"lib","info","saves","fichas_jugador.json"),"r")
        fichas_j = json.load(fichas)
        return fichas_j #-----> Puede cargar
    except (FileNotFoundError):
        return None #----> No pude cargar
