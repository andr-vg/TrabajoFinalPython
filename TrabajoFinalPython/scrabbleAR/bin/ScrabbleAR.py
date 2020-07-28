import PySimpleGUI as sg
import Juego #Programa Principal
import os
import sys
import json
import ScrabbleAR
import pathlib
from GameConfigManager import empezando_la_partida
from GameConfigManager import botones_especiales
# ----------------------------------------------------------------------
#Path making
absolute_path = os.path.join(os.path.dirname(__file__), '..')
icono_ventana = b"iVBORw0KGgoAAAANSUhEUgAAAEkAAABJCAYAAABxcwvcAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAS2SURBVHja7Jw/bBRHFIe/tXwKnIRQTIEgGwGRQL4IIgFCchpMQcGfigLSXJEWOY3BDhIFvVPQIFoarqOgIkoiClsIBVDcOCffwUlGkRwllSVksJAoTHGzsF5mZnd2Z/aOu3nSSqfZ29vd377vvZk3ewNq+xr4CXgErAObA7j9DzwQ9xliYHuBhwMqStr2UNy/1s4NqTjJ7VxWgZ4D3wPbGGzbJu7zeZpQYeILs0DAcFkAzCR02BKnnsV2XGO4bTamxV9R4/4EYsGQixQArZgmBwCuxhpO4g0RoyJNZgAexxq2e30+BPNIk8cAr2IN3j5apMl6kBAn8NpsEQmAEa9FunmRvEh2bNTS71Q1w5e3wIbD31fZOvDOdhQvkt3mUwaMRRPCXIHB6l2gbloKSepSVKRqhgut9VCk+DZvcC0fjrMRkyYzfOdMn4SXSWBZiB6Uidt8xqcY9IEnJTEMysCtqnBp28jNKW5yTLGFwIT4jk6os2WIdFZxYtnFTVsWaS7jsWMp3l5xLZLs5FXxFG0iV0SkaLilEmrCZeCuSoL2gugTLSqOGe/hOKyuKYs463FPKp44ohPX6LMstwq8lLQfc5ndVKhFZhO5orilZUknuIUa1CLrN+RU9tIVbqc0qNHHyMkmHu+5wm0lBTXbyNnArWLYVyqEW4iYQUi4rGykv9RHyJ1WtD91gZsMtRuK726IWNVr5GrAr5L2BrDmAjcZaqFhr9wUuby4BZrzq0LEJ7qMWkJtVXPMgga5VsEgPKbYd0h0Em9qjv/WpBho4kl1ydOo5+xTTRf0pLzbSsbBdu6xmylqtpCzJVJdM6C1IlKoeCpFqpe1EkRaEV2RiiHOuboAJlmtn7LcAeCCjRFymicFiqdkUlwvglyW7BaI66lrPKri0pPGFWOeVYOT/u24Y7kprqchMpfMo+7k+eGsIsmwuGWpVPGjA8RaCqHqmiJbIdwC7NWsVShULOBmEvArtnFT4bBMvhkKmR13FLRVQv5gG7cyMtCUo99dA36RtN817RLocAso793piqNSyZimY2kFtzJLGsf71ZtGc6C2kKUGk2IXJQPlKeCJw9j0syI2NYrgZjOrFc1yNiqTppkuE24q1NoWRJovGblCmU4nkqyTdwU7b+n+W3KWi2JTI29skuGmKppPWLzoaQP3tzXvVjPIdKm4qdx+0aJIv/UAuZaiGqH1phEDt29g8R1ETWxziRzA5TyxKYlbGaiZImcLt3jiSDuvFrcyUOslcsbe5P82oSfMqJ401OZF8iJ5kbxIXiQvkhfJi+RNbqPAf8CeQbqpw+MHa8BOMZTaTXf6+xXwD7BP7FsCvgNotjtPJCORyF6PsHX6eSDWBWi2Oy26M8Y7gCPAC+B6s93ZEPu+pPuK9SIwdXj8YHJA/UXs89II8Ees4cSAeFIAhM12Z43u2zBV4HexL6RbU9olBtK3JVWHo7HP9wO6a5VEc/RtunPom5+5SHPAfeFBh2K7VunO1PwpPh8BdjXbnUYCtWU+1vi/iXbEV72ZHfI4LV31Bvz6SZEHaddPAjiPX4krfv/nVQdcxK/ntglcSlP2K4Z7dUCj9QP2C0YfAW8GVJQ34v5mxP1K7f0A2wJqfDSaFUAAAAAASUVORK5CYII="
# print("ABSOLUTE PATH: ",absolute_path)
logo = os.path.join(absolute_path, "lib","media","Logo.png")
jugar = os.path.join(absolute_path, "lib", "media", "Jugar.png")
salir = os.path.join(absolute_path, "lib", "media", "Salir.png")
# ----------------------------------------------------------------------
def limpiar_json():
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
    cadena = cadena.split(" - ")
    aux = cadena[1]+" "+cadena[2]
    return aux
