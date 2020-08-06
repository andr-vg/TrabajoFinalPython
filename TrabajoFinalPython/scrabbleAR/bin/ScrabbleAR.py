import PySimpleGUI as sg
import Juego #Programa Principal
import os
import sys
import json
import pathlib
import Icono
from GameConfigManager import empezando_la_partida
from GameConfigManager import botones_especiales
# ----------------------------------------------------------------------
#Path making
absolute_path = os.path.join(os.path.dirname(__file__), '..')
icono_ventana = Icono.obtener_logo()
# print("ABSOLUTE PATH: ",absolute_path)
logo = os.path.join(absolute_path, "lib","media","Logo.png")
jugar = os.path.join(absolute_path, "lib", "media", "Jugar.png")
salir = os.path.join(absolute_path, "lib", "media", "Salir.png")
# ----------------------------------------------------------------------
def limpiar_json():
    """
    Elimina los puntajes que son 0
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","saves","top_10.json"),"r")
        datos = json.load(arch)
        lista = datos["puntos"]
        lista_final = []
        for cadena in lista:
            aux = cadena.split(" - ")
            if aux[3] != "0":
                lista_final.append(cadena)
        arch.close()
        arch = open(os.path.join(absolute_path, "lib","info","saves","top_10.json"),"w")
        datos["puntos"] = lista_final
        json.dump(datos,arch,indent=4)
        arch.close()
    except (FileNotFoundError):
        pass
# ----------------------------------------------------------------------
def key_orden(cadena):
    """
    Key de orden para la lista del top 10
    """
    cadena = cadena.split(" - ")
    aux = int(cadena[3])
    return aux
# ----------------------------------------------------------------------
def cargar_top_10():
    """
    Cargamos los puntajes del top 10
    """
    # las sigs listas contienen listas que corresponderan
    # a las filas de la tabla del top 10
    list_facil = list()
    list_medio = list()
    list_dificil = list()
    try:
        arch = open(os.path.join(absolute_path, "lib","info","saves","top_10.json"),"r")
        top_10 = json.load(arch)
        list_aux = top_10["puntos"].copy()
        # ordenamos por puntos la lista
        list_aux = sorted(list_aux,key=key_orden,reverse=True)
        for punt in list_aux:
            dato = punt.split(" - ")
            if (dato[3] != "0"):
                # agregamos una fila con nombre del usuario,
                # de la fecha y el puntaje obtenido
                jugada = [dato[0], dato[1], dato[3]]
                if (dato[4] == "facil"):
                    list_facil.append(jugada)
                elif (dato[4] == "medio"):
                    list_medio.append(jugada)
                elif (dato[4] == "dificil"):
                    list_dificil.append(jugada)
        list_facil = list_facil[:10]
        list_medio = list_medio[:10]
        list_dificil = list_dificil[:10]
    except (FileNotFoundError):
        sg.popup("No se encontro el archivo de puntuaciones, se iniciara vacio",keep_on_top=True)
    finally:
        return list_facil,list_medio,list_dificil
# ----------------------------------------------------------------------
def crear_layout(config):
    """
    Crea el layout de la ventana menu
    """
    list_facil, list_medio, list_dificil = cargar_top_10()

    tab1_layout = [
        [sg.Button("", key="-jugar-", pad=(None,30),image_filename=jugar, border_width = 0,button_color=("#c5dbf1","#c5dbf1")) ],
        # [sg.Button("Continuar partida pospuesta",visible=False,key="-continuar-",size=(50,4), pad=(150,2))],
        [sg.Button("", key="-salir-", pad=(None,0), image_filename=salir, border_width = 0,button_color=("#c5dbf1","#c5dbf1"))]
    ]
    frame_0 = [
        [sg.Radio("Facil", "nivel", tooltip="Adjetivos, sustantivos y verbos", key="facil", default= True if config["dificultad"] == "facil" else False),
        sg.Radio("Medio", "nivel", tooltip="Sustantivos y verbos", key="medio", default= True if config["dificultad"] == "medio" else False ),
        sg.Radio("Dificil", "nivel", tooltip="Categoria al azar", key="dificil", default= True if config["dificultad"] == "dificil" else False)]
    ]
    colum = [
        [sg.Text("A, E, O, S, I, U, N, L, R, T"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_1_cant"],key="grupo_1_cant")],
        [sg.Text("C, D, G"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_2_cant"],key="grupo_2_cant")],
        [sg.Text("M, B, P"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_3_cant"],key="grupo_3_cant")],
        [sg.Text("F,H,V,Y"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_4_cant"],key="grupo_4_cant")],
        [sg.Text("J"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_5_cant"],key="grupo_5_cant")],
        [sg.Text("K, LL, Ñ, Q, RR, W, X"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_6_cant"],key="grupo_6_cant")],
        [sg.Text("Z"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_7_cant"],key="grupo_7_cant")]
    ]
    frame_col = [
        [sg.Frame("Cantidad de letras",layout=colum)]
    ]
    frame_1 = [
        [sg.Text("A, E, O, S, I, U, N, L, R, T"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_1"],key="grupo_1")],
        [sg.Text("C, D, G"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_2"],key="grupo_2")],
        [sg.Text("M, B, P"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_3"],key="grupo_3")],
        [sg.Text("F,H,V,Y"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_4"],key="grupo_4")],
        [sg.Text("J"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_5"],key="grupo_5")],
        [sg.Text("K, LL, Ñ, Q, RR, W, X"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_6"],key="grupo_6")],
        [sg.Text("Z"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=config["grupo_7"],key="grupo_7")]
    ]
    tiempo = config["tiempo"].split(":")
    frame_2 = [
        [sg.Frame("Tiempo (en minutos)",layout=[[sg.Slider((1,60),default_value=tiempo[0],orientation="horizontal",key="-tiempo-")]])]
    ]
    texto_ayuda_config = '• DIFICULTAD: según la dificultad que se elija, se podrán formar\n'+ \
                  'distintos tipos de palabras y se jugará con distintos tableros.\n'+ \
                  '    • FACIL: se permiten formar Sustantivos, adjetivos y verbos\n'+ \
                  '    • MEDIO: se permiten formar Adjetivos y verbos\n' + \
                  '    • DIFICIL: se permiten formar palabras de tipo aleatorio\n' + \
                  '\n• TIEMPO: Indica cuánto dura la partida de principio a fin, teniendo\n'+ \
                  'en cuenta que la máquina tarda un segundo en hacer su jugada.\n'+ \
                  '\n• PUNTOS POR LETRA: cuántos puntos vale cada letra, al colocar una\n'+\
                  'palabra válida los puntos de las letras utilizadas se sumaran al puntaje\n'+\
                  'del jugador.\n'+ \
                  '\n• CANTIDAD DE LETRAS: esta opción permite elegir con cuántas letras se\n'+\
                  'quiere jugar. Una partida con pocas letras será una partida mas corta y \n'+\
                  'mientras menos vocales haya será más difícil armar palabras.'


    ayuda_config= [[sg.Text(texto_ayuda_config, auto_size_text=True)]]
    tab2_layout0 = [
        [sg.Column(frame_2),sg.Frame("Dificultad",layout=frame_0)],
        [sg.Frame("Puntos por letra",layout=frame_1),sg.Column(frame_col)],
        [sg.Button("Guardar", key="-guardar-"),sg.Button("Config predeterminada",key="-pred-")]
                   ]
    tab2_layout = [[sg.Column(tab2_layout0),sg.Column(ayuda_config)]
    ]
    sin_datos = [['' for i in range(10)] for j in range(10)]

    headings = ['    USUARIO    ', '    FECHA    ', '    PUNTOS    ']

    frame_top_10 = [
         [sg.Radio("Facil",group_id="top",default=True,key="t_Facil"),sg.Radio("Medio",group_id="top",key="t_Medio"),sg.Radio("Dificil",group_id="top",key="t_Dificil"),
         sg.B("Actualizar",key="act")],
         [sg.Table(values= list_facil if len(list_facil) != 0 else sin_datos,
          headings=headings, max_col_width=400, auto_size_columns=True,
          text_color='black', justification='center',
          num_rows=10, font='Courier 12', pad=(12,2), background_color="#c5dbf1",
          alternating_row_color='#8fa8bf', key='top_10', def_col_width=30,
          header_text_color='white', header_background_color='#8fa8bf')]
    ]
    tab3_layout = [
        [sg.Frame("TOP 10 mejores jugadas",layout= frame_top_10)]
    ]
    texto_ayuda0 = ' ScrabbleAR es un juego de estrategia en el cual se juega Jugador vs Máquina por turnos,\n'+\
                  'con el objetivo de formar palabras colocando letras en los casilleros de un tablero\n'+\
                  'para sumar puntos. Si se consiguen más puntos que la máquina al final de la partida\n'+\
                  'se gana el juego, de lo contrario se pierde.'
    texto_ayuda1 = ' Antes de empezar a jugar desde ScrabbleAR recomendamos echar un vistazo,\n'+\
                   'a la pestaña "Configuración de nivel", en ella se tiene la opción de\n'+\
                   'modificar aspectos importantes del juegos, como por ej: la duración de\n'+\
                   'la partida, la dificultad, etc.\n '+\
                   ' En caso de que no se quiera modificar las configuraciones de partida se\n'+\
                   'pueden dejar como estan por defecto. Para empezar a jugar nada más basta\n' +\
                   'con clickear en el botón "JUGAR" que se encuentra en la pestaña "Juego" de\n'+\
                   'este menú y empezará la partida dandote la opcion de ingresar tu nombre de\n'+\
                   'usuario para guardar tu puntaje o jugar como jugador invitado.'

    frame_ayuda_0 = [
        [sg.T(texto_ayuda0)]]
    frame_ayuda_1 = [
        [sg.Text(texto_ayuda1)]]

    tab_lista = [[sg.Tab("Introduccion",layout=frame_ayuda_0)],
                 [sg.Tab("Como empezar a jugar",layout=frame_ayuda_1)],
                 [sg.Tab("Empezando la partida",layout= [[sg.Text(empezando_la_partida())]] )],
                 [sg.Tab("Botones especiales",layout= [[sg.Text(botones_especiales())]] )]]
    tab4_layout = [[sg.TabGroup(layout=tab_lista)]]
    tab_grupo = [
        [sg.Tab("Juego", tab1_layout, element_justification='c' , key="-tab1-", background_color="#c5dbf1", title_color="#2c2825", border_width=0),
         sg.Tab("Como jugar", tab4_layout, element_justification='c' , key="-tab4-", background_color="#c5dbf1", title_color="#c5dbf1", border_width = 0),
         sg.Tab("Config nivel", tab2_layout, element_justification='c' , key="-tab2-", background_color="#c5dbf1", title_color="#c5dbf1",
                border_width=0),
         sg.Tab("Top 10", tab3_layout, element_justification='c' , key="-tab3-", background_color="#c5dbf1", title_color="#c5dbf1", border_width=0)]]
    layout = [[sg.Image(logo, background_color=("#c5dbf1"))],
              [sg.TabGroup(tab_grupo, enable_events=True, key="-tabgrupo-")]]
    return layout , list_facil, list_medio, list_dificil
# ----------------------------------------------------------------------
def guardar_configuracion(config):
    """
    Guarda la configuracion que hizo el usuario en un .json
    """
    arch = open(os.path.join(absolute_path, "lib","info","config","configUsuario.json"), "w")
    json.dump(config,arch,indent=2)
    arch.close()
# ----------------------------------------------------------------------
def cargar_config_pred():
    """
    Carga la configuracion predeterminada del juego
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","config","configPred.json"), "r")
        config = dict()
        config = json.load(arch)
        arch.close()
    except (FileNotFoundError):
        sg.popup("Algo salio mal! no hay config predeterminada :(",keep_on_top=True)
        exit()
    return config
