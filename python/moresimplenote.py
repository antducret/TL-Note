import simplenote as sn
import os
import construction as cn
import config as cf
import debug as db
import extraction as ex
import datetime as dt

def add_break(date,type,config,tags,id_SN):
    """ upload a note for breakday on simple note"""
    note = cn.construct_break(date,type,config)
    upload_note(note,date,tags,id_SN)

def add_holiday(date0,date1,config_data,tags,id_SN):
    """ upload a note for holiday on simple note"""
    numdays = (date1-date0).days
    dates = [date0 + dt.timedelta(days=x) for x in range(numdays)]
    notes = cn.construct_holidays(date0,date1,config_data)
    for i in range(numdays) :
        upload_note(notes[i],dates[i],tags,id_SN)

def add_agentcard(folder,config_data,tags,id_SN,DEBUG = False):
    """ upload a note for work days on simple note"""
    pathfiles = sorted([f for f in os.listdir(folder) if f.endswith('.pdf')])
    for path in pathfiles :
        note = cn.construct_card(folder+path,config_data,debug = DEBUG)
        if note != "PAST": upload_note(note,date,tags,id_SN)

def upload_note(note,date,tags,id_SN):
    dict_note = dict()
    dict_note["key"] = date.strftime("%d_%m_%Y")
<<<<<<< HEAD
    if date.year == dt.datetime.today().year and note[0]!="-" : note = "-"+note
=======
>>>>>>> f82bd2ee5c9640a23ab0333e35297e6a06ca2387
    dict_note["content"] = note
    dict_note["tags"] = ["TEST"] #TODO : Change to "tags" when ready to upload real data
    db.print_data(dict_note)
    if cf.UPLOAD :
        id_SN.update_note(dict_note)

def outdate(id_SN):
    """ WIP:  delete all outdated notes """
<<<<<<< HEAD
=======
    #outdated_keys = [(dt.date.today() - dt.timedelta(days=x)).strftime("%d_%m_%Y") for x in range(1,731)]
>>>>>>> f82bd2ee5c9640a23ab0333e35297e6a06ca2387
    all_notes = id_SN.get_note_list(data = False)[0]
    for note in all_notes:
        if "_" in note["key"]:
            date_note = dt.datetime.strptime(note["key"],"%d_%m_%Y")
            if  date_note < dt.datetime.today() :
                id_SN.delete_note(note["key"])
            elif date_note.year == dt.datetime.today().year :
                dict_note = id_SN.get_note(note["key"])
                if dict_note["content"][0] != "-":
                    dict_note["content"] = "-"+dict_note["content"]
                    id_SN.update_note(dict_note)
