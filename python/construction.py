import extraction as ext
import config as cf
import debug as db
import datetime as dt

def construct_break(d,m,y,t,config_data):
    """ return a string named note formated for break day"""
    d = str(d)[2:-2]
    m = str(m)[2:-2]
    y = str(y)[2:-2]
    t = str(t)[2:-2]
    l = ext.weekday(d,m,y)
    logo = cf.get_logo("CONGE",config_data)
    return "{}-{} {} {} \n\n {}".format(d,m,l,logo,t)

def construct_holiday(date,config_data):
    """ return a string named note formated for holiday day"""
    d = date.day
    m = date.month
    y = date.year
    d_s = cf.int2digit(d)
    m_s = cf.int2digit(m)
    l = ext.weekday(d,m,y)
    logo = cf.get_logo("VACANCE",config_data)
    return "{}-{} {} {}️".format(d_s,m_s,l,logo)

def construct_holidays(d0,m0,y0,d1,m1,y1,config_data):
    """ return a list of notes formated for holiday days"""
    d0 = int(str(d0)[2:-2])
    m0 = int(str(m0)[2:-2])
    y0 = int(str(y0)[2:-2])
    d1 = int(str(d1)[2:-2])
    m1 = int(str(m1)[2:-2])
    y1 = int(str(y1)[2:-2])
    notes = []
    date0 = dt.datetime(y0,m0,d0)
    date1 = dt.datetime(y1,m1,d1)
    date = date0

    while (date != (date1 + dt.timedelta(days=1))):
        notes.append(construct_holiday(date),config_data)
        date += dt.timedelta(days=1)
    return notes

def isLogo(key,data,config_data):
    """ return a boolean to know if a specific logo must be added based on data of a day"""
    h_i = int(data["H_I"][0][:2])
    h_f = int(data["H_F"][-1][:2])
    v_list = [key[:2] for key in data["CAR"] if key[:2].isdigit()]
    return {
        "MOTO": (data["L_I"][0] == data["L_F"][-1] and data["L_I"][0] not in config_data["DEPOTS"]),
        "BOR" : (data["L_F"][-1] in config_data["DEPOTS_BOR"]),
        "PER" : (data["L_F"][-1] in config_data["DEPOTS_PER"]),
        "MATIN" :(h_i>= int(config_data["H_MATIN"][0]) and h_i< int(config_data["H_MIDI"][0])),
        "MIDI" :(h_i>= int(config_data["H_MIDI"][0]) and h_i< int(config_data["H_APREM"][0])),
        "APREM" :(h_i>= int(config_data["H_APREM"][0]) and h_i< int(config_data["H_NUIT"][0]) and h_f < 24),
        "NUIT" : (h_i>= int(config_data["H_NUIT"][0]) or h_f>=24),
        "1":any(key in v_list for key in config_data["L1"]),
        "9":any(key in v_list for key in config_data["9"]),
        "12":any(key in v_list for key in config_data["12"]),
        "17":any(key in v_list for key in config_data["17"]),
        "42":any(key in v_list for key in config_data["42"]),
        "54":any(key in v_list for key in config_data["54"]),
        "58":any(key in v_list for key in config_data["58"]),
        "60":any(key in v_list for key in config_data["60"]),
    }.get(key, False)

def update_logo(logo,key,data,config_data):
    """ return a total logo with addition of specific logo if specific condition is ok """
    if isLogo(key,data,config_data):
        logo += cf.get_logo(key,config_data)
    return logo

def make_logo(data,config_data):
    """ return a total logo for a specific note of a specific date"""
    logo = ""
    keys_good_order = ["MOTO","BOR","PER","MATIN","MIDI","APREM","NUIT","1","9","12","17","42","54","58","60"]
    for i in keys_good_order:
        logo = update_logo(i,logo,data,config_data)
    return logo

def make_title(data,config_data):
    """ return a note title with this format : MM-DD WEEKDAY_LETTER LOGO START_HOUR START_PLACE    """
    month = cf.int2digit(data["MONTH"])
    day = cf.int2digit(data["DAY"])
    M_D = month+"-"+day
    logo = make_logo(data, config_data)
    title = "{} {} {} {} {}\n".format(M_D,data["WEEKDAY"],logo,data["H_I"][0],data["L_I"][0])
    return title

def make_summary(data,config_data):
    """ return a summary of the day with this format :
    -----
        TURN DD/MM/YYYY

        CAR[k]
        P_i[k] L_i[k] H_i[k] H_f[k] L_f[k] P_f[k]
        CAR[k+1]
        ...
    -----"""

    day = cf.int2digit(data["DAY"])
    month = cf.int2digit(data["MONTH"])
    summary = "{TURN} {DAY}/{MONTH}/{YEAR}\n\n".format(**data)

    if all((section != None and len(section)==len(data["CAR"]))  for section in [data["CAR"],data["P_I"],data["L_I"],data["H_I"],data["H_F"],data["L_F"],data["P_F"]]):
        for i in range(len(data["CAR"])):
            summary += "{}\n{} {} {} {} {} {}\n".format(data["CAR"][i],data["P_I"][i],data["L_I"][i],data["H_I"][i],data["H_F"][i],data["L_F"][i],data["P_F"][i])
    else: summary = "_SUMMARY_INFEASIBLE"

    return summary

def make_details(data,config_data):
    """ WIP : return a string of the detailed information of a specific date"""
    return "_DETAILS_"

def construct_card(path,config_data,debug = False):
    """ return a note (string) from pdf file to upload on simplenote """
    data = ext.extract_data(path)
    note = make_title(data,config_data) +"\n"+ make_summary(data,config_data)+ "\n" + make_details(data,config_data)

    if debug :
        print("¨¨¨¨¨¨¨¨¨\n")
        print(note)
        print("\n¨¨¨¨¨¨¨¨¨")
        db.print_data(data)
        print("\n---------------------------------------------------------------------------------------------------\n")
    return note
