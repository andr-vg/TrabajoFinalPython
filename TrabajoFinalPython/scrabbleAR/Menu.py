import PySimpleGUI as sg
import nivel_1 #commit
# import nivel_2
# import nivel_3
import os
import sys
import json

absolute_path = os.path.dirname(os.path.abspath(__file__))

if ("win" in sys.platform):
    logo = absolute_path + "\\Datos\\media\\Logo.png"
else:
    logo = absolute_path + "/Datos/media/Logo.png"


def crear_layout():
    top_10 = []

    tab1_layout = [
        [sg.Text("")],
        [sg.Button("Iniciar Juego", key="-1-")],
        [sg.Button("Salir", key="-5-")]
    ]
    frame_0 = [
        [sg.Radio("Facil", "nivel", tooltip="Adjetivos, sustantivos y verbos", key="facil", default=True),
        sg.Radio("Medio", "nivel", tooltip="Sustantivos y verbos", key="medio"),
        sg.Radio("Dificil", "nivel", tooltip="Categoria al azar", key="dificil")]
    ]

    colum = [
        [sg.Text("A, E, O, S, I, U, N, L, R, T"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=1,key="grupo_1_cant")],
        [sg.Text("C, D, G"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=2,key="grupo_2_cant")],
        [sg.Text("M, B, P"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=3,key="grupo_3_cant")],
        [sg.Text("F,H,V,Y"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=4,key="grupo_4_cant")],
        [sg.Text("J"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=6,key="grupo_5_cant")],
        [sg.Text("K, LL, Ñ, Q, RR, W, X"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=8,key="grupo_6_cant")],
        [sg.Text("Z"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=10,key="grupo_7_cant")]
    ]
    frame_col = [
        [sg.Frame("Cantidad de letras",layout=colum)]
    ]
    
    frame_1 = [
        [sg.Text("A, E, O, S, I, U, N, L, R, T"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=1,key="grupo_1")],
        [sg.Text("C, D, G"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=2,key="grupo_2")],
        [sg.Text("M, B, P"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=3,key="grupo_3")],
        [sg.Text("F,H,V,Y"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=4,key="grupo_4")],
        [sg.Text("J"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=6,key="grupo_5")],
        [sg.Text("K, LL, Ñ, Q, RR, W, X"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=8,key="grupo_6")],
        [sg.Text("Z"),sg.Spin(values=[1,2,3,4,5,6,7,8,9,10],initial_value=10,key="grupo_7")]
    ]

    frame_2 = [
        [sg.Frame("Tiempo (en minutos)",layout=[[sg.Slider((1,60),default_value=10,orientation="horizontal",key="-tiempo-")]])]
    ]


    tab2_layout = [
        [sg.Frame("Dificultad",layout=frame_0),sg.Column(frame_2)],
        [sg.Frame("Puntos por letra",layout=frame_1),sg.Column(frame_col)],                  
        [sg.Button("Guardar", key="-guardar-")]
                   ]

    tab3_layout = [
        [sg.Text("Top 10")],
        [sg.Listbox(top_10, default_values="Aun no hay partidas registradas", size=(55, 10))]
    ]

    tab_grupo = [
        [sg.Tab("Juego", tab1_layout, key="-tab1-", background_color="#2c2825", title_color="#2c2825", border_width=0),
         sg.Tab("Config nivel", tab2_layout, key="-tab2-", background_color="#2c2825", title_color="#2c2825",
                border_width=0),
         sg.Tab("Top 10", tab3_layout, key="-tab3-", background_color="#2c2825", title_color="#2c2825", border_width=0)]
    ]

    layout = [[sg.Image(logo, background_color=("#2c2825"))],
              [sg.TabGroup(tab_grupo, enable_events=True, key="-tabgrupo-")]]
    return layout

# def crear_predeterminado(config):
#     arch = open(absolute_path + "\\Datos\\info\\configPred.json","w")
#     json.dump(config,arch,indent=2)
#     arch.close()

def guardar_configuracion(config):
    arch = open(absolute_path + "\\Datos\\info\\configUsuario.json","w")
    json.dump(config,arch,indent=2)
    arch.close()

def cagar_config():
    arch = open(absolute_path + "\\Datos\\info\\configPred.json","r")
    config = dict()
    config = json.load(arch)
    arch.close()
    return config

def main():
    sg.theme("DarkAmber")
    layout = crear_layout()
    config = cagar_config()
    window = sg.Window("ScrabbleAR", layout)
    while True:
        event, values = window.read()
        print(event, values)
        if (event == None):
            break
        if (event == "-guardar-"):
            config["tiempo"] = values["-tiempo-"]*60
            if (window["facil"].get()):
                config["dificultad"] = "facil"
            elif (window["medio"].get()):
                config["dificultad"] = "medio"            
            elif (window["dificil"].get()):
                config["dificultad"] = "dificil"
            config["grupo_1"] = int(window.FindElement("grupo_1").get())
            config["grupo_2"] = int(window.FindElement("grupo_2").get())
            config["grupo_3"] = int(window.FindElement("grupo_3").get())
            config["grupo_4"] = int(window.FindElement("grupo_4").get())
            config["grupo_5"] = int(window.FindElement("grupo_5").get())
            config["grupo_6"] = int(window.FindElement("grupo_6").get())
            config["grupo_7"] = int(window.FindElement("grupo_7").get())
            config["grupo_1_cant"] = int(window.FindElement("grupo_1_cant").get())
            config["grupo_2_cant"] = int(window.FindElement("grupo_2_cant").get())
            config["grupo_3_cant"] = int(window.FindElement("grupo_3_cant").get())
            config["grupo_4_cant"] = int(window.FindElement("grupo_4_cant").get())
            config["grupo_5_cant"] = int(window.FindElement("grupo_5_cant").get())
            config["grupo_6_cant"] = int(window.FindElement("grupo_6_cant").get())
            config["grupo_7_cant"] = int(window.FindElement("grupo_7_cant").get())

            guardar_configuracion(config)
            


    window.close()


if __name__ == "__main__":
    main()
