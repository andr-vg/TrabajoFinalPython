import PySimpleGUI as sg 
# import nivel_1
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
    layout = [
        [sg.Image(logo,background_color=("#2c2825"))],
        [sg.Button("Jugar",border_width=1,pad=(80,10),size=(30,2))],
        [sg.Button("Configuraciones",border_width=1,pad=(80,10),size=(30,2))],
        [sg.Button("Top 10",border_width=1,pad=(80,10),size=(30,2))]

    ]
    return layout

def main():
    layout = crear_layout()
    sg.theme("DarkAmber")
    window = sg.Window("ScrabbleAR",layout)
    while True:
        event,values = window.read()
        if (event == None):
            break
    
    window.close()

if __name__ == "__main__":
    main()


