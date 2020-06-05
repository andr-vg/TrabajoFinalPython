import PySimpleGUI as sg
import csv
import sys
import string
import random
import time
import IdentificarPalabra as es
from functools import reduce
import os
import json
absolute_path = os.path.dirname(os.path.abspath(__file__))  # Look for your absolute directory path

def guardar_partida(lista):  # recibe el layout saca los botones que no son del tablero y los exporta a un csv
    guardar = lista
    guardar.pop(0)
    #guardar.pop(16)
    #guardar.pop(17)
    if "win" in sys.platform:
        # arch = open(".\\TrabajoFinalPython\\TrabajoFinalPython\\scrabbleAR\\Datos\\guardado.csv","w")

        arch = open(absolute_path + '\\Datos\\info\\guardado.csv',
                    "w")  # esto lo agregue porque no me encontraba el archivo
    else:
        arch = open(absolute_path + "/Datos/info/guardado.csv", "w")

    escritor = csv.writer(arch)
    for aux in lista:
        escritor.writerow(aux[i].get_text() for i in range(len(aux)))
    arch.close()

def cargar_config_pred():
    """
    carga la configuracion del usuario
    devuelve un diccionario
    """
    if ("win" in sys.platform):
        arch = open(absolute_path + "\\Datos\\info\\configPred.json","r")
    else:
        arch = open(absolute_path + "/Datos/info/configPred.json","r")
    config = dict()
    config = json.load(arch)
    arch.close()
    return config

def cargar_config_usr():
    """
    carga la configuracion del usuario
    devuelve un diccionario
    """
    if ("win" in sys.platform):
        arch = open(absolute_path + "\\Datos\\info\\configUsuario.json","r")
    else:
        arch = open(absolute_path + "/Datos/info/configUsuario.json","r")
    config = dict()
    config = json.load(arch)
    arch.close()
    return config

def cargar_configuraciones(bolsa,puntos_por_letra):
    """
    Carga las configuraciones de usuario o predeterminadas en caso de que no existan las del usuario
    """
    config = dict()
    if ("win" in sys.platform):
        if "configUsuario.json" in os.listdir(absolute_path+"\\Datos\\info"):
            print("HAY CONFIG")
            config = cargar_config_usr()
        else:
            print("NO HAY CONFIG")
            config = cargar_config_pred()
    else:
        if "configUsuario.json" in os.listdir(absolute_path+"/Datos/info"):
             print("HAY CONFIG")
             config = cargar_config_usr()
        else:
            print("NO HAY CONFIG")
            config = cargar_config_pred()
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
    return bolsa,puntos_por_letra,tiempo,dificultad

def hay_fichas(necesito, bolsa):
    return necesito <= (sum(list(bolsa.values())))  # devuelve true si hay en la bolsa la cantidad de fichas que se necesitan

def dar_fichas(dic, bolsa):  # se ingresa un diccionario, y a las keys vacias se les asigna una ficha retirando esa ficha de la bolsa
    letras_juntas= reduce(lambda a,b: a+b , [k*bolsa[k] for k in list(bolsa.keys()) if bolsa[k] != 0]) #cada letra de bolsa y lo multiplico por su cantidad y las sumo A+A= AA, AA+BBB= AABBB
    print("cant de letras = "+str(letras_juntas))
    cant_reemplazadas = 0
    for i in dic.keys():
        if dic[i] == "":
            letra=random.choice(letras_juntas)
            if bolsa[letra] > 0:
                letras_juntas.replace(letra,"",1)
                dic[i]= letra
                bolsa[letra]= (bolsa[letra]) -1
                cant_reemplazadas += 1
    if cant_reemplazadas == 0:
        sg.popup('Se acabaron las fichas')

def devolver_fichas(dic,keys,bolsa):
    for nro in keys:
        bolsa[dic[nro]]+=1
        dic[nro]=""
    return dic

