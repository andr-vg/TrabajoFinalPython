import PySimpleGUI as sg
import time
import os
import ScrabbleAR   #-----------------> Menu del juego
import GameConfigManager as cm #---------> Manejo de configuraciones
import GameManager as gm
import Icono

absolute_path = os.path.join(os.path.dirname(__file__), '..')
icono_ventana = Icono.obtener_logo()

# --------------------------------------------------------------
    # Funciones a usar en el main
# --------------------------------------------------------------

def contar_tiempo(cont_tiempo_min, cont_tiempo_seg):
    """
    Devuelve los tiempos actuales del juego
    """
    if cont_tiempo_seg == 0:
        cont_tiempo_seg = 59
        if cont_tiempo_min - 1 <= 0:
            cont_tiempo_min =0
            print(cont_tiempo_min)
        else:
            cont_tiempo_min -= 1
    else:
        cont_tiempo_seg -= 1
    if cont_tiempo_seg < 10:
        tiempo_seg_final = '0' + str(cont_tiempo_seg)
    else:
        tiempo_seg_final = cont_tiempo_seg
    return cont_tiempo_min, cont_tiempo_seg, tiempo_seg_final

def seleccion_de_fichas(window, event, letras_usadas, palabra_nueva, letras, botones,
                        terminar, cont_tiempo_seg, cont_tiempo_min, colores):
    """
    El jugador selecciona las fichas que quiere formar y las dispone
    en el tablero.
    """
    window['-d'].update(disabled=False)
    for botoncito in ['-c', '-cf', '-p', '-t', '-paso', 'como_jugar',
                        'botonera', 'ver_config']:
        window[botoncito].update(disabled=True)
    box = event  # letra seleccionada
    letras_usadas[box] = letras[box]
    # al seleccionado se le cambia el color
    window[box].update(button_color=('white', '#55a4fc'))
    # desactivo los botones de las fichas
    for val in letras.keys():
        window[val].update(disabled=True)
    if cont_tiempo_seg == 0:
        cont_tiempo_seg = 59
        cont_tiempo_min -= 1
    else:
        cont_tiempo_seg -= 1

    event, values = window.read()
    if event in botones.keys():
        # refresco la tabla en la casilla seleccionada
        # con la letra elegida antes
        # se le devuelve el color
        window[box].update(button_color=('white', '#006699'))
        ind = event  # casilla seleccionada
        palabra_nueva[ind] = letras[box]
        if len(palabra_nueva.keys()) > 1:
            # recien ahora puede confirmar
            window['-c'].update(disabled=False)
        # actualizo la casilla y la desactivo
        window[ind].update(letras[box], disabled=True,
        button_color = ('black', colores['letra_jugador']))

        for val in letras.keys():
            if val not in letras_usadas.keys():
                # refresco la tabla B
                window[val].update(disabled=False)
        for botoncito in ['-cf', '-p', '-t', '-paso', 'como_jugar',
                        'botonera','ver_config']:
            window[botoncito].update(disabled=False)
    # si cierra abruptamente nos dirigimos directamente a terminar
    if event is None:
        terminar = True
    return cont_tiempo_seg, cont_tiempo_min, terminar

def mostrar_popups_info (event,guardado,pred):
    """
    Muestra los popups correspondientes de cada boton
    """
    if event == 'como_jugar':
        sg.popup(cm.empezando_la_partida(), title='Como jugar')
    elif event == 'botonera':
        sg.popup(cm.botones_especiales(), title='Botones especiales')
    elif event == 'ver_config':
        cm.get_config_actual(guardado,pred)

