import simplenote as sn
import os
import construction as cn
import config as cf
import extraction as ex

def add_break(id_SN,d,m,y,type):
    note = cn.construct_break(d,m,y,type)
    if cf.upload : id_SN.add_note(note)

def add_holiday(id_SN,d0,m0,y0,d1,m1,y1):
    notes = cn.construct_holidays(d0,m0,y0,d1,m1,y1)
    for note in notes :
        if cf.upload : id_SN.add_note(note)

def add_agentcard(id_SN,folder,DEBUG = False):
    pathfiles = sorted([f for f in os.listdir(folder) if f.endswith('.pdf')])
    for path in pathfiles :
        note = cn.construct_card(folder+path,debug = DEBUG )
        if cf.upload : id_SN.add_note(note)

def outdate():
    """
    Delete all outdated notes
    """
    print(" outdate() is not implemented yet")
