import simplenote as sn
import os
import construction as cn
import config as cf
import extraction as ex
import datetime as dt

def add_break(d,m,y,type,config_data,id_SN):
    """ upload a note for breakday on simple note"""
    note = cn.construct_break(d,m,y,type,config_data)
    date = dt.datetime(y,m,d)
    upload_note(note, date, id_SN)

def add_holiday(d0,m0,y0,d1,m1,y1,config_data,id_SN):
    """ upload a note for holiday on simple note"""
    date0 = dt.datetime(y0,m0,d0)
    date1 = dt.datetime(y1,m1,d1)
    if date0 > date1:
        return 0
    else :
        numdays = (date1-date0).days
        dates = [date0 + datetime.timedelta(days=x) for x in range(numdays)]
        notes = cn.construct_holidays(d0,m0,y0,d1,m1,y1,config_data)
        for i in range(len(notes)) :
            upload_note(notes[i],dates[i],id_SN)
        return 1

def add_agentcard(folder,config_data,id_SN,DEBUG = False):
    """ upload a note for work days on simple note"""
    pathfiles = sorted([f for f in os.listdir(folder) if f.endswith('.pdf')])
    for path in pathfiles :
        note,date = cn.construct_card(folder+path,config_data,debug = DEBUG )
        upload_note(note,date,id_SN)

def upload_note(note,date,id_SN):
    if cf.UPLOAD :
        dict_note["key"] = "DATE"
        dict_note["content"] = "NOTE"
        dict_note["tags"] = "TAGS"
        id_SN.add_note(dict_note)
    else :
        pass


def outdate():
    """ WIP:  delete all outdated notes """
    pass