def cambio_de_fichas(window, letras, cambios_de_fichas, gm, pj, bolsa,
                    img_nros, puntos_por_letra, turno_pc, turno_jugador, guardado, pred):
    """
    Se realizan los cambios de fichas que desea el jugador y éste pierde un turno
    """
    letras_a_cambiar=[]
    for elem in ['-c', '-d', '-paso', '-p', '-t']:
        window[elem].update(disabled=True)
    for elem in ['-selec', '-deshacer-selec']:
        window[elem].update(visible=True)
    sg.Popup('Cambio de fichas:',
        'Seleccione las letras que quiere cambiar o el boton ',
        '\"seleccionar todas las fichas\" y vuelva a clickear',
        'en \"Cambiar fichas\" para confirmar el cambio',
        keep_on_top=True)
    # para que no se minimice despues del popup
    window.BringToFront()
    cerro_ventana = False
    while True:
        event = window.read()[0]
        if event is None:
            cerro_ventana = True
            break
        elif event in letras.keys():
            letras_a_cambiar.append(event)
            window[event].update(disabled=True)
        elif event == '-selec':
            for ficha in letras.keys():
                if ficha not in letras_a_cambiar:
                    letras_a_cambiar.append(ficha)
                    window[ficha].update(disabled=True)
        elif event == '-deshacer-selec':
            for ficha in letras_a_cambiar:
                window[ficha].update(disabled=False)
            letras_a_cambiar = []
        elif event == '-cf':
            window['-selec'].update(visible=False)
            window['-deshacer-selec'].update(visible=False)
            if letras_a_cambiar:
                letras = gm.devolver_fichas(letras, letras_a_cambiar, bolsa)
                gm.dar_fichas(letras,bolsa)
                pj.setFichas(letras)
                for f in letras_a_cambiar:
                    window[f].update(letras[f],  disabled=False,
                        image_size=(50, 50), image_subsample=21,
                        image_filename=img_nros[puntos_por_letra[letras[f]]])
                cambios_de_fichas -= 1
                window['cfichas'].update(str(cambios_de_fichas))
                if cambios_de_fichas == 0:
                    window['-cf'].update(disabled=True)
                    window['-cf'].set_tooltip(
                        'Ya realizaste 3 cambios de fichas.')
            break
        else:
            mostrar_popups_info(event,guardado,pred)
    if not cerro_ventana:
        turno_jugador, turno_pc = gm.cambiar_turno(turno_jugador, turno_pc,
                                    window)
        window['-paso'].update(disabled=False)
        window['-p'].update(disabled=False)
        window['-t'].update(disabled=False)
    return cambios_de_fichas, turno_pc, turno_jugador

def guardar_datos(config, tipo_palabra, tiempo_str, pj_puntos, pc_puntos,
                    nombre, turno_jugador, turno_pc, cambios_de_fichas, primer_turno):
    """
    Función que guarda los datos al posponer partida
    """
    #datos = dict()
    datos = config
    datos['tipo'] = tipo_palabra
    datos['tiempo'] = tiempo_str
    datos['puntos_j'] = pj_puntos
    datos['puntos_pc'] = pc_puntos
    datos['nombre'] = nombre
    datos['turno_jugador'] = str(turno_jugador)
    datos['turno_pc'] = str(turno_pc)
    datos['cambios_fichas'] = cambios_de_fichas
    datos['primer_turno'] = str(primer_turno).capitalize()
    return datos

def posponer_partida(pc, pj, cm, config, tipo_palabra, tiempo_str,
                    nombre, turno_jugador, turno_pc, cambios_de_fichas,primer_turno):
    """
    funcion de posponer y guardar partida
    """
    boton = pc.get_botones()
    cm.guardar_partida(boton)
    datos = guardar_datos(config, tipo_palabra, tiempo_str, pj.puntos,
            pc.puntos, nombre, turno_jugador, turno_pc, cambios_de_fichas,primer_turno)
    pc.guardar_estado()
    pj.guardar_info()
    cm.guardar_info_partida(datos)
    sg.popup_no_border('Partida guardada', keep_on_top=True,
                        auto_close_duration=2)

