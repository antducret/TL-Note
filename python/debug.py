from warnings import warn as warnings

DEBUG = 1 # Define if debug mode is on/off

def print_data(data):
    """ print a dictionary called data  in a specific format """
    for i in data:
        print("\n",i,":",(data[i]))

def warn(txt):
    """ return a warning string in a specific format """
    format = "\x1b[0;31;47m"
    txt = format+"\n"+txt+"\n"
    warnings(txt)
