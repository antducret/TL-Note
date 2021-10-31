#!/usr/bin/env python3
import config as cf
import debug as db
import datetime as dt
import extraction as ext
import moresimplenote as msn
import simplenote as sn


# control a particular pdf file
if 0:
    m = 11
    d = 11
    path = "./pers/INPUT/{}-{}.pdf".format(m,d)
    print(ext.pdf2text(path))
    db.print_data(ext.extract_data(path))

# add folder of cards
if 1:
    id =  cf.get_id()
    id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])
    config_data = cf.get_config()
    msn.add_agentcard("./pers/INPUT/",config_data,["TEST"],id_SN)

# upload note
if 0:
    id =  cf.get_id()
    id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])
    date = dt.datetime(2010,1,1)
    msn.upload_note("_NOTE_",date,"", id_SN)
