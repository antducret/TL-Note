import PySimpleGUI as sg
import moresimplenote as msn
import simplenote as sn
import config as cf
import subprocess
import webbrowser
import debug as db

date_number = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
year_number = ["2021","2022","2023"]

def open_main_window():
    id =  cf.get_id()
    id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])
    sg.theme('Reddit')
    layout = [
            [sg.Text("")],
            [sg.Text("Dossier des cartes agents : "),
            sg.InputText(key="-INPUT-"),sg.FolderBrowse(key="-FOLDER-"),
            sg.Button("Ajouter",key="-SUBMITCARD-")],
            [sg.Text("")],
            [sg.Text("Congés : "),sg.Listbox(["C","R","RR"],size=(4,4),key="-BREAKTYPE-"),sg.T("Date (JJ/MM/AAAA)"),sg.Listbox(date_number,size=(4,4),key="-BREAKDAY-"),sg.Listbox(date_number[:12],size=(4,4),key="-BREAKMONTH-"),sg.Listbox(year_number,size=(4,4),key="-BREAKYEAR-"),sg.Button("Ajouter",key="-SUBMITBREAK-")],
            [sg.Text("")],
            [sg.Text("Vacances : "),sg.T("Début (JJ/MM/AAAA)"),sg.Listbox(date_number,size=(4,4),key="-HOLIDAYDAY0-"),sg.Listbox(date_number[:12],size=(4,4),key="-HOLIDAYMONTH0-"),sg.Listbox(year_number,size=(4,4),key="-HOLIDAYYEAR0-"),sg.T("Fin (JJ/MM/AAAA)"),sg.Listbox(date_number,size=(4,4),key="-HOLIDAYDAY1-"),sg.Listbox(date_number[:12],size=(4,4),key="-HOLIDAYMONTH1-"),sg.Listbox(year_number,size=(4,4),key="-HOLIDAYYEAR1-"),sg.Button("Ajouter",key="-SUBMITHOLIDAY-")],
            [sg.Button("Simplenote",key = "-SIMPLENOTE-"),sg.Button("Fichier de configuration",key = "-CONFIG-")],
            [sg.T("")],
            [sg.T(" TL-Note a bien démarré", background_color='lightblue',key = "-OUTPUT-")],
            [sg.T("")]
            ]

    window = sg.Window('TL-Note', layout, size=(800,450),element_justification='l',auto_size_text=True,
                       auto_size_buttons=True,resizable=True,grab_anywhere=False,border_depth=5,finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "-SUBMITCARD-":
            msn.add_agentcard(id_SN,str(values["-FOLDER-"]))
            window['-OUTPUT-'].update(" Cartes agents ajoutées à partir du dossier : "+str(values["-FOLDER-"]))
        elif event == "-SUBMITBREAK-":
            if ([] not in [values["-BREAKTYPE-"],values["-BREAKDAY-"],values["-BREAKMONTH-"],values["-BREAKYEAR-"]] ):
                msn.add_break(id_SN,values["-BREAKDAY-"],values["-BREAKMONTH-"],values["-BREAKYEAR-"],values["-BREAKTYPE-"])
                window['-OUTPUT-'].update(" Congé " +str(values["-BREAKTYPE-"])+" du "+str(values["-BREAKDAY-"])[2:-2]+"/"+str(values["-BREAKMONTH-"])[2:-2]+"/"+str(values["-BREAKYEAR-"])[2:-2]+" ajouté")
            else:
                window['-OUTPUT-'].update("Vérifiez que tout les données ont étées saisies (type, jour, mois, année)")
        elif event == "-SUBMITHOLIDAY-":
            if ([] not in [values["-HOLIDAYDAY0-"],values["-HOLIDAYDAY1-"],values["-HOLIDAYMONTH0-"],values["-HOLIDAYMONTH1-"],values["-HOLIDAYYEAR0-"],values["-HOLIDAYYEAR1-"]] ):
                msn.add_holiday(id_SN,values["-HOLIDAYDAY0-"],values["-HOLIDAYMONTH0-"],values["-HOLIDAYYEAR0-"],values["-HOLIDAYDAY1-"],values["-HOLIDAYMONTH1-"],values["-HOLIDAYYEAR1-"])
                window['-OUTPUT-'].update(" Vacances du "+str(values["-HOLIDAYDAY0-"])[2:-2]+"/"+str(values["-HOLIDAYMONTH0-"])[2:-2]+"/"+str(values["-HOLIDAYYEAR0-"])[2:-2]+" au "+str(values["-HOLIDAYDAY1-"])[2:-2]+"/"+str(values["-HOLIDAYMONTH1-"])[2:-2]+"/"+str(values["-HOLIDAYYEAR1-"])[2:-2]+" ajoutées")
            else:
                window['-OUTPUT-'].update("Vérifiez que tout les données ont étées saisies ( jour, mois, année) pour le début et la fin des vacances")
        elif event == "-SIMPLENOTE-":
            webbrowser.open('https://app.simplenote.com/', new = 2)
        elif event == "-CONFIG-":
                window['-OUTPUT-'].update("Cette fonctionnalité n'est pas encore implémentée")

id =  cf.get_id()
id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])
msn.add_agentcard(id_SN,"./tmp/1.INPUT/",DEBUG = db.debug)
