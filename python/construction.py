import extraction as ext
import config as cf
import datetime as dt

def construct_break(date,t,config_data):
    """ return a string named note formated for break day"""
    l = ext.weekday(date)
    d = cf.int2digit(date.day)
    m = cf.int2digit(date.month)
    logo = cf.get_logo("CONGE",config_data)
    return "{}-{} {} {} \n\n {}".format(d,m,l,logo,t)

def construct_holiday(date,config_data):
    """ return a string named note formated for holiday day"""
    d = cf.int2digit(date.day)
    m = cf.int2digit(date.month)
    l = ext.weekday(date)
    logo = cf.get_logo("VACANCE",config_data)
    return "{}-{} {} {}️".format(d,m,l,logo)

def construct_holidays(date0,date1,config_data):
    """ return a list of notes formated for holiday days"""
    notes = []
    date = date0
    while (date != (date1 + dt.timedelta(days=1))):
        notes.append(construct_holiday(date,config_data))
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
        "RADIO":any(key in v_list for key in config_data["LRADIO"]),
        "TD":any(key in v_list for key in config_data["LTD"]),
        "FORM":any(key in v_list for key in config_data["LSPE"]),
        "TR":any(key in v_list for key in config_data["LSPE"]),
        "1": any(key in v_list for key in config_data["L1"]),
        "9": any(key in v_list for key in config_data["L9"]),
        "12":any(key in v_list for key in config_data["L12"]),
        "17":any(key in v_list for key in config_data["L17"]),
        "42":any(key in v_list for key in config_data["L42"]),
        "54":any(key in v_list for key in config_data["L54"]),
        "58":any(key in v_list for key in config_data["L58"]),
        "60":any(key in v_list for key in config_data["L60"]),

    }.get(key, False)

def update_logo(logo,key,data,config_data):
    """ return a total logo with addition of specific logo if specific condition is ok """
    if isLogo(key,data,config_data):
        logo += cf.get_logo(key,config_data)
    return logo

def make_logo(data,config_data):
    """ return a total logo for a specific note of a specific date"""
    logo = ""
    keys_good_order = ["MOTO","BOR","PER","MATIN","MIDI","APREM","NUIT","1","9","12","17","42","54","58","60","FORM","TD"]
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

def construct_card(path,config_data):
    """ return a note (string) from pdf file to upload on simplenote """
    data = ext.extract_data(path)
    date = dt.datetime(data["YEAR"],data["MONTH"],data["DAY"])
    if date < dt.datetime.today()-dt.timedelta(days=1):
        return "PAST"
    else :
        note = make_title(data,config_data) +"\n"+ make_summary(data,config_data)+ "\n" + make_details(data,config_data)
        return note
