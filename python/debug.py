from warnings import warn as warnings

debug = 1

def print_data(data):
    for i in data:
        print("\n",i,":",(data[i]))

def warn(txt):
    format = "\x1b[0;31;47m"
    txt = format+"\n"+txt+"\n"
    warnings(txt)
