import extraction as ext
import config as cf
import debug as db
import datetime as dt

def construct_break(d,m,y,t):
    d = str(d)[2:-2]
    m = str(m)[2:-2]
    y = str(y)[2:-2]
    t = str(t)[2:-2]
    l = ext.weekday(d,m,y)
    logo = cf.lg("CONGE")
    return "{}-{} {} {} \n\n {}".format(d,m,l,logo,t)
def construct_holiday(date):
    d = date.day
    m = date.month
    y = date.year
    l = ext.weekday(d,m,y)
    d = "0"+str(d) if len(str(d)) == 1 else str(d)
    m = "0"+str(m) if len(str(m)) == 1 else str(m)
    logo = cf.lg("VACANCE")
    txt = "{}-{} {} {}️".format(d,m,l,logo)
    return txt
def construct_holidays(d0,m0,y0,d1,m1,y1):
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
        notes.append(construct_holiday(date))
        date += dt.timedelta(days=1)
    return notes
def cond(data,x):
    config = cf.get_config()
    h_i = int(data["H_I"][0][:2])
    h_f = int(data["H_F"][-1][:2])
    v_list = [x[:2] for x in data["CAR"] if x[:2].isdigit()]
    return {
        "MOTO": (data["L_I"][0] == data["L_F"][-1] and data["L_I"][0] not in config["DEPOTS"]),
        "BOR" : (data["L_F"][-1] in config["DEPOTS_BOR"]),
        "PER" : (data["L_F"][-1] in config["DEPOTS_PER"]),
        "MATIN" :(h_i>= int(config["H_MATIN"][0]) and h_i< int(config["H_MIDI"][0])),
        "MIDI" :(h_i>= int(config["H_MIDI"][0]) and h_i< int(config["H_APREM"][0])),
        "APREM" :(h_i>= int(config["H_APREM"][0]) and h_i< int(config["H_NUIT"][0]) and h_f < 24),
        "NUIT" : (h_i>= int(config["H_NUIT"][0]) or h_f>=24),
        "1":any(x in v_list for x in config["L1"]),
        "9":any(x in v_list for x in config["9"]),
        "12":any(x in v_list for x in config["12"]),
        "17":any(x in v_list for x in config["17"]),
        "42":any(x in v_list for x in config["42"]),
        "54":any(x in v_list for x in config["54"]),
        "58":any(x in v_list for x in config["58"]),
        "60":any(x in v_list for x in config["60"]),
    }.get(x, False)
def update_logo(key,logo,data):
    #print(key," : ",cond(data,key))
    if cond(data,key):
        logo += cf.lg(key)
    return logo
def make_logo(data):
    config = cf.get_config()
    logo = ""
    keys_good_order = ["MOTO","BOR","PER","MATIN","MIDI","APREM","NUIT","1","9","12","17","42","54","58","60"]
    for i in keys_good_order:
        logo = update_logo(i,logo,data)
    return logo
def make_title(data):
    """
    Crée le titre selon ce format : MOIS-JOUR JOUR_SEMAINE CODE_LOGO HEURE_DEBUT LIEU_DEBUT
    """
    d = data
    month_tmp = "0" + str(d["MONTH"]) if len(str(d["MONTH"])) == 1 else str(d["MONTH"])
    day_tmp = "0" + str(d["DAY"]) if len(str(d["DAY"])) == 1 else str(d["DAY"])
    M_D = month_tmp+"-"+day_tmp
    logo = make_logo(d)
    title = "{} {} {} {} {}\n".format(M_D,d["WEEKDAY"],logo,d["H_I"][0],d["L_I"][0])

    return title
def make_summary(data):
    """
    Retourn un résumé de la journée dans ce format :
    -----
        TOUR JJ/MM/YYYY

        VOIT[k]
        P_i[k] L_i[k] H_i[k] H_f[k] L_f[k] P_f[k]
        VOIT[k+1]
        ...
    -----
    """
    d = data
    d["DAY"] = "0"+str(d["DAY"]) if len(str(d["DAY"])) == 1 else str(d["DAY"])
    d["MONTH"] = "0"+str(d["MONTH"]) if len(str(d["MONTH"])) == 1 else str(d["MONTH"])
    summary = "{TURN} {DAY}/{MONTH}/{YEAR}\n\n".format(**d)
    if all((x != None and len(x)==len(d["CAR"]))  for x in [d["CAR"],d["P_I"],d["L_I"],d["H_I"],d["H_F"],d["L_F"],d["P_F"]]):
        for i in range(len(d["CAR"])):
            summary += "{}\n{} {} {} {} {} {}\n".format(d["CAR"][i],d["P_I"][i],d["L_I"][i],d["H_I"][i],d["H_F"][i],d["L_F"][i],d["P_F"][i])
    else: summary = "_SUMMARY_INFEASIBLE"
    return summary
def make_details(data):
    return "_DETAILS_"
def construct_card(path,debug = False):
    data = ext.extract_data(path)
    note = make_title(data) +"\n"+ make_summary(data)+ "\n" + make_details(data)
    if debug :
        print("¨¨¨¨¨¨¨¨¨\n")
        print(note)
        print("\n¨¨¨¨¨¨¨¨¨")
        db.print_data(data)
        print("\n---------------------------------------------------------------------------------------------------\n")
    return note
