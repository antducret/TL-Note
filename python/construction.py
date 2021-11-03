import extraction as ext
import config as cf
import datetime as dt
import re

def construct_break(date,t,config):
    """ return a string named note formated for break day"""
    l = ext.weekday(date)
    d = cf.int2digit(date.day)
    m = cf.int2digit(date.month)
    logo = cf.get_logo("CONGE",config)
    return "{}-{} {} {}  {}".format(d,m,l,logo,t)
def construct_holiday(date,config):
    """ return a string named note formated for holiday day"""
    d = cf.int2digit(date.day)
    m = cf.int2digit(date.month)
    l = ext.weekday(date)
    logo = cf.get_logo("VACANCE",config)
    return "{}-{} {} {}️".format(d,m,l,logo)
def construct_holidays(date0,date1,config):
    """ return a list of notes formated for holiday days"""
    notes = []
    date = date0
    while (date != (date1 + dt.timedelta(days=1))):
        notes.append(construct_holiday(date,config))
        date += dt.timedelta(days=1)
    return notes
def isLogo(key,data,config):
    """ return a boolean to know if a specific logo must be added based on data of a day"""
    h_i = int(data["H_I"][0][:2])
    h_f = int(data["H_F"][-1][:2])
    v_list = [(re.search('\d{1,2}', key)[0] if key[0].isdigit() else key) for key in data["CAR"]]
    return {
        "MOTO": (data["L_I"][0] == data["L_F"][-1] and data["L_I"][0] not in config["DEPOTS"]),
        "BOR" : (data["L_F"][-1] in config["DEPOTS_BOR"]),
        "PER" : (data["L_F"][-1] in config["DEPOTS_PER"]),
        "MATIN" :(h_i>= int(config["H_MATIN"][0]) and h_i< int(config["H_MIDI"][0])),
        "MIDI" :(h_i>= int(config["H_MIDI"][0]) and h_i< int(config["H_APREM"][0])),
        "APREM" :(h_i>= int(config["H_APREM"][0]) and h_i< int(config["H_NUIT"][0]) and h_f < 24),
        "NUIT" : (h_i>= int(config["H_NUIT"][0]) or h_f>=24),
        "RADIO":any(key in v_list for key in config["LRADIO"]),
        "TD":any(key in v_list for key in config["LTD"]),
        "SPE":any(key in v_list for key in config["LSPE"]),
        "1": any(key in v_list for key in config["L1"]),
        "9": any(key in v_list for key in config["L9"]),
        "12":any(key in v_list for key in config["L12"]),
        "17":any(key in v_list for key in config["L17"]),
        "42":any(key in v_list for key in config["L42"]),
        "50":any(key in v_list for key in config["L50"]),
        "54":any(key in v_list for key in config["L54"]),
        "58":any(key in v_list for key in config["L58"]),
        "60":any(key in v_list for key in config["L60"]),

    }.get(key, False)
def update_logo(logo,key,data,config):
    """ return a total logo with addition of specific logo if specific condition is ok """
    if isLogo(key,data,config):
        logo += cf.get_logo(key,config)
    return logo
def make_logo(data,config):
    """ return a total logo for a specific note of a specific date"""
    logo = ""
    keys_good_order = ["MOTO","BOR","PER","MATIN","MIDI","APREM","NUIT","1","9","12","17","42","50","54","58","60","RADIO","SPE","TD"]
    for key in keys_good_order:
        logo = update_logo(logo,key,data,config)
    return logo
def make_title(data,config):
    """ return a note title with this format : MM-DD WEEKDAY_LETTER LOGO START_HOUR START_PLACE    """
    month = cf.int2digit(data["MONTH"])
    day = cf.int2digit(data["DAY"])
    M_D = month+"-"+day
    logo = make_logo(data, config)
    title = "{} {} {} {} {}\n".format(M_D,data["WEEKDAY"],logo,data["H_I"][0],data["L_I"][0])
    return title
def make_summary(data,config):
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
    summary = "{} {}/{}/{}\n\n".format(data["TURN"],day,month,data["YEAR"])

    if all((section != None and len(section)==len(data["CAR"]))  for section in [data["CAR"],data["P_I"],data["L_I"],data["H_I"],data["H_F"],data["L_F"],data["P_F"]]):
        for i in range(len(data["CAR"])):
            summary += "{}\n{} {} {} {} {} {}\n".format(data["CAR"][i],data["P_I"][i],data["L_I"][i],data["H_I"][i],data["H_F"][i],data["L_F"][i],data["P_F"][i])
    else: summary = "_SUMMARY_INFEASIBLE"

    return summary
def sort_lines(data):
    """ return a list of lines in chronologic order """
    d_h = data["DOUBLE_HOUR"]
    breakword = data["KEYWORD"]
    breakline = [ breakword[i]+"\t\t"+d_h[i] for i in range(len(d_h))]
    list = data["DOTLINE"]
    list = sorted(list, key = lambda x: x[-5:])
    list += breakline
    list = sorted(list, key = lambda x: x[-5:])
    return list
def make_details(data,config):
    """ return a string of the detailed information of a specific date"""
    lines = ["Voiture "+data["CAR"][0]]+sort_lines(data)
    copylines = lines.copy()
    k = 1
    for i in range(len(lines)) :
        if "Coupure" in lines[i] or "Interruption" in lines[i]: # Retour à la ligne avant-après breakline + Nextvoiture
            copylines[i] = "\n"+lines[i]+"\n\n"+"Voiture "+data["CAR"][k]
            k += 1
        if re.search("\d+\s*/\s*\d+\s+",lines[i]) != None: # Retour à la ligne entre voiture/numéro et dotline
            carnum = re.search("\d+\s*/\s*\d+\s+",lines[i])[0]
            copylines[i] = carnum+"\n"+re.sub("\d+\s*/\s*\d+\s+","",lines[i])
    details = "\n".join(copylines)
    return details
def construct_card(path,config):
    """ return a note (string) from pdf file to upload on simplenote """
    data = ext.extract_data(path)
    date = dt.datetime(data["YEAR"],data["MONTH"],data["DAY"])
    if date < dt.datetime.today()-dt.timedelta(days=1):
        return "PAST",date
    else :
        note = make_title(data,config) +"\n"+ make_summary(data,config)+ "\n" + make_details(data,config)
        return note,date
