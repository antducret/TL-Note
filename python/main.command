#!/usr/bin/env python3

# IMPORT
import config as cf
import interface as int
import moresimplenote as msn
import PySimpleGUI as sg
import simplenote as sn
import webbrowser as web


# MAIN

#   Initialize config and tags
config = cf.get_config()
tags = ["TEST"]#cf.get_tags()

#   Simplenote id
id = cf.get_id()
id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])

#   Delete old notes
msn.outdate(id_SN)

#   Interface
sg.theme('Reddit')
window = int.get_window()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "-SUBMITCARD-":
        folder = int.get_folder(values)
        msn.add_agentcard(folder,config,tags,id_SN)
        window['-OUTPUT-'].update(" Cartes agents ajoutées à partir du dossier : "+folder)
    elif event == "-SUBMITBREAK-":
        if int.get_break_validity(values) == "VOID":
            window['-OUTPUT-'].update("Vérifiez que tout les données ont étées saisies (type, jour, mois, année)")
        elif int.get_break_validity(values) == "PAST":
            window['-OUTPUT-'].update("Veuillez entrer une date future")
        else :
            type,day,month,year = int.get_break_string(values)
            date = int.get_break_date(values)
            msn.add_break(date,type,config,tags,id_SN)
            window['-OUTPUT-'].update(" Congé " +type+" du "+day+"/"+month+"/"+year+" ajouté")
    elif event == "-SUBMITHOLIDAY-":
        if int.get_holiday_validity(values) == "VOID":
            window['-OUTPUT-'].update("Vérifiez que tout les données ont étées saisies ( jour, mois, année) pour le début et la fin des vacances")
        elif int.get_holiday_validity(values) == "PAST":
            window['-OUTPUT-'].update(" Veuillez inscire des dates qui ne sont pas encore passées")
        elif int.get_holiday_validity(values) == "REVERSE":
            window['-OUTPUT-'].update(" Veuillez inscire les dates dans l'ordres chronologiques")
        else:
            date0,date1 = int.get_holiday_dates(values)
            msn.add_holiday(date0,date1,config,tags,id_SN)
            d0,m0,y0,d1,m1,y1 = int.get_holiday_string(values)
            window['-OUTPUT-'].update(" Vacances du "+d0+"/"+m0+"/"+y0+" au "+d1+"/"+m1+"/"+y1+" ajoutées")
    elif event == "-SIMPLENOTE-":
        web.open('https://app.simplenote.com/', new = 2)
    elif event == "-CONFIG-":
        window['-OUTPUT-'].update("Cette fonctionnalité n'est pas encore implémentée")