def cargar_top_10():    #esto podria ir en GameConfigManager?
    """
    Cargamos los puntajes del top 10
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","saves","top_10.json"),"r")
        list_aux = []
        list_final = []
        top_10 = json.load(arch)
        # list_aux = sorted(top_10["puntos"],reverse=True)
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(list_aux)
        list_aux = top_10["puntos"].copy()
        list_aux = list_aux[-10:]
        list_aux = sorted(list_aux,key=key_orden,reverse=True)
        # print("\n LISTA")
        # pp.pprint(list_aux)
        for punt in list_aux:
            dato = punt.split(" - ")
            # print("DATO",dato)
            if (dato[3] != "0"):
                cadena = "|Usuario: "+dato[0]+" |Fecha: "+dato[1]+" - "+dato[2]+" |Puntos: "+dato[3]+" |Nivel: "+dato[4]
                list_final.append(cadena)
    except (FileNotFoundError):
        sg.popup("No se encontro el archivo de puntuaciones, se iniciara vacio",keep_on_top=True)
        list_final = []
    return list_final
# ----------------------------------------------------------------------
def crear_layout(config):
    """
    Crea el layout de la ventana menu
    """
    top_10 = cargar_top_10()

    tab1_layout = [
        [sg.Button("", key="-jugar-", image_filename=jugar, border_width = 0,button_color=("#c5dbf1","#c5dbf1")) ],
        # [sg.Button("Continuar partida pospuesta",visible=False,key="-continuar-",size=(50,4), pad=(150,2))],
        [sg.Button("", key="-salir-", image_filename=salir, border_width = 0,button_color=("#c5dbf1","#c5dbf1"))]
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
    frame_2 = [
        [sg.Frame("Tiempo (en minutos)",layout=[[sg.Slider((1,60),default_value=round(config["tiempo"] / 60),orientation="horizontal",key="-tiempo-")]])]
    ]

    ayuda_config= [
[sg.Text("""•Dificultad: segun la dificultad que se elija, se podran formar
distintos tipos de palabras y se jugara con distintos tableros.
	• Facil: se permiten formar Sustantivos, adjetivos y verbos
	• Medio: se permiten formar Adjetivos y verbos
	• Dificil: se permiten formar palabras de tipo aleatorio

•Tiempo: Indica cuanto dura la partida de principio a fin, teniendo en cuenta
que la maquina tarda un segundo en hacer su jugada.

•Puntos por letra: cuantos puntos vale cada letra, al colocar una palabra valida
 los puntos de las letras utilizadas se sumaran al puntaje del jugador.

