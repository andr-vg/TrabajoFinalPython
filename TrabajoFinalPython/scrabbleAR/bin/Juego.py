import PySimpleGUI as sg
import time
import os
import ScrabbleAR   #-----------------> Menu del juego
import GameConfigManager as cm #---------> Manejo de configuraciones
import GameManager as gm
absolute_path = os.path.join(os.path.dirname(__file__), '..')
icono_ventana = b"iVBORw0KGgoAAAANSUhEUgAAAEkAAABJCAYAAABxcwvcAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAS2SURBVHja7Jw/bBRHFIe/tXwKnIRQTIEgGwGRQL4IIgFCchpMQcGfigLSXJEWOY3BDhIFvVPQIFoarqOgIkoiClsIBVDcOCffwUlGkRwllSVksJAoTHGzsF5mZnd2Z/aOu3nSSqfZ29vd377vvZk3ewNq+xr4CXgErAObA7j9DzwQ9xliYHuBhwMqStr2UNy/1s4NqTjJ7VxWgZ4D3wPbGGzbJu7zeZpQYeILs0DAcFkAzCR02BKnnsV2XGO4bTamxV9R4/4EYsGQixQArZgmBwCuxhpO4g0RoyJNZgAexxq2e30+BPNIk8cAr2IN3j5apMl6kBAn8NpsEQmAEa9FunmRvEh2bNTS71Q1w5e3wIbD31fZOvDOdhQvkt3mUwaMRRPCXIHB6l2gbloKSepSVKRqhgut9VCk+DZvcC0fjrMRkyYzfOdMn4SXSWBZiB6Uidt8xqcY9IEnJTEMysCtqnBp28jNKW5yTLGFwIT4jk6os2WIdFZxYtnFTVsWaS7jsWMp3l5xLZLs5FXxFG0iV0SkaLilEmrCZeCuSoL2gugTLSqOGe/hOKyuKYs463FPKp44ohPX6LMstwq8lLQfc5ndVKhFZhO5orilZUknuIUa1CLrN+RU9tIVbqc0qNHHyMkmHu+5wm0lBTXbyNnArWLYVyqEW4iYQUi4rGykv9RHyJ1WtD91gZsMtRuK726IWNVr5GrAr5L2BrDmAjcZaqFhr9wUuby4BZrzq0LEJ7qMWkJtVXPMgga5VsEgPKbYd0h0Em9qjv/WpBho4kl1ydOo5+xTTRf0pLzbSsbBdu6xmylqtpCzJVJdM6C1IlKoeCpFqpe1EkRaEV2RiiHOuboAJlmtn7LcAeCCjRFymicFiqdkUlwvglyW7BaI66lrPKri0pPGFWOeVYOT/u24Y7kprqchMpfMo+7k+eGsIsmwuGWpVPGjA8RaCqHqmiJbIdwC7NWsVShULOBmEvArtnFT4bBMvhkKmR13FLRVQv5gG7cyMtCUo99dA36RtN817RLocAso793piqNSyZimY2kFtzJLGsf71ZtGc6C2kKUGk2IXJQPlKeCJw9j0syI2NYrgZjOrFc1yNiqTppkuE24q1NoWRJovGblCmU4nkqyTdwU7b+n+W3KWi2JTI29skuGmKppPWLzoaQP3tzXvVjPIdKm4qdx+0aJIv/UAuZaiGqH1phEDt29g8R1ETWxziRzA5TyxKYlbGaiZImcLt3jiSDuvFrcyUOslcsbe5P82oSfMqJ401OZF8iJ5kbxIXiQvkhfJi+RNbqPAf8CeQbqpw+MHa8BOMZTaTXf6+xXwD7BP7FsCvgNotjtPJCORyF6PsHX6eSDWBWi2Oy26M8Y7gCPAC+B6s93ZEPu+pPuK9SIwdXj8YHJA/UXs89II8Ees4cSAeFIAhM12Z43u2zBV4HexL6RbU9olBtK3JVWHo7HP9wO6a5VEc/RtunPom5+5SHPAfeFBh2K7VunO1PwpPh8BdjXbnUYCtWU+1vi/iXbEV72ZHfI4LV31Bvz6SZEHaddPAjiPX4krfv/nVQdcxK/ntglcSlP2K4Z7dUCj9QP2C0YfAW8GVJQ34v5mxP1K7f0A2wJqfDSaFUAAAAAASUVORK5CYII="
def main(guardado):
    """
    Desarrollo del juego y tablero principal
    """
    colores = cm.cargar_colores()
    import random
    #-----------------------------------------------------------
        #Configuracion de bolsa puntos y Imagen de numeros
    #-----------------------------------------------------------
    bolsa = {"E":0,"A":0,"I":0,"O":0,"U":0,"S":0,"N":0,"R":0,"L":0,"T":0,"C":0,"D":0,"M":0,"B":0,
        "G":0,"P":0,"F":0,"H":0,"V":0,"J":0,"Y":0,"K":0,"Ñ":0,"Q":0,"W":0,"X":0,"Z":0,"LL":0,"RR":0}
    puntos_por_letra = {"E":0,"A":0,"I":0,"O":0,"U":0,"S":0,"N":0,"R":0,"L":0,"T":0,"C":0,"D":0,"M":0,"B":0,
        "G":0,"P":0,"F":0,"H":0,"V":0,"J":0,"Y":0,"K":0,"Ñ":0,"Q":0,"W":0,"X":0,"Z":0,"LL":0,"RR":0}

    img_nros = {1: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'uno.png'),
                2: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'dos.png'),
                3: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'tres.png'),
                4: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'cuatro.png'),
                5: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'cinco.png'),
                6: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'seis.png'),
                7: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'siete.png'),
                8: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'ocho.png'),
                9: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'nueve.png'),
                10: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'diez.png'),
                11: os.path.join(absolute_path, 'lib', 'media', 'nros_png', 'vacio.png')}

    bolsa , puntos_por_letra, tiempo ,dificultad, config, pred= cm.cargar_configuraciones(bolsa,puntos_por_letra,guardado)
    # ----------------------------------------------------------------------
        #Cargo dificultad para despues diferenciar que tablero cargar y mandarselo al objeto
        #Abro el tablero correspondiente a la dificultad seleccionada
    # ----------------------------------------------------------------------
    if (guardado): #Si hay partida guardada carga el tablero guardado
        tab = cm.cargar_tablero("guardado")
    else:
        try:
            if(dificultad == "facil"):
                tab = cm.cargar_tablero("facil")
            elif (dificultad == "medio"):
                tab = cm.cargar_tablero("medio")
            else:
                tab = cm.cargar_tablero("dificil")
        except (FileNotFoundError):
            sg.popup("No se ha encontrado el tablero",keep_on_top=True)
    # ----------------------------------------------------------------------
        # Opciones de dificultad --> lista de tags
    # ----------------------------------------------------------------------
    dificultad_random = {'sust': ["NC", "NN", "NCS", "NCP", "NNS", "NP", "NNP", "W"],
                         'adj': ["JJ", "AO", "AQ", "DI", "DT"],
                         'verbo': ["VAG", "VBG", "VAI", "VAN", "MD", "VAS", "VMG", "VMI",
                          "VB", "VMM", "VMN", "VMP", "VBN", "VMS", "VSG", "VSI", "VSN", "VSP", "VSS"]}
    if dificultad == "dificil":
        tipo_palabra = random.choice(list(dificultad_random.keys()))
        tipo = dificultad_random[tipo_palabra]
    elif dificultad == 'facil':
        tipo_palabra = ""
        tipo = dificultad_random['sust'] + dificultad_random['adj'] + dificultad_random['verbo']
    else:
        tipo_palabra = ""
        tipo = dificultad_random['adj'] + dificultad_random['verbo']

    if not(guardado):
        nombre = sg.popup_get_text("ScrabbleAR está por comenzar, ingrese su nombre de jugador", title="Ingrese su nombre", default_text="Invitado",size=(None, None),keep_on_top=True)
        if nombre == None or nombre == "":
            nombre = "Invitado"
    else:
        nombre = config["nombre"]
    #Instanciacion de objetos y creacion del layout
    palabras_usadas = []
    layout, letras, letras_pc, botones, long_tablero = gm.crear_layout(bolsa,tab ,dificultad, tipo_palabra, img_nros, puntos_por_letra, nombre, palabras_usadas)  # botones es un diccionario de pares (tupla, valor)
    from JugadorPC import PC
    from Jugador import Jugador
    pj = Jugador(letras,long_tablero,botones,puntos_por_letra,dificultad,tipo,guardado)
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
    window = sg.Window("Ventana de juego", layout, icon=icono_ventana)
    letras_usadas = {}  # pares (clave, valor) de las letras seleccionadas del atril
    palabra_nueva = {}  # pares (clave, valor) de las letras colocadas en el tablero
    puntos_jugador = dict()
    puntos_jugador = cm.cargar_puntuaciones()
    lista_puntajes = puntos_jugador["puntos"]
    terminar = False
    if (guardado):
        primer_turno = False
    else:
        primer_turno = True
    cambios_de_fichas = 3
    posiciones_ocupadas_tablero = []  # aca vamos almacenando las posiciones (i,j) ocupadas en el tablero
    fin_fichas = False
    fin_juego = False
    guardar_partida = False
    #Configuracion del tiempo
    if not(guardado):
        cont_tiempo_min_config = tiempo
        cont_tiempo_min = round(cont_tiempo_min_config / 60)
        if (cont_tiempo_min > 0):
            cont_tiempo_seg = 59
            cont_tiempo_min -= 1
        else:
            cont_tiempo_seg = 0
    else:
        aux_tiempo = config["tiempo"].split(":")
        cont_tiempo_min = int(aux_tiempo[0])
        cont_tiempo_seg = int(aux_tiempo[1])
    window.finalize()
    # se decide de forma aleatoria quien comienza la partida si no se abrio el archivo guardado
    if guardado:
        turno_pc = True if config["turno_pc"] == "True" else False
        turno_jugador = True if config["turno_jugador"] == "True" else False
    else:
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
        # print("POS: ",event)
        if (cont_tiempo_seg == 0):
            cont_tiempo_seg = 59
            cont_tiempo_min -= 1 if cont_tiempo_min -1 > 0 else 0
        else:
            cont_tiempo_seg -= 1
        if (cont_tiempo_seg < 10):
            tiempo_seg_final = "0" + str(cont_tiempo_seg)
        else:
            tiempo_seg_final = cont_tiempo_seg
        tiempo_str = "{}:{}".format(cont_tiempo_min,tiempo_seg_final)
        window["tiempo"].update(tiempo_str)
        if (cont_tiempo_min == 0) and (cont_tiempo_seg == 0):
            sg.popup("Se termino el tiempo",keep_on_top=True)
            fin_juego = True
        #------------------------------------------------------
            # mientras sea el turno del jugador, podrá realizar
            # todos los eventos del tablero
        #------------------------------------------------------
        if turno_jugador:
            if event is None or terminar:
                guardar_partida = gm.salir_del_juego()
                if not guardar_partida:
                    sg.popup_no_frame('Salió de la partida', keep_on_top=True)
                    break
            # botones del atril del jugador
            if event in letras.keys():
                window['-d'].update(disabled=False)
                for botoncito in ['-c','-cf','-p','-t','-paso','como_jugar','botonera','ver_config']:
                    window[botoncito].update(disabled=True)
                box = event  # letra seleccionada
                letras_usadas[box] = letras[box]
                window[box].update(button_color=('white', '#55a4fc'))    #al seleccionado se le cambia el color
                for val in letras.keys():
                    window[val].update(disabled=True)  # desactivo los botones de las fichas
                if (cont_tiempo_seg == 0):
                    cont_tiempo_seg = 59
                    cont_tiempo_min -= 1
                else:
                    cont_tiempo_seg -= 1
                
                event, values = window.read()
                if event in botones.keys():
                # refresco la tabla en la casilla seleccionada con la letra elegida antes
                    window[box].update(button_color=('white', '#006699'))      #se le devuelve el color
                    ind = event  # casilla seleccionada
                    palabra_nueva[ind] = letras[box]
                    if len(palabra_nueva.keys()) > 1:
                        window["-c"].update(disabled=False) # recien ahora puede confirmar
                    window[ind].update(letras[box], disabled=True, button_color = ("black",colores["letra_jugador"]))  # actualizo la casilla y la desactivo
                    botones = pc.get_botones().copy()
                    botones[ind] = letras[box] + "/"
                    pc.actualiza_botones(botones)
                    for val in letras.keys():
                        if val not in letras_usadas.keys():
                            window[val].update(disabled=False)  # refresco la tabla B
                    for botoncito in ['-cf','-p','-t','-paso','como_jugar','botonera','ver_config']:
                        window[botoncito].update(disabled=False)
                if event is None:
                    terminar = True
            # boton de deshacer las palabras puestas en el tablero
            if event == "-d":
                letras_usadas, palabra_nueva = gm.sacar_del_tablero(window, letras.keys(), palabra_nueva, botones_aux, dificultad)
            # boton de pasar el turno a la pc
            elif event == "-paso":
                turno_jugador, turno_pc= gm.cambiar_turno(turno_jugador ,turno_pc, window)
                letras_usadas, palabra_nueva = gm.sacar_del_tablero(window, letras.keys(), palabra_nueva, botones_aux, dificultad)
            #boton cambio de fichas
            elif (event == "-cf") and (cambios_de_fichas != 0):
                letras_usadas, palabra_nueva = gm.sacar_del_tablero(window, letras.keys(), palabra_nueva, botones_aux, dificultad) #si ya hay fichas jugadas en el tablero volveran al atril
                letras_a_cambiar=[]
                window["-c"].update(disabled=True)  #los desactivo para que no se toque nada que no sean las fichas a cambiar
                window["-d"].update(disabled=True)  #-c y -d no los vuelvo a activar porque los quiero desactivados cuando empiece el sigueinte turno
                window["-paso"].update(disabled=True)
                window["-p"].update(disabled=True)
                window["-t"].update(disabled=True)
                #window.Disable() # desactivamos la ventana del juego durante el popup
                #window.Disappear() #alternativa a disable() y enable() si no se puede hacer funcionar esas funciones en linux
                sg.Popup('Cambio de fichas:',
                             'Seleccione las letras que quiere cambiar o el boton ',
                             '\"seleccionar todas las fichas\" y vuelva a clickear en ',
                             '\"Cambiar fichas\" para confirmar el cambio',keep_on_top=True)
                #window.enable()
                #window.Reappear()
                event, values = window.read()
                if not event is None:
                    window.BringToFront() # para que no se minimice despues del popup
                    window["-selec"].update(visible=True)
                    window["-deshacer-selec"].update(visible=True)
                    cerro_ventana = False
                    while True:
                        event = window.read()[0]
                        if event is None:
                            cerro_ventana = True
                            break
                        if event in letras.keys():
                            letras_a_cambiar.append(event)
                            window[event].update(disabled=True)
                        elif event == "-selec":
                            for ficha in letras.keys():
                                if ficha not in letras_a_cambiar:
                                    letras_a_cambiar.append(ficha)
                                    window[ficha].update(disabled=True)
                        elif event == "-deshacer-selec":
                            for ficha in letras_a_cambiar:
                                window[ficha].update(disabled=False)
                            letras_a_cambiar = []
                        elif event == "-cf":
                            window["-selec"].update(visible=False)
                            window["-deshacer-selec"].update(visible=False)
                            if letras_a_cambiar:
                                letras= gm.devolver_fichas(letras,letras_a_cambiar,bolsa)
                                gm.dar_fichas(letras,bolsa)
                                pj.setFichas(letras)
                                for f in letras_a_cambiar:
                                    window[f].update(letras[f], image_size=(50, 50), image_subsample=21, image_filename=img_nros[puntos_por_letra[letras[f]]], disabled=False)
                                cambios_de_fichas -= 1
                                window["cfichas"].update(str(cambios_de_fichas))
                                if cambios_de_fichas == 0:
                                    window["-cf"].update(disabled=True)
                                    window["-cf"].set_tooltip('Ya realizaste 3 cambios de fichas.')
                                # print("Cambio de letras realizado.")
                            #else:
                            #      print("No se selecciono ninguna letra, no se realizo ningun cambio.")
                            #    pass
                            break
                    if not cerro_ventana:
                        turno_jugador,turno_pc= gm.cambiar_turno(turno_jugador,turno_pc, window)
                        window["-paso"].update(disabled=False)
                        window["-p"].update(disabled=False)
                        window["-t"].update(disabled=False)
            # boton de guardar partida
            elif event == "-p" or guardar_partida:
                boton = pc.get_botones()
                cm.guardar_partida(boton)
                datos = dict()
                datos = config
                datos["tiempo"] = tiempo_str
                datos["puntos_j"] = pj.puntos
                datos["puntos_pc"] = pc.puntos
                datos["nombre"] = nombre
                datos["turno_jugador"] = str(turno_jugador)
                datos["turno_pc"] = str(turno_pc)
                pc.guardar_estado()
                pj.guardar_info()
                cm.guardar_info_partida(datos)
                sg.popup_no_border("Partida guardada",keep_on_top=True,auto_close_duration=2)
                break
            # boton de terminar partida
            elif event == "-t" or fin_fichas or fin_juego:
                seguir = False
                if event == "-t": # le preguntamos si realmente quiere finalizar el juego
                    #window.Disable() # desactivamos la ventana del juego pa que no se le ocurra cerrar con la otra ventana activa
                    seguir = gm.preguntar_si_sigue_el_juego()
                    #window.enable()
                    window.BringToFront()
                if not seguir:
                    pj.restar_puntos_finales()
                    pc.restar_puntos_finales()
                    gm.mostrar_fichas_compu(window, pc.getFichas(), img_nros, puntos_por_letra)
                    if (pj.puntos > pc.puntos):
                        sg.popup_no_frame("Termino el juego \nTus puntos vs Puntos PC ",
                                    "     "+str(pj.puntos)+"         |        "+str(pc.puntos),
                                        " Ganaste!",keep_on_top=True)
                    elif (pj.puntos == pc.puntos):
                        sg.popup("Termino el juego \nTus puntos vs Puntos PC ",
                                 "     "+str(pj.puntos)+"         |        "+str(pc.puntos),
                                 " EMPATE!",keep_on_top=True)
                    else:
                        sg.popup_no_frame("Termino el juego \nTus puntos vs Puntos PC \n",
                                         "     "+str(pj.puntos)+"         |        "+str(pc.puntos),
                                         " Perdiste :(",keep_on_top=True)
                    from datetime import datetime
                    fecha =  datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                    # puntos_jugador[fecha] = pj.puntos
                    if nombre != None: # solo guarda si le pone un nombre
                        datos = nombre+" - "+str(fecha)+" - "+str(pj.puntos)+" - "+ str(dificultad)
                        lista_puntajes.append(datos)
                        puntos_jugador["puntos"] = lista_puntajes
                        cm.guardar_puntuaciones(puntos_jugador)
                    sg.popup_no_frame("Volveras al menu",auto_close=True,auto_close_duration=5,button_type=None,keep_on_top=True)
                    if (guardado):
                        #Si termine la partida guardada la borro
                        os.remove(os.path.join(absolute_path, "lib","info","saves","datos_guardados.json"))
                        os.remove(os.path.join(absolute_path, "lib","info","saves","datos_pc.json"))
                        os.remove(os.path.join(absolute_path, "lib","info","saves","guardado.json"))
                    break
            # boton de confirmar palabra
            elif event == "-c":
                #window.Disable()
                window["-c"].update(disabled=True)
                # vamos a analizar si la palabra fue posicionada correctamente (misma fila y columnas contiguas):
                posiciones_ocupadas_tablero = pc.get_pos_tablero()
                letras_usadas, palabra_nueva, turno_jugador, turno_pc, fin_fichas = gm.confirmar_palabra(window, letras, botones, palabra_nueva, letras_usadas, puntos_por_letra, pj, posiciones_ocupadas_tablero, bolsa, primer_turno, img_nros, botones_aux, dificultad, pc)
                pc.actualizar_pos_tablero(posiciones_ocupadas_tablero)
                if primer_turno and turno_pc:  # si le da confirmar y está mal la palabra, no deja de ser su primer turno
                    primer_turno = False
                window["p_j"].update(str(pj.puntos))
                #window.enable()
                window.BringToFront()
            elif event == "como_jugar":
                sg.popup(cm.empezando_la_partida(),title="Como jugar")
            elif event == "botonera":
                sg.popup(cm.botones_especiales(),title="Botones especiales")
            elif event == "ver_config":
                sg.popup(cm.get_config_actual(guardado,pred),title="Config del juego")
        if turno_pc:
            time.sleep(1)   #maquina pensando la jugarreta
            primer_turno = pc.jugar(window,primer_turno)
            fichas_pc = pc.getFichas()
            gm.dar_fichas(fichas_pc, bolsa)
            pc.setFichas(fichas_pc)
            fin_fichas = gm.pocas_fichas(pc.getFichas())
            # finaliza y actualizamos los turnos: turno_pc = False, turno_jugador = True
            turno_jugador, turno_pc = gm.cambiar_turno(turno_jugador ,turno_pc, window)

    window.close()
    ScrabbleAR.main()
# if __name__ == "__main__":
#     main(True)