def finalizar_juego(pj, pc, gm, cm, window, img_nros, puntos_por_letra, nombre,
        dificultad, lista_puntajes, puntos_jugador, guardado, absolute_path):
    """
    Funcion que se ocupa de realizar los calculos finales y guardar en top_10
    al finalizar la partida
    """
    import time
    pj.restar_puntos_finales()
    pc.restar_puntos_finales()
    gm.mostrar_fichas_compu(window, pc.getFichas(), img_nros, puntos_por_letra)
    # popup_animated using built-in GIF image
    cubito = Icono.obtener_gif()
    for i in range(30000):
        sg.popup_animated(cubito, title='ScrabbleAR', text_color='white', background_color='#8fa8bf',
                        message='              RECALCULANDO PUNTAJE        \n                                    ...                       \nDescontando puntaje de las fichas del atril..',
                      font=('Century Gothic',13), no_titlebar=True,
                      alpha_channel=0.9, time_between_frames=100, keep_on_top=True)
    sg.popup_animated(None)  # close all Animated Popups
    if pj.puntos > pc.puntos:
        ganador = 'Invitado' if nombre == None else nombre
        puntos = pj.puntos
        mensaje = 'GANASTE! :)'
    elif pj.puntos == pc.puntos:
        ganador = 'Empate'
        puntos = pj.puntos
        mensaje = 'EMPATE!'
    else:
        ganador = 'Maquina'
        puntos = pc.puntos
        mensaje = 'PERDISTE :('
    gm.mostrar_puntajes_finales(pj.puntos, pc.puntos, mensaje)
    if puntos > 0:
        from datetime import datetime
        fecha =  datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        datos = ganador + ' - ' + str(fecha) + ' - ' + str(puntos) + \
            ' - ' + str(dificultad)
        lista_puntajes.append(datos)
        puntos_jugador['puntos'] = lista_puntajes
        cm.guardar_puntuaciones(puntos_jugador)
    sg.popup_no_frame('Volveras al menu', auto_close=True,
                auto_close_duration=5, button_type=None,
                keep_on_top=True)
    if guardado:
        # Si termine la partida guardada la borro
        os.remove(os.path.join(absolute_path, 'lib', 'info', 'saves',
                                'datos_guardados.json'))
        os.remove(os.path.join(absolute_path, 'lib', 'info', 'saves',
                                'datos_pc.json'))
        os.remove(os.path.join(absolute_path, 'lib', 'info', 'saves',
                                'guardado.json'))

def analizar_palabra(window, letras, botones, palabra_nueva, letras_usadas,
                    puntos_por_letra, pj, pc, bolsa, primer_turno, img_nros,
                    botones_aux, turno_pc, dificultad):
    """
    Acá analizamos si la palabra que confirmo el jugador es correcta
    tanto en ubicación como en el tipo pedido segun dificultad
    """
    window['-c'].update(disabled=True)
    # vamos a analizar si la palabra fue posicionada
    # correctamente (misma fila y columnas contiguas):
    posiciones_ocupadas_tablero = pc.get_pos_tablero()
    # confirmamos que sea correcta o no la palabra y lugares:
    letras_usadas, palabra_nueva, turno_jugador, turno_pc, fin_fichas = \
        gm.confirmar_palabra(window, letras, botones, palabra_nueva,
        letras_usadas, puntos_por_letra, pj, posiciones_ocupadas_tablero,
        bolsa, primer_turno, img_nros, botones_aux, dificultad, pc)
    pc.actualizar_pos_tablero(posiciones_ocupadas_tablero)
    # si le da confirmar y está mal la palabra, no deja de ser su primer turno
    if primer_turno and turno_pc:
        primer_turno = False
    window['p_j'].update(str(pj.puntos))
    window.BringToFront()
    return letras_usadas, palabra_nueva, turno_jugador, turno_pc, fin_fichas, primer_turno
# --------------------------------------------------------------
    # Main del juego
# --------------------------------------------------------------

