import simplenote as sn
import os
import debug as db
import construction as cn
import config as cf
import extraction as ext
import datetime as dt

def add_break(date,type,config,tags,id_SN):
    """ call upload for a note for breakday on simple note"""
    note = cn.construct_break(date,type,config)
    upload_note(note,date,tags,id_SN)
    print("BREAK")

def add_holiday(date0,date1,config,tags,id_SN):
    """ call upload for a note for holiday on simple note"""
    numdays = (date1-date0).days
    dates = [date0 + dt.timedelta(days=x) for x in range(numdays+1)]
    notes = cn.construct_holidays(date0,date1,config)
    for i in range(numdays+1) :
        upload_note(notes[i],dates[i],tags,id_SN)
    print("HOLIDAY")

def add_agentcard(folder,config,tags,id_SN):
    """ call upload for a note for work days on simple note"""
    print("PDF to Simplenote")
    print("\tFinding all pdf cards ...")
    pathfiles = sorted([f for f in os.listdir(folder) if f.endswith('.pdf')])
    print("\tConstruction and uploading corresponding notes ...")
    for path in pathfiles :
        note,date = cn.construct_card(folder+"/"+path,config)
        if note != "PAST":
            upload_note(note,date,tags,id_SN)
            print("WORK")
    print("DONE !")

def upload_note(note,date,tags,id_SN):
    dict_note = dict()
    dict_note["key"] = date.strftime("%d_%m_%Y")
    if date.year == dt.datetime.today().year and note[0]!="-" : note = "-"+note
    dict_note["content"] = note
    dict_note["tags"] = tags
    if cf.UPLOAD :
        print("\t",dict_note["key"],"constructed",end=" ")
        id_SN.update_note(dict_note)
        print("uploaded",end=" " )

def delete_test_note(id_SN):
    print("Deleting test notes ...")
    print("\tLoading TEST notes ...")
    all_notes = id_SN.get_note_list(data = True,tags=["TEST"])[0]
    print("\tDeleting TEST notes ...")
    for note in all_notes:
        id_SN.delete_note(note["key"])
        print("\t\t",note["key"])
    print("\tDone")

def update(id_SN):
    """ WIP:  delete all outdated notes """
    print("Updating notes ...")
    print("\tLoading all notes ...")
    all_notes = id_SN.get_note_list(data = False)[0]
    print("\tUpdating ...")
    for note in all_notes:
        if "_" in note["key"]:
            date_note = dt.datetime.strptime(note["key"],"%d_%m_%Y")
            if  date_note < dt.datetime.today() :
                id_SN.delete_note(note["key"])
                print("\t\t",note["key"],"outdated")
            elif date_note.year == dt.datetime.today().year :
                dict_note = id_SN.get_note(note["key"])[0]
                if (dict_note["content"])[0] != "-":
                    dict_note["content"] = "-"+dict_note["content"]
                    id_SN.update_note(dict_note)
                    print("\t\t",note["key"],"new year : begin with \"-\" ")
    print("\tDone")