•Cantidad de letras: esta opcion permite elegir con cuantas letras se quiere jugar.
una partida con pocas letras sera una partida mas corta y mientras menos
vocales haya sera mas dificil armar palabras.""")]
    ]
    tab2_layout0 = [
        [sg.Column(frame_2),sg.Frame("Dificultad",layout=frame_0)],
        [sg.Frame("Puntos por letra",layout=frame_1),sg.Column(frame_col)],
        [sg.Button("Guardar", key="-guardar-"),sg.Button("Config predeterminada",key="-pred-")]
                   ]
    tab2_layout = [[sg.Column(tab2_layout0),sg.Column(ayuda_config)]

    ]
    frame_top_10 = [
         [sg.Listbox(["Aun no se ha jugado"] if len(top_10) == 0 else top_10, size=(100, 10), background_color="#c5dbf1")]
    ]
    tab3_layout = [
        [sg.Frame("Puntuaciones de los ultimos 10 juegos",layout= frame_top_10)]
    ]
    frame_ayuda_0 = [
        [sg.T("""ScrabbleAR es un juego de estrategia en el cual se juega Jugador vs Maquina por turnos,
con el objetivo de formar palabras colocando letras en los casilleros de un tablero
para sumar puntos.
Si se consiguen mas puntos que la maquina al final de la partida se gana el juego, de
lo contrario se pierde.""")]
    ]

    frame_ayuda_1 = [
        [sg.Text("""Antes de empezar a jugar desde ScrabbleAR recomendamos hechar un vistazo
a la pestaña "Configuracion de nivel", en ella se tiene la opcion de modificar aspectos
importantes del juegos como por ej: la duracion de la partida, la dificultad, etc.
En caso de que no se quiera modificar las configuraciones de partida se pueden dejar
con estan por defecto.
Para empezar a jugar nada mas basta con clickear en el boton "JUGAR" que se encuentra en
la pestaña "Juego" de este menu y empezara la partida dandote la opcion de ingresar tu nombre
de usuario para guardar tu puntaje o jugar como jugador invitado.""")]]

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
    return layout
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
    # sg.theme("lightblue")
    layout = crear_layout(config)
    window = sg.Window("ScrabbleAR", layout,element_justification='c', resizable=True,auto_size_buttons=True,auto_size_text=True,finalize=True,icon=icono_ventana)

    while True:
        event, values = window.read()
        print("Evento",event)
        if (event == None):
            limpiar_json()
            break
        if (event == "-salir-"):
            salir = sg.popup("Salir del juego?", custom_text=("   SI   ","   NO   "),keep_on_top=True)
            if (salir == "   SI   "):
                limpiar_json()
                break
            else:
                pass
        if (event == "-pred-"):
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
                window["-tiempo-"].update(value = round(config["tiempo"] / 60))
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

        if (event == "-jugar-"):
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

        if (event == "-tab3-" ):
            window.refresh()
        if (event == "-guardar-"):
            window["-pred-"].update(disabled=False)
            if "configUsuario.json" in os.listdir(os.path.join(absolute_path, "lib","info","config")):
                config = cargar_config_usr()
            else:
                config = cargar_config_pred()
            config["tiempo"] = values["-tiempo-"]*60
            if (window["facil"].get()):
                config["dificultad"] = "facil"
            elif (window["medio"].get()):
                config["dificultad"] = "medio"
            elif (window["dificil"].get()):
                config["dificultad"] = "dificil"
            #-----------------------------------
            #Guardando las configs
            #-----------------------------------
            for i in range(7):
                ind = i+1
                config["grupo_"+str(ind)] = int(window.FindElement("grupo_"+str(ind)).get()) if int(window.FindElement("grupo_"+str(ind)).get()) > 0 else 1
                config["grupo_"+str(ind)+"_cant"] =  int(window.FindElement("grupo_"+str(ind)+"_cant").get()) if int(window.FindElement("grupo_"+str(ind)+"_cant").get()) > 0 else 1
            guardar_configuracion(config)
            sg.popup("Se han guardado las configuraciones",keep_on_top=True)
    window.close()
if __name__ == "__main__":
    main()