def main(guardado):
    """
    Desarrollo del juego y tablero principal
    """
    colores = cm.cargar_colores()
    import random
    #-----------------------------------------------------------
        # Configuracion de bolsa puntos y Imagen de numeros
    #-----------------------------------------------------------
    bolsa = {'E': 0, 'A': 0, 'I': 0, 'O': 0, 'U': 0, 'S': 0, 'N': 0, 'R': 0,
             'L': 0, 'T': 0, 'C': 0, 'D': 0, 'M': 0, 'B': 0, 'G': 0, 'P': 0,
             'F': 0, 'H': 0, 'V': 0, 'J': 0, 'Y': 0, 'K': 0, 'Ñ': 0, 'Q': 0,
             'W': 0, 'X': 0, 'Z': 0, 'LL': 0, 'RR': 0}

    puntos_por_letra = {'E': 0, 'A': 0, 'I': 0, 'O': 0, 'U': 0, 'S': 0,
                        'N': 0, 'R': 0, 'L': 0, 'T': 0, 'C': 0, 'D': 0,
                        'M': 0, 'B': 0, 'G': 0, 'P': 0, 'F': 0, 'H': 0,
                        'V': 0, 'J': 0, 'Y': 0, 'K': 0, 'Ñ': 0, 'Q': 0,
                        'W': 0, 'X': 0, 'Z': 0, 'LL': 0, 'RR': 0}

    img_nros = {1: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'uno.png'),
                2: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'dos.png'),
                3: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'tres.png'),
                4: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'cuatro.png'),
                5: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'cinco.png'),
                6: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'seis.png'),
                7: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'siete.png'),
                8: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'ocho.png'),
                9: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'nueve.png'),
                10: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'diez.png'),
                11: os.path.join(absolute_path, 'lib', 'media', 'nros_png',
                'vacio.png')}

    # cargamos las configuraciones correspondientes
    bolsa, puntos_por_letra, tiempo, dificultad, config, pred = \
    cm.cargar_configuraciones(bolsa, puntos_por_letra, guardado)
    # ----------------------------------------------------------------------
        # Cargo dificultad para despues diferenciar que tablero cargar y
        # mandarselo al objeto
        # Abro el tablero correspondiente a la dificultad seleccionada
    # ----------------------------------------------------------------------
    if guardado: #Si hay partida guardada carga el tablero guardado
        tab = cm.cargar_tablero('guardado')
    else:
        if dificultad == 'facil':
                tab = cm.cargar_tablero('facil')
        elif dificultad == 'medio':
                tab = cm.cargar_tablero('medio')
        else:
                tab = cm.cargar_tablero('dificil')
    if (tab is None):
        sg.popup(f'No se encontro el tablero {dificultad}')
        ScrabbleAR.main()
        return None

    # ----------------------------------------------------------------------
        # Opciones de dificultad --> lista de tags
    # ----------------------------------------------------------------------
    dificultad_random = {
                'sust': ['NC', 'NN', 'NCS', 'NCP', 'NNS', 'NP', 'NNP', 'W'],
                'adj': ['JJ', 'AO', 'AQ', 'DI', 'DT'],
                'verbo': ['VAG', 'VBG', 'VAI', 'VAN', 'MD', 'VAS', 'VMG',
                          'VMI', 'VB', 'VMM', 'VMN', 'VMP', 'VBN', 'VMS',
                          'VSG', 'VSI', 'VSN', 'VSP', 'VSS']}
    if dificultad == 'dificil':
        tipo_palabra = random.choice(list(dificultad_random.keys())) \
        if not guardado else config['tipo']
        tipo = dificultad_random[tipo_palabra]
    elif dificultad == 'facil':
        tipo_palabra = ''
        tipo = dificultad_random['sust'] + dificultad_random['adj'] + \
               dificultad_random['verbo']
    else:
        tipo_palabra = ''
        tipo = dificultad_random['adj'] + dificultad_random['verbo']
    if not guardado:
        nombre = sg.popup_get_text('ScrabbleAR está por comenzar, ingrese su nombre de jugador', title='Ingrese su nombre',
                default_text='Invitado', size=(None, None), keep_on_top=True)
        if nombre in (None, ''):
            nombre = 'Invitado'
    else:
        nombre = config['nombre']
    # ----------------------------------------------------------------------
    # Instanciacion de objetos y creacion del layout
    # ----------------------------------------------------------------------
    palabras_usadas = []
    palabras_usadas_pc = []
    layout, letras, letras_pc, botones, long_tablero = gm.crear_layout(bolsa,
    tab, dificultad, tipo_palabra, img_nros, puntos_por_letra, nombre,
    palabras_usadas, palabras_usadas_pc, guardado)

    from JugadorPC import PC
    from Jugador import Jugador
    window = sg.Window('Ventana de juego', layout, icon=icono_ventana,
                        finalize=True)
    pj = Jugador(letras, long_tablero, botones, puntos_por_letra, dificultad,
                 tipo, guardado, window)
    pc = PC(letras_pc, long_tablero, botones, puntos_por_letra, dificultad,
            tipo, guardado,window)
    botones_aux = botones.copy() #-----> Botones_aux lo uso para el boton deshacer

    # ----------------------------------------------------------------------
        # Manejo de puntajes, si hay partida guardada setea los puntos
        # Sino es 0
    # ----------------------------------------------------------------------
    if guardado:
        pj.puntos = int(config['puntos_j'])
        pc.puntos = int(config['puntos_pc'])
        window['p_pc'].update(pc.getPuntos())
        window['p_j'].update(pj.getPuntos())

    # ----------------------------------------------------------------------
        #Configuracion de ventana y turnos
    # ----------------------------------------------------------------------

    letras_usadas = {} # pares (clave, valor) de las letras selecs del atril
    palabra_nueva = {} # pares (clave, valor) de las letras puestas en el tab
    puntos_jugador = dict()
    puntos_jugador = cm.cargar_puntuaciones()
    lista_puntajes = puntos_jugador['puntos']
    terminar = False
    # cambios de fichas
    if guardado:
        cambios_de_fichas = int(config["cambios_fichas"])
        window["cfichas"].update(cambios_de_fichas)
        if cambios_de_fichas == 0:
            window["-cf"].update(disabled=True)
    else:
        cambios_de_fichas = 3
    # aca vamos almacenando las posiciones (i,j) ocupadas en el tablero:
    # posiciones_ocupadas_tablero = []
    fin_fichas = False
    fin_juego = False
    guardar_partida = False
    # Configuracion del tiempo
    if not guardado:
        tiempo = tiempo.split(":")
        cont_tiempo_min = int(tiempo[0])
        if cont_tiempo_min > 0:
            cont_tiempo_seg = 59
            cont_tiempo_min -= 1
        else:
            cont_tiempo_seg = 0
    else:
        aux_tiempo = config['tiempo'].split(':')
        cont_tiempo_min = int(aux_tiempo[0])
        cont_tiempo_seg = int(aux_tiempo[1])
    window.finalize()
    # se decide de forma aleatoria quien comienza la partida si no se abrio
    # el archivo guardado
    if guardado:
        primer_turno = True if config['primer_turno'] == 'True' else False
        turno_pc = True if config['turno_pc'] == 'True' else False
        turno_jugador = True if config['turno_jugador'] == 'True' else False
    else:
        primer_turno = True
        turno = random.choice([True, False])
        turno_jugador,turno_pc = gm.cambiar_turno(turno,not(turno), window)
        sg.popup("Se eligió aleatoriamente que {} coloque sus fichas en el primer turno.".format('la maquina' if turno_pc else 'el jugador \''+nombre+'\''),
                 '¡A jugar!', title='Empieza la partida', line_width=100)

    if (dificultad == 'dificil'):
        if (tipo_palabra == 'sust'):
            sg.Popup('Dificultad: Dificil, tipo de palabras: solo sustantivos',no_titlebar=True,keep_on_top=True)
        elif (tipo_palabra == 'adj'):
            sg.Popup('Dificultad: Dificil, tipo de palabras: solo adjetivos',no_titlebar=True,keep_on_top=True)
        else:
            sg.Popup('Dificultad: Dificil, tipo de palabras: solo verbos',no_titlebar=True,keep_on_top=True)

    # ----------------------------------------------------------------------
        #Loop de ventana
    # ----------------------------------------------------------------------
    while True:
        event, values = window.read(timeout=1000)
        # actualizamos el tiempo:

        cont_tiempo_min, cont_tiempo_seg, tiempo_seg_final = contar_tiempo(
                        cont_tiempo_min, cont_tiempo_seg)
        tiempo_str = '{}:{}'.format(cont_tiempo_min, tiempo_seg_final)
        window['tiempo'].update(tiempo_str)
        # chequeamos que no se acabe el tiempo:
        if (cont_tiempo_min == 0) and (cont_tiempo_seg == 0):
            sg.popup('Se termino el tiempo', keep_on_top=True)
            # para que entre al if de terminar juego
            # dentro del if del turno_jugador
            fin_juego = turno_jugador = True
            turno_pc = False
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
            # boton de guardar partida
            if event == '-p' or guardar_partida:
                posponer_partida(pc, pj, cm, config, tipo_palabra, tiempo_str,
                    nombre, turno_jugador, turno_pc, cambios_de_fichas, primer_turno)
                break
            # si selecciona botones del atril del jugador
            elif event in letras.keys():
                cont_tiempo_seg, cont_tiempo_min, terminar = \
                    seleccion_de_fichas(window, event, letras_usadas,
                                palabra_nueva, letras, botones, terminar,
                                cont_tiempo_seg, cont_tiempo_min, colores)
            # boton de deshacer las palabras puestas en el tablero
            elif event == '-d':
                letras_usadas, palabra_nueva = gm.sacar_del_tablero(window,
                letras.keys(), palabra_nueva, botones_aux, dificultad)
            # boton de pasar el turno a la pc
            elif event == '-paso':
                turno_jugador, turno_pc = gm.cambiar_turno(turno_jugador,
                                          turno_pc, window)
                letras_usadas, palabra_nueva = gm.sacar_del_tablero(window,
                        letras.keys(), palabra_nueva, botones_aux, dificultad)
            # boton cambio de fichas
            elif (event == '-cf') and (cambios_de_fichas != 0):
                # si ya hay fichas jugadas en el tablero volveran al atril
                letras_usadas, palabra_nueva = gm.sacar_del_tablero(window,
                        letras.keys(), palabra_nueva, botones_aux, dificultad)
                cambios_de_fichas, turno_pc, turno_jugador = cambio_de_fichas(
                            window, letras, cambios_de_fichas, gm, pj, bolsa,
                            img_nros, puntos_por_letra, turno_pc, turno_jugador, guardado, pred)
            # boton de terminar partida
            elif event == '-t' or fin_fichas or fin_juego:
                seguir = False
                if event == '-t':
                    # le preguntamos si realmente quiere finalizar el juego
                    seguir = gm.preguntar_si_sigue_el_juego()
                    window.BringToFront()
                if not seguir:
                    finalizar_juego(pj, pc, gm, cm, window, img_nros,
                    puntos_por_letra, nombre, dificultad, lista_puntajes,
                    puntos_jugador, guardado, absolute_path)
                    break
            # boton de confirmar palabra
            elif event == '-c':
                letras_usadas, palabra_nueva, turno_jugador, turno_pc, \
                fin_fichas, primer_turno = analizar_palabra(
                    window, letras, botones, palabra_nueva, letras_usadas,
                    puntos_por_letra, pj, pc, bolsa, primer_turno, img_nros,
                    botones_aux, turno_pc, dificultad)
            elif event in ('como_jugar', 'botonera', 'ver_config'):
                mostrar_popups_info(event,guardado,pred)
        if turno_pc:
            time.sleep(0.5)   # maquina pensando la jugarreta
            primer_turno = pc.jugar(window, primer_turno)
            fichas_pc = pc.getFichas()
            gm.dar_fichas(fichas_pc, bolsa)
            pc.setFichas(fichas_pc)
            fin_fichas = gm.pocas_fichas(pc.getFichas())
            if (fin_fichas):
                finalizar_juego(pj, pc, gm, cm, window, img_nros,
                    puntos_por_letra, nombre, dificultad, lista_puntajes,
                    puntos_jugador, guardado, absolute_path)
                break
            else:
                turno_jugador, turno_pc = gm.cambiar_turno(turno_jugador,
                                                    turno_pc, window)
    window.close()
    ScrabbleAR.main()
