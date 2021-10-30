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
    """ open the main window... """

    id =  cf.get_id()
    id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])
    config_data = cf.get_config()

    sg.theme('Reddit')
    layout = [
            [
            sg.Text("")],
            [
            sg.Text("Dossier des cartes agents : "),
            sg.InputText(key="-INPUT-"),sg.FolderBrowse(key="-FOLDER-"),
            sg.Button("Ajouter",key="-SUBMITCARD-")],
            [
            sg.Text("")],
            [
            sg.Text("Congés : "),
            sg.Listbox(["C","R","RR"],size=(4,4),key="-BREAKTYPE-"),
            sg.T("Date (JJ/MM/AAAA)"),
            sg.Listbox(date_number,size=(4,4),key="-BREAKDAY-"),
            sg.Listbox(date_number[:12],size=(4,4),key="-BREAKMONTH-"),
            sg.Listbox(year_number,size=(4,4),key="-BREAKYEAR-"),
            sg.Button("Ajouter",key="-SUBMITBREAK-")],
            [
            sg.Text("")],
            [
            sg.Text("Vacances : "),
            sg.T("Début (JJ/MM/AAAA)"),
            sg.Listbox(date_number,size=(4,4),key="-HOLIDAYDAY0-"),
            sg.Listbox(date_number[:12],size=(4,4),key="-HOLIDAYMONTH0-"),
            sg.Listbox(year_number,size=(4,4),key="-HOLIDAYYEAR0-"),
            sg.T("Fin (JJ/MM/AAAA)"),
            sg.Listbox(date_number,size=(4,4),key="-HOLIDAYDAY1-"),
            sg.Listbox(date_number[:12],size=(4,4),key="-HOLIDAYMONTH1-"),
            sg.Listbox(year_number,size=(4,4),key="-HOLIDAYYEAR1-"),
            sg.Button("Ajouter",key="-SUBMITHOLIDAY-")],
            [
            sg.Button("Simplenote",key = "-SIMPLENOTE-"),
            sg.Button("Fichier de configuration",key = "-CONFIG-")],
            [
            sg.T("")],
            [
            sg.T(" TL-Note a bien démarré", background_color='lightblue',key = "-OUTPUT-")],
            [
            sg.T("")]
            ]
    window = sg.Window('TL-Note', layout, size=(800,450),element_justification='l',auto_size_text=True,
                       auto_size_buttons=True,resizable=True,grab_anywhere=False,border_depth=5,finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "-SUBMITCARD-":
            folder = str(values["-FOLDER-"])
            msn.add_agentcard(folder,config_data,id_SN,DEBUG=db.debug)
            window['-OUTPUT-'].update(" Cartes agents ajoutées à partir du dossier : "+folder)
        elif event == "-SUBMITBREAK-":
            type_list = values["-BREAKTYPE-"]
            day_list = values["-BREAKDAY-"]
            month_list = values["-BREAKMONTH-"]
            year_list = values["-BREAKYEAR-"]
            if ([] not in [type_list,day_list,month_list,year_list]):
                type = str(type_list)[2:-2]
                day = str(day_list)[2:-2]
                month = str(month_list)[2:-2]
                year = str(year_list)[2:-2]
                print(type,day,month,year)
                msn.add_break(int(day),int(month),int(year),type,config_data,id_SN)
                window['-OUTPUT-'].update(" Congé " +type+" du "+day+"/"+month+"/"+year+" ajouté")
            else:
                window['-OUTPUT-'].update("Vérifiez que tout les données ont étées saisies (type, jour, mois, année)")
        elif event == "-SUBMITHOLIDAY-":
            day0 = values["-HOLIDAYDAY0-"]
            month0 = values["-HOLIDAYMONTH0-"]
            year0 = values["-HOLIDAYYEAR0-"]
            day1 = values["-HOLIDAYDAY1-"]
            month1 = values["-HOLIDAYMONTH1-"]
            year1 = values["-HOLIDAYYEAR1-"]
            if ([] not in [day0,day1,month0,month1,year0,year1] ):
                day0 = str(values["-HOLIDAYDAY0-"])[2:-2]
                month0 = str(values["-HOLIDAYMONTH0-"])[2:-2]
                year0 = str(values["-HOLIDAYYEAR0-"])[2:-2]
                day1 = str(values["-HOLIDAYDAY1-"])[2:-2]
                month1 = str(values["-HOLIDAYMONTH1-"])[2:-2]
                year1 = str(values["-HOLIDAYYEAR1-"])[2:-2]
                msn.add_holiday(int(day0),int(month0),int(year0),int(day1),int(month1),int(year1),config_data,id_SN)
                window['-OUTPUT-'].update(" Vacances du "+day0+"/"+month0+"/"+year0+" au "+day1+"/"+month1+"/"+year1+" ajoutées")
            else:
                window['-OUTPUT-'].update("Vérifiez que tout les données ont étées saisies ( jour, mois, année) pour le début et la fin des vacances")
        elif event == "-SIMPLENOTE-":
            webbrowser.open('https://app.simplenote.com/', new = 2)
        elif event == "-CONFIG-":
                window['-OUTPUT-'].update("Cette fonctionnalité n'est pas encore implémentée")
