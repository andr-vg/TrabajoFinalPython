import PySimpleGUI as sg
import Juego #Programa Principal
import os
import sys
import json
import ScrabbleAR
from pathlib import Path
# ----------------------------------------------------------------------
#Path making
absolute_path = Path(os.path.join("TrabajoFinalPython","ScrabbleAR"))
# print("ABSOLUTE PATH: ",absolute_path)
logo = os.path.join(absolute_path, "lib","media","Logo.png")
jugar = os.path.join(absolute_path, "lib", "media", "Jugar.png")
salir = os.path.join(absolute_path, "lib", "media", "Salir.png")

# ----------------------------------------------------------------------
def cargar_top_10():
    """
    Cargamos los puntajes del top 10
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","top_10.json"),"r")
        list_aux = []
        top_10 = json.load(arch)
        top_10 = {k: v for k, v in sorted(top_10.items())}
        for key in top_10.keys():
            key_aux = key.split("-")
            str_aux = "Fecha: " + key_aux[0] +" Puntos: "+ str(top_10[key])
            list_aux.append(str_aux)
        list_aux = list_aux[:10] #-----> Organizo por dia y muestro solamente 10 
        #---------------------------------------------------
        #Saco los datos sobrantes
        #---------------------------------------------------
        lista_keys_borrar = list(top_10.keys())
        lista_keys_borrar = lista_keys_borrar[10:len(top_10.keys())]
        for key in lista_keys_borrar:
            top_10.pop(key)

    except (FileNotFoundError):
        sg.popup("No se encontro el archivo de puntuaciones, se iniciara vacio")
        list_aux = []
    return list_aux
# ----------------------------------------------------------------------
def crear_layout(config):
    """
    Crea el layout de la ventana menu
    """
    top_10 = cargar_top_10()

    tab1_layout = [
        [sg.Button("", key="-jugar-", size=(50,4), pad=(150,2), image_filename=jugar, button_color=("#E3F2FD","#E3F2FD")) ],
        # [sg.Button("Continuar partida pospuesta",visible=False,key="-continuar-",size=(50,4), pad=(150,2))],
        [sg.Button("", key="-salir-",size=(50,4), pad= (150,3), image_filename=salir, button_color=("#E3F2FD","#E3F2FD"))]
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


    tab2_layout = [
        [sg.Frame("Dificultad",layout=frame_0),sg.Column(frame_2)],
        [sg.Frame("Puntos por letra",layout=frame_1),sg.Column(frame_col)],
        [sg.Button("Guardar", key="-guardar-"),sg.Button("Config predeterminada",key="-pred-")]
                   ]
    frame_top_10 = [
         [sg.Listbox(["Aun no se ha jugado"] if len(top_10) == 0 else top_10, pad=(140,None),size=(30, 10), background_color="#E3F2FD")]
    ]
    tab3_layout = [
        [sg.Frame("Puntuaciones de los ultimos 10 juegos",layout= frame_top_10)]
    ]
    frame_ayuda_0 = [
        [sg.T("""En la pestaña de configuraciones encontrara las siguientes opciones 
        • Dificultad 
        • Cantidad de letras 
        • Puntos por letra
        • Tiempo
        """)]
    ]
    frame_ayuda_1 = [
        [sg.Text("""• Facil: se permiten 'Sustantivos, adjetivos y verbos'
• Medio: 'Adjetivos y verbos'
• Dificil: Un tipo aleatorio
        """)]
    ]

    frame_ayuda_2 = [
        [sg.Text(
            """En el juego hay distintos tipos de casilleros: 
            • Casilleros de premio: que duplican o triplican el puntaje de la palabra
            • Casilleros de descuento: Que quitan 1, 2 o 3 puntos dependiendo

Cada uno de estos casilleros esta indicado con un color en cada nivel de dificultad 
            """
        )]
    ]
    frame_ayuda_3 = [
        [sg.Text("""Si no podes formar ninguna palabra en tu turno
