import simplenote as sn
import os
import construction as cn
import config as cf
import extraction as ex

def add_break(d,m,y,type,config_data,id_SN):
    """ upload a note for breakday on simple note"""
    note = cn.construct_break(d,m,y,type)
    if cf.UPLOAD : id_SN.add_note(note)

def add_holiday(d0,m0,y0,d1,m1,y1,config_data,id_SN):
    """ upload a note for holiday on simple note"""
    notes = cn.construct_holidays(d0,m0,y0,d1,m1,y1)
    for note in notes :
        if cf.UPLOAD : id_SN.add_note(note)

def add_agentcard(folder,config_data,id_SN,DEBUG = False):
    """ upload a note for work days on simple note"""
    pathfiles = sorted([f for f in os.listdir(folder) if f.endswith('.pdf')])
    for path in pathfiles :
        note = cn.construct_card(folder+path,config_data,debug = DEBUG )
        if cf.UPLOAD : id_SN.add_note(note)

def outdate():
    """ WIP:  delete all outdated notes """
    pass
