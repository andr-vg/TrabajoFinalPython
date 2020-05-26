import PySimpleGUI as sg
import nivel_1 #commit
# import nivel_2
# import nivel_3
import os
import sys

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

    tab2_layout = [[sg.Text("Dificultad")],
                   [sg.Radio("Facil", "nivel", tooltip="Adjetivos, sustantivos y verbos", key="facil", default=True),
                    sg.Radio("Medio", "nivel", tooltip="Sustantivos y verbos", key="medio"),
                    sg.Radio("Dificil", "nivel", tooltip="Categoria al azar", key="dificil")],

                   [sg.Button("Confirmar", key="-confirmar-")]
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


def main():
    sg.theme("DarkAmber")
    layout = crear_layout()

    window = sg.Window("ScrabbleAR", layout)
    while True:
        event, values = window.read()
        print(event, values)
        if (event == None):
            break

        if (window["facil"].get()):
            print("Facil")
        elif (window["medio"].get()):
            print("Medio")
        elif (window["dificil"].get()):
            print("Dificil")

    window.close()


if __name__ == "__main__":
    main()
