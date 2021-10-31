import textract as tx
import datetime as dt
import debug as db
import re

def weekday(date):
    """ return the first french letter for each weekday """
    letters = ["L","M","W","J","V","S","D"]
    return letters[date.weekday()]

def pdf2text(path):
    """ return a text file from pdf """
    text = tx.process(path)
    return text.decode("utf-8")

def extract_data(path):
    """ extract all data from a pdf returning a dictionary """
    txt = pdf2text(path)
    data = dict()

    # Date information
    date = re.search('\d{2}/\d{2}/\d{4}', txt)[0]
    date_tab = date.split("/")
    data["DAY"] =  int(date_tab[0])
    data["MONTH"] = int(date_tab[1])
    data["YEAR"] = int(date_tab[2])
    data["WEEKDAY"] = weekday(data["DAY"],data["MONTH"],data["YEAR"])

    # General info
    data["AGENT"] = re.search('\(\d{4}\)', txt)[0][1:-1]
    data["TURN"] = re.search('\d{5}', txt)[0]
    tmp_type = re.search('jrn.\s.*\s', txt)[0]
    tmp_type = re.sub("jrn.\s","",tmp_type)
    data["TYPE"] = re.search('Voiture|Radio|Form', txt)[0]

    # --- SPECIFIC DATA -----

    # Voiture
    CAR_tmp = re.search('Voiture\s+((\d+ +\- +\d+\s+)|Radio|Form|TD)+', txt)
    CAR_tmp = CAR_tmp[0][9:].split("\n") if CAR_tmp != None else ["00000"]
    data["CAR"] = [x for x in CAR_tmp if x]

    # Prise début
    P_I_tmp = re.search('Prise\sdébut\s(\d{2}:\d{2}\n)+\s', txt)
    P_I_tmp = P_I_tmp[0][12:].split("\n") if P_I_tmp != None else ["00000"]
    data["P_I"] = [x for x in P_I_tmp if x]

    # Lieu début
    L_I_tmp = re.search('Lieu\s(début)+\s(.+\n)+\s', txt)
    L_I_tmp = L_I_tmp[0][11:].split("\n") if L_I_tmp != None else ["00000"]

        #FIX (bug with mixed L_I, H_I)
    L_I_H_I_tmp = [x for x in L_I_tmp if x and "début" not in x]
    L_I_tmp = [re.search("[A-Z0-9\.]+",x)[0] for x in L_I_H_I_tmp if re.search("[A-Z]+",x)]

    data["L_I"] = [x for x in L_I_tmp if x]

    # Tour début
    H_I_tmp = re.search('Heure\sdébut\s(\d{2}:\d{2}\n)+\s', txt)
    H_I_tmp = H_I_tmp[0][11:].split("\n") if H_I_tmp != None else [re.search("\d{2}:\d{2}",x)[0] for x in L_I_H_I_tmp if re.search("\d{2}:\d{2}",x)]

    data["H_I"] = [x for x in H_I_tmp if x]

    # Tour fin
    H_F_tmp = re.search('Heure\sfin\s(\d{2}:\d{2}\n)+\s', txt)
    H_F_tmp = H_F_tmp[0][9:].split("\n") if H_F_tmp != None else ["00000"]

    data["H_F"] = [x for x in H_F_tmp if x]

    # Lieu fin
    L_F_tmp = re.search('Lieu\sfin\s(.+\n)+\s', txt)
    L_F_tmp = L_F_tmp[0][9:].split("\n") if L_F_tmp != None else ["00000"]

        #FIX (bug with mixed L_F, H_I)
    L_F_H_F_tmp = [x for x in L_F_tmp if "fin" not in x]
    L_F_tmp = [re.search("[A-Z0-9\.]+",x)[0] for x in L_F_H_F_tmp if re.search("[A-Z]+",x)]

    data["L_F"] = [x for x in L_F_tmp if x]

    # Prise fin ----
    P_F_tmp = re.search('Prise\sfin\s(\d{2}:\d{2}\n)+\s', txt)
    P_F_tmp = P_F_tmp[0][10:].split("\n") if P_F_tmp != None else [re.search("\d{2}:\d{2}",x)[0] for x in L_F_H_F_tmp if re.search("\d{2}:\d{2}",x)]

    data["P_F"] = [x for x in P_F_tmp if x]

    # Further details to determine

    # Used for DEBUG
    data["TAB"] = [x for x in txt.split("\n")[:50] if x not in [""," ","\n","\n "]]
    data["SOURCE"] = re.search('\d{2}/\d{2}/\d{4} \d{2}:\d{2}', [x for x in txt.split("\n") if "HASTUS" in x][0])[0]

    return data
