import config as cf
import datetime as dt
import moresimplenote as msn
import PySimpleGUI as sg
import simplenote as sn
import subprocess



date_number = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
year_number = ["2021","2022","2023"]

def get_layout():
    """ layout of the main window """
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
    return layout
def get_window():
    window = sg.Window('TL-Note', get_layout(), size=(800,450),element_justification='l',auto_size_text=True,
    auto_size_buttons=True,resizable=True,grab_anywhere=False,border_depth=5,finalize=True)
    return window
def get_folder(values):
    return str(values["-FOLDER-"])
def get_break_string(values):
    type = str(values["-BREAKTYPE-"])[2:-2]
    day = str(values["-BREAKDAY-"])[2:-2]
    month = str(values["-BREAKMONTH-"])[2:-2]
    year = str(values["-BREAKYEAR-"])[2:-2]
    return type,day,month,year
def get_break_date(values):
    t,d,m,y = get_break_string(values)
    date = dt.datetime(int(y),int(m),int(d))
    return date
def get_break_validity(values):
    type_list = values["-BREAKTYPE-"]
    day_list = values["-BREAKDAY-"]
    month_list = values["-BREAKMONTH-"]
    year_list = values["-BREAKYEAR-"]
    if ([] in [type_list,day_list,month_list,year_list]):
        return "VOID"
    if get_break_date(values) <dt.datetime.today()-dt.timedelta(days=1):
        return "PAST"
    else: return 1
def get_holiday_string(values):
    d0 = str(values["-HOLIDAYDAY0-"])[2:-2]
    m0 = str(values["-HOLIDAYMONTH0-"])[2:-2]
    y0 = str(values["-HOLIDAYYEAR0-"])[2:-2]
    d1 = str(values["-HOLIDAYDAY1-"])[2:-2]
    m1 = str(values["-HOLIDAYMONTH1-"])[2:-2]
    y1 = str(values["-HOLIDAYYEAR1-"])[2:-2]
    return d0,m0,y0,d1,m1,y1
def get_holiday_dates(values):
    d0,m0,y0,d1,m1,y1 = get_holiday_string(values)
    date0 = dt.datetime(int(y0),int(m0),int(d0))
    date1 = dt.datetime(int(y1),int(m1),int(d1))
    return date0,date1
def get_holiday_validity(values):
    d0 = values["-HOLIDAYDAY0-"]
    m0 = values["-HOLIDAYMONTH0-"]
    y0 = values["-HOLIDAYYEAR0-"]
    d1 = values["-HOLIDAYDAY1-"]
    m1 = values["-HOLIDAYMONTH1-"]
    y1 = values["-HOLIDAYYEAR1-"]
    if ([] in [d0,m0,y0,d1,m1,y1]): return "VOID"
    date0,date1 = get_holiday_dates(values)
    today_date = dt.datetime.today()-dt.timedelta(days=1)
    if date0<today_date or date1<today_date: return "PAST"
    if date0>date1: return "REVERSE"
    else: return 1