podes darle al boton "Cambiar Fichas"
para seleccionar las fichas que quieres cambiar y dandole de nuevo al boton
se cambian
• Solo hay 3 cambios de fichas por juego y cuando cambias perdes el turno
"""
        )]]



    tab_lista = [
                [sg.Tab("Info",layout=frame_ayuda_0)],
                 [sg.Tab("Dificultad",layout=frame_ayuda_1)],
                 [sg.Tab("Casilleros especiales",layout=frame_ayuda_2)],
                 [sg.Tab("Cambio de fichas",layout=frame_ayuda_3)]]
    tab4_layout = [[sg.TabGroup(layout=tab_lista)]]
    tab_grupo = [
        [sg.Tab("Juego", tab1_layout, key="-tab1-", background_color="#E3F2FD", title_color="#2c2825", border_width=0),
         sg.Tab("Como jugar", tab4_layout, key="-tab4-", background_color="#E3F2FD", title_color="#E3F2FD", border_width = 0),
         sg.Tab("Config nivel", tab2_layout, key="-tab2-", background_color="#E3F2FD", title_color="#E3F2FD",
                border_width=0),
         sg.Tab("Top 10", tab3_layout, key="-tab3-", background_color="#E3F2FD", title_color="#E3F2FD", border_width=0)]
    ]

    layout = [[sg.Image(logo, background_color=("#E3F2FD"),pad=(100,None))],
              [sg.TabGroup(tab_grupo, enable_events=True, key="-tabgrupo-")]]
    return layout
# ----------------------------------------------------------------------
def guardar_configuracion(config):
    """
    Guarda la configuracion que hizo el usuario en un .json
    """
    arch = open(os.path.join(absolute_path, "lib","info","configUsuario.json"), "w")
    json.dump(config,arch,indent=2)
    arch.close()
# ----------------------------------------------------------------------
def cargar_config_pred():
    """
    Carga la configuracion predeterminada del juego
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","configPred.json"), "r")
        config = dict()
        config = json.load(arch)
        arch.close()
    except (ZeroDivisionError):
        sg.popup("Algo salio mal! no hay config predeterminada :(")
        exit()
    return config
# ----------------------------------------------------------------------
def cargar_config_usr():
    """
    Carga el archivo json con las configuraciones que hizo el usuario
    en la pestaña de configuracion
    """
    try:
        arch = open(os.path.join(absolute_path, "lib","info","configUsuario.json"), "r")
        config = dict()
        config = json.load(arch)
        arch.close()
    except (FileNotFoundError):
        sg.popup("No se encontro configuracion de usuario, se usara la predeterminada")
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
    if "configUsuario.json" in os.listdir(os.path.join(absolute_path, "lib","info")):
        config = cargar_config_usr()
    else:
        config = cargar_config_pred()
    # ----------------------------------------------------------------------
    sg.theme("lightblue")
    layout = crear_layout(config)
    window = sg.Window("ScrabbleAR", layout,resizable=True,auto_size_buttons=True,auto_size_text=True,finalize=True)

    while True:
        event, values = window.read()
        # print("Evento",event,"valor",values)
        if (event == None or event == "-salir-"):
            break
        if (event == "-pred-"):
            try: 
                os.remove(os.path.join(absolute_path, "lib","info","configUsuario.json"))
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
                sg.popup("Configuraciones reiniciadas")

        if (event == "-jugar-"):
            if ("guardado.csv" in os.listdir(os.path.join(absolute_path, "lib","info"))):
                popup = sg.popup("Hay una partida guardada desea continuarla?", custom_text=("   SI   ","   NO   "))            
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

        if (event == "-guardar-"):
            window["-pred-"].update(disabled=False)
            if "configUsuario.json" in os.listdir(os.path.join(absolute_path, "lib","info")):
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
            sg.popup("Se han guardado las configuraciones")

    window.close()
    
if __name__ == "__main__":
    main()
