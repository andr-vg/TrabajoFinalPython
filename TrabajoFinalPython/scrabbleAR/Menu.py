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
        [sg.Image(logo)],
        [sg.Button("Jugar",border_width=1,pad=(80,10),size=(30,2))],
        [sg.Button("Configuraciones",border_width=1,pad=(80,10),size=(30,2))],
        [sg.Button("Top 10",border_width=1,pad=(80,10),size=(30,2))]

    ]
    sg.theme("DarkAmber")
    return layout

def main():
    layout = crear_layout()
    window = sg.Window("ScrabbleAR",layout)
    while True:
        event,values = window.read()
        if (event == None):
            break
    
    window.close()

if __name__ == "__main__":
    main()


