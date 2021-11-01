#!/usr/bin/env python3
import config as cf
import debug as db
import datetime as dt
import extraction as ext
import moresimplenote as msn
import simplenote as sn
import os


# control a particular pdf file
if 1:
    id =  cf.get_id()
    id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])
    config = cf.get_config()
    folder = "./pers/INPUT/"
    msn.add_agentcard(folder,config,["TEST"],id_SN) # DEBUG @ line 29,30  msn

# add folder of cards
if 0:
    id =  cf.get_id()
    id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])
    config = cf.get_config()
    msn.add_agentcard("./pers/INPUT/",config,["TEST"],id_SN)
# upload note
if 0:
    id =  cf.get_id()
    id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])
    date = dt.datetime(2010,1,1)
    msn.upload_note("_NOTE_",date,"", id_SN)
