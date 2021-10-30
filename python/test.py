#!/usr/bin/env python3
import config as cf
import debug as db
import moresimplenote as msn
import simplenote as sn


# control a particular pdf file
if 0 :
    m = 11
    d = 11

    m = "0" + str(m) if len(str(m)) == 1 else str(m)
    d = "0" + str(d) if len(str(d)) == 1 else str(d)

    path = "./pers/INPUT/{}-{}.pdf".format(m,d)
    print(pdf2text(path))
    db.print_data(extract_data(path))

# add folder of cards
if 0 :
    id =  cf.get_id()
    id_SN = sn.Simplenote(id["ID"][0],id["PW"][0])
    msn.add_agentcard(id_SN,"./pers/INPUT/",DEBUG = db.debug)