# ----------------------------------------------------------------------
def cargar_config_usr():
    """
    Carga el archivo json con las configuraciones que hizo el usuario
    en la pestaña de configuracion
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","config","configUsuario.json"), "r")
        config = dict()
        config = json.load(arch)
        arch.close()
    except (FileNotFoundError):
        sg.popup("No se encontro configuracion de usuario, se usara la predeterminada",keep_on_top=True)
        config = cargar_config_pred()
    finally:
        return config
# ----------------------------------------------------------------------
def main():
    """
    Visualización principal antes de iniciar el juego
    """
    #Si hay configuraciones de usuario las cargo para mostrarlas en
    #pestaña config
    if "configUsuario.json" in os.listdir(os.path.join(absolute_path, "lib","info","config")):
        config = cargar_config_usr()
    else:
        config = cargar_config_pred()
    # ----------------------------------------------------------------------
    sg.LOOK_AND_FEEL_TABLE['MyNewTheme'] = {'BACKGROUND': '#c5dbf1',
                                        'TEXT': '#000000',
                                        'INPUT': '#2a6daf',
                                        'TEXT_INPUT': '#000000',
                                        'SCROLL': '#2a6daf',
                                        'BUTTON': ('white', '#2a6daf'),
                                        'PROGRESS': ('#2a6daf', '#2a6daf'),
                                        'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,}
    sg.theme("MyNewTheme")
    sg.set_options(font=('verdana', 10))
    # sg.theme("lightblue")
    layout, list_facil, list_medio, list_dificil = crear_layout(config)
    window = sg.Window("ScrabbleAR", layout,element_justification='c', resizable=True,auto_size_buttons=True,auto_size_text=True,finalize=True,icon=icono_ventana)
    sin_datos = [['' for i in range(10)] for j in range(10)]

    while True:
        event, values = window.read()
        # print("Evento",event)
        if (event == None):
            limpiar_json()
            break
        elif (event == "-salir-"):
            salir = sg.popup("Salir del juego?", custom_text=("   SI   ","   NO   "),keep_on_top=True)
            if (salir == "   SI   "):
                limpiar_json()
                break
            else:
                pass
        elif (event == "-pred-"):
            try:
                os.remove(os.path.join(absolute_path, "lib","info","config","configUsuario.json"))
                window["-pred-"].update(disabled=True)
                config = cargar_config_pred()
                #---------------------------------------------------------------------------------
                #Actualizacion del menu
                #Con las configs predeterminadas
                #---------------------------------------------------------------------------------
                for i in range(7):
                    ind = i + 1 if i < 7 else 7
                    window["grupo_"+str(ind)].update(config["grupo_"+str(ind)])
                    window["grupo_"+str(ind)+"_cant"].update(config["grupo_"+str(ind)+"_cant"])
                window["-tiempo-"].update(value = int(config["tiempo"].split(":")[0]))
                if (config["dificultad"] == "facil"):
                    window["facil"].update(True)
                elif (config["dificultad" == "medio"]):
                    window["medio"].update(True)
                elif (config["dificultad"] == "dificil"):
                    window["dificil"].update(True)
                #-----------------------------------------------------------------------------------
            except (FileNotFoundError):
                window["-pred-"].update(disabled=True)
                config = cargar_config_pred()
            finally:
                sg.popup("Configuraciones reiniciadas",keep_on_top=True)
        elif (event == "-jugar-"):
            print("Estoy jugando")
            if ("guardado.json" in os.listdir(os.path.join(absolute_path, "lib","info","saves"))):
                print("Entre al if")
                popup = sg.popup("Hay una partida guardada desea continuarla?", custom_text=("   SI   ","   NO   "),keep_on_top=True)
                if (popup == "   NO   "):
                    window.close()
                    Juego.main(False)
                elif (popup == None):
                    pass
                else:
                    window.close()
                    Juego.main(True)
            else:
                window.close()
                Juego.main(False)
        elif (event == "act"):
            if (window["t_Facil"].get()):
                window["top_10"].update(list_facil if len(list_facil) != 0 else sin_datos)
            elif (window["t_Medio"].get()):
                window["top_10"].update(list_medio if len(list_medio) != 0 else sin_datos)
            elif (window["t_Dificil"]):
                window["top_10"].update(list_dificil if len(list_dificil) != 0 else sin_datos)
            window.refresh()
        elif (event == "-tabgrupo-")and(values["-tabgrupo-"] == "-tab3-"):
            window.refresh()
        elif (event == "-guardar-"):
            window["-pred-"].update(disabled=False)
            if "configUsuario.json" in os.listdir(os.path.join(absolute_path, "lib","info","config")):
                config = cargar_config_usr()
            else:
                config = cargar_config_pred()
            config["tiempo"] = str(int(values["-tiempo-"]))+":00"
            if (window["facil"].get()):
                config["dificultad"] = "facil"
            elif (window["medio"].get()):
                config["dificultad"] = "medio"
            elif (window["dificil"].get()):
                config["dificultad"] = "dificil"
            #-----------------------------------
            #Guardando las configs
            #-----------------------------------
            valido = True
            for i in range(7):
                ind = i+1
                try:
                    valor_punt = int(window["grupo_"+str(ind)].get())
                    valor_cant = int(window["grupo_"+str(ind)+"_cant"].get())
                    if valor_cant > 0 and valor_cant < 12 and valor_punt > 0 and valor_punt < 11:
                        config["grupo_"+str(ind)] = int(window.FindElement("grupo_"+str(ind)).get())
                        config["grupo_"+str(ind)+"_cant"] =  int(window.FindElement("grupo_"+str(ind)+"_cant").get())
                    else:
                        sg.Popup('Solo puede ingresar puntajes de 1 a 10',
                                 'y cantidades de 1 a 11',
                                 'por favor intente nuevamente', title="Error")
                        valido = False
                        break
                except ValueError:
                    print('haber')
                    sg.Popup('Solo puede ingresar puntajes de 1 al 10',
                             'y cantidades de 1 a 11',
                             'por favor intente nuevamente', title="Error")
                    valido = False
                    break
            if (valido):
                guardar_configuracion(config)
                sg.popup("Se han guardado las configuraciones",keep_on_top=True)
    window.close()
if __name__ == "__main__":
    main()