def crear_layout(bolsa,csvreader):  # Creacion del Layout, interpretando los caracteres del csv traduciendo a botones

    blanco = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', '#F44336')) # rojo

    descuento = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                            pad=(0, 0), button_color=('black', '#FFB74D')) # marron
   
    descuento_2 = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                            pad=(0, 0), button_color=('black', '#000000')) # negro

    descuento_3 = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                            pad=(0, 0), button_color=('black', '#8BC34A')) # verde

    premio = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', '#FFFFFF')) # blanco

    premio_2 = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', '#2196F3')) # celeste

    sg.theme("lightblue")
    #sg.theme_background_color('#488A99')

    layout = []
    botones = {}
    key = 0
    # vamos a tratar a los botones como una matriz nxn, donde cada elem tiene asociada una posicion (i,j)
    # 0<=i<=n-1 y 0<=j<=n-1
    i = 0  # i lleva la posicion de fila
    for fila in csvreader:
        fichas = []
        j = 0  # j lleva la posicion de columna
        for boton in fila:
            key = (i, j)  # por lo tanto las key ahora son elementos de una matriz
            if boton == "":  # esto antes eran 4 if, los cambie por un if y 3 elif
                fichas.append(blanco("", key))
                botones[key] = ""
            elif boton == "+":
                fichas.append(premio("", key))
                botones[key] = "+"
            elif boton == "++":
                fichas.append(premio_2("", key))
                botones[key] = "++"
            elif boton == "-":
                fichas.append(descuento("", key))
                botones[key] = "-"
            elif boton == "--":
                fichas.append(descuento_2('', key))
                botones[key] = "--"
            elif boton == "---":
                fichas.append(descuento_3('', key))
                botones[key] = "---"
            elif boton in string.ascii_uppercase and boton != "":
                fichas.append(blanco(boton, key))
                botones[key] = ""
            j += 1
        layout.append(fichas)
        i += 1
    long_tablero  = len(layout) #Esto lo necesita la clase PC para las palabras
    fichas_por_jugador = 7
    letras_jugador= {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: ''}
    letras_maquina= {10: '', 11: '', 12: '',13: '', 14: '', 15: '',16: ''}
    if hay_fichas(fichas_por_jugador, bolsa):
        dar_fichas(letras_maquina, bolsa)
        print("se entregaron las fichas a la maquina: ", letras_maquina)

    if hay_fichas(fichas_por_jugador, bolsa):
        dar_fichas(letras_jugador, bolsa)
        print("se entregaron las fichas al jugador: ", letras_jugador)
    colum = [
        [sg.T("Tiempo: "),sg.Text(str(time.process_time() * 10), key='tiempo')],
       [sg.Text("Puntos jugador:"),sg.T("",key="p_j",size=(0,1))], #Puse (0,1) porque sino no entraban numeros de 2 digitos
       [sg.Text("Puntos Pc:"),sg.T("",key="p_pc",size=(0,1))],
       [sg.Text("Turno actual: ",size=(13,1)),sg.Text("",key="turno",size=(15,1))]
    ]
    frame_colum = [
        [sg.Frame("Info del juego",layout=colum)]
    ]
   
    frame_fichas_jugador = [[sg.Button(button_text=list(letras_jugador.values())[i], key=list(letras_jugador.keys())[i], size=(4, 1),
                             button_color=('white', '#CE5A57'),border_width=0) for i in range(fichas_por_jugador)]]
    frame_fichas_maquina = [[sg.Button(button_text="", key=(list(letras_maquina.keys())[i]), size=(4, 1),border_width=0,
                             button_color=('white', '#CE5A57'),disabled=True) for i in range(fichas_por_jugador)]]
    fila_fichas_jugador = [sg.Frame("Fichas jugador",layout=frame_fichas_jugador)]+ [sg.Text("",key="turnoj", size=(15, 1))]
    fila_fichas_maquina = [sg.Frame("Fichas maquina",layout=frame_fichas_maquina)]+ [sg.Text("",key="turnopc", size=(15, 1))]
    fila_botones = [sg.Button("Confirmar", key="-c", disabled=True), sg.Button("Deshacer", key="-d", disabled=True), sg.Button("Terminar", key="-t"),
                    sg.Button("Cambiar fichas", key="-cf",tooltip='Un click aqui para seleccionar las letras,\nClick en las letras a cambiar,\nOtro click aqui para cambiarlas.'),
                    sg.Button("Posponer", key="-p"),sg.Button("Pasar Turno",key="-paso")]+[sg.Column(frame_colum)]
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
        window[val].update(botones[val], disabled=False) # eliminamos del tablero las fichas
    letras_usadas = dict()
    palabra_nueva = dict()
    return letras_usadas, palabra_nueva

def confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, puntos_por_letra, pj, posiciones_ocupadas_tablero, bolsa):
    """
    Funcion que analiza si la palabra ingresada es una palabra valida y si no lo es
    actualiza el tablero y los parametros
    """
    turno_jugador = True
    turno_pc = False
    letras_usadas, palabra_nueva, actualizar_juego, posiciones_ocupadas_tablero = pj.jugar(palabra_nueva, letras_usadas, posiciones_ocupadas_tablero)
    if actualizar_juego:
        window['-d'].update(disabled=True)
        letras = pj.getFichas()
        dar_fichas(letras, bolsa)
        pj.setFichas(letras)
        for f in letras_usadas.keys():  #en el lugar de las fichas que se usaron pongo las letras nuevas en el tablero
            window[f].update(letras[f], disabled=False)
        letras_usadas = dict()
        palabra_nueva = dict()
        turno_jugador = False
        turno_pc = True
    else:
        letras_usadas, palabra_nueva = sacar_del_tablero(window, letras.keys(), palabra_nueva, botones)
    return letras_usadas, palabra_nueva, turno_jugador, turno_pc  


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

def main():
    bolsa = {"E":0,"A":0,"I":0,"O":0,"U":0,"S":0,"N":0,"R":0,"L":0,"T":0,"C":0,"D":0,"M":0,"B":0,
        "G":0,"P":0,"F":0,"H":0,"V":0,"J":0,"Y":0,"K":0,"Ñ":0,"Q":0,"W":0,"X":0,"Z":0,"LL":0,"RR":0}
    puntos_por_letra = {"E":0,"A":0,"I":0,"O":0,"U":0,"S":0,"N":0,"R":0,"L":0,"T":0,"C":0,"D":0,"M":0,"B":0,
        "G":0,"P":0,"F":0,"H":0,"V":0,"J":0,"Y":0,"K":0,"Ñ":0,"Q":0,"W":0,"X":0,"Z":0,"LL":0,"RR":0}
    # Config del tablero:
    bolsa , puntos_por_letra, tiempo ,dificultad = cargar_configuraciones(bolsa,puntos_por_letra)

    #Cargo dificultad para despues diferenciar que tablero cargar y mandarselo al objeto
    #Abro el tablero correspondiente a la dificultad seleccionada

    if "win" in sys.platform: #Abre para windows
        if(dificultad == "facil"):
            arch = open(absolute_path + '\\Datos\\info\\tablero-mario.csv', "r")  # esto lo agregue porque no me encontraba el archivo
        elif (dificultad == "medio"):
            arch = open(absolute_path + '\\Datos\\info\\tablero-nivel-2.csv', "r")
        else:
            arch = open(absolute_path + '\\Datos\\info\\tablero-nivel-3.csv', "r")
    else: #Abre para linux
        if(dificultad == "facil"):
            arch = open(absolute_path + '/Datos/info/tablero-nivel-1.csv', "r")  # esto lo agregue porque no me encontraba el archivo
        elif (dificultad == "medio"):
            arch = open(absolute_path + '/Datos/info/tablero-nivel-2.csv', "r")
        else:
            arch = open(absolute_path + '/Datos/info/tablero-nivel-3.csv', "r")

    csvreader = csv.reader(arch)

    layout, letras, letras_pc, botones, long_tablero = crear_layout(bolsa,csvreader)  # botones es un diccionario de pares (tupla, valor)

    from JugadorPC import PC
    from Jugador import Jugador

    #Opciones de dificultad
    dificultad_random = ["NN","JJ","VB"]
    if (dificultad == "dificil"):
        import random
        tipo = dificultad_random[random.randint(0,2)]
    else:
        tipo = ""

    pj = Jugador(letras,long_tablero,botones,puntos_por_letra,dificultad,tipo)
    pc = PC(letras_pc,long_tablero,botones,puntos_por_letra,dificultad,tipo)

    window = sg.Window("Ventana de juego", layout)

    letras_usadas = {}  # pares (clave, valor) de las letras seleccionadas del atril

    palabra_nueva = {}  # pares (clave, valor) de las letras colocadas en el tablero

    turno_jugador = True

    turno_pc = False

    primer_turno = True

    cambios_de_fichas = 0

    posiciones_ocupadas_tablero = []  # aca vamos almacenando las posiciones (i,j) ocupadas en el tablero

    cont_tiempo = tiempo  # Esto deberia venir como parametro
    cuenta_regresiva = int(time.time()) + cont_tiempo
    #Cierro el archivo del tablero
    arch.close()
    window.finalize()

    # se decide de forma aleatoria quien comienza la partida
    #turno = random.randint(0,1) # comentado por ahora
    turno = 1 # lo dejamos en uno hasta poder implementar el turno de la pc, despues se saca
    if turno == 1:
        turno_jugador, turno_pc = cambiar_turno(not(turno_jugador), not(turno_pc), window)
    else:
        turno_jugador, turno_pc = cambiar_turno(turno_jugador, turno_pc, window)

    while True:  # Event Loop
        # Actualizamos el tiempo en pantalla
        restar_tiempo = int(time.time())
        event, values = window.read(timeout=1000)
        window["tiempo"].update(str(round(cuenta_regresiva - restar_tiempo)))
        if restar_tiempo > cuenta_regresiva:
            print("Se termino el tiempo")
            # Implementar final de partida
            pass
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
                # no pude agregar que actualice aca porque sino mueren las fichas
                if restar_tiempo > cuenta_regresiva:
                    print("Se termino el tiempo")
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
                letras_a_cambiar=[]
                while True:
                    event = window.read()[0]
                    if event is None:
                        break   #ver
                    elif event in letras.keys():
                        letras_a_cambiar.append(event)
                        window[event].update(disabled=True)
                    elif event == "-cf":
                        print(letras)
                        letras=devolver_fichas(letras,letras_a_cambiar,bolsa)
                        dar_fichas(letras,bolsa)
                        pj.setFichas(letras)
                        print(letras)
                        for f in letras_a_cambiar:
                            window[f].update(letras[f], disabled=False)
                        cambios_de_fichas+=1
                        if cambios_de_fichas == 3:
                            window["-cf"].update(disabled=True)
                            window["-cf"].set_tooltip('Ya realizaste 3 cambios de fichas.')
                        break
                turno_jugador,turno_pc= cambiar_turno(turno_jugador,turno_pc, window)
            # boton de guardar partida
            elif event == "-p":
                guardar_partida(layout)
            # boton de terminar partida
            elif event == "-t":  # Y no se termino el tiempo..
                # Implementar
                pass
            # boton de confirmar palabra
            elif event == "-c":
                window["-c"].update(disabled=True)
                print(palabra_nueva)
                # vamos a analizar si la palabra fue posicionada correctamente (misma fila y columnas contiguas):
                letras_usadas, palabra_nueva, turno_jugador, turno_pc = confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, puntos_por_letra, pj, posiciones_ocupadas_tablero, bolsa)
                window["p_j"].update("Puntos jugador:"+str(pj.puntos))
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
                # no pude agregar que actualice aca porque sino mueren las fichas
                if restar_tiempo > cuenta_regresiva:
                    print("Se termino el tiempo")
                if event in botones.keys():
                # refresco la tabla en la casilla seleccionada con la letra elegida antes
                    ind = event  # casilla seleccionada
                    palabra_nueva[ind] = letras[box]
                    if len(palabra_nueva.keys()) > 1:
                        window["-c"].update(disabled=False) # recien ahora puede confirmar
                    window[ind].update(letras[box], disabled=True)  # actualizo la casilla y la desactivo
                    for val in letras.keys():
                        if val not in letras_usadas.keys():
                            window[val].update(disabled=False)  # refresco la tabla B
        # turno de la pc: implementar
        if turno_pc:
           #aca va un if o un elif??
            #time.sleep(0.5)   #maquina pensando la jugarreta
            pc.jugar(window,posiciones_ocupadas_tablero)
            fichas_pc = pc.getFichas()
            print("FICHAS de la pc antes:",fichas_pc)
            dar_fichas(fichas_pc, bolsa)
            print("Fichas de la pc despues:",fichas_pc)
            pc.setFichas(fichas_pc)
            # aca tendriamos que llamar al modulo de jugadorPC
            # finaliza y actualizamos los turnos: turno_pc = False, turno_jugador = True
            turno_jugador, turno_pc= cambiar_turno(turno_jugador ,turno_pc, window)
        # Implementar final de partida

    window.close()

if __name__ == "__main__":
    main()
