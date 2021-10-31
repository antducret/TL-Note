import csv
import emoji

UPLOAD = 0
CONFIG_FILE = "./config/config.csv"
ID_FILE = "./pers/id.csv"
TAGS_FILE = "./pers/tags.csv"

def get_config():
    """ return a dictionary containing all the data in config.csv """
    config_data = dict()
    with open(CONFIG_FILE,'r') as data:
       for line in csv.reader(data,delimiter = ";"):
           config_data[line[0]]  = [x for x in line[1].split(',')]
    return config_data

def print_cf():
    """ print all the data contained in config.csv """
    data = get_config()
    for i in data:
        print(i,(10-len(i))*" ",lg(i) if (data[i][0][0] == ":") else data[i])

def get_id():
    """ return a dictionary containing all the id data in id.csv"""
    id = dict()
    with open(ID_FILE,'r') as data:
       for line in csv.reader(data,delimiter = ";"):
            id[line[0]] = line[1].split(',')
    return id

def get_tags():
    """ return a list containing all the tags in tags.csv"""
    tags = []
    with open(TAGS_FILE,'r') as data:
        for line in csv.reader(data,delimiter = ";"):
            tags.append(line)
    return tags

def get_logo(key,config_data):
    """ return the string "emoji" corresponding to the CLDR code at config_data[key]  """
    return emoji.emojize(config_data[key][0])

def int2digit(int):
    """ return a double digit string of an int """
    string = int = "0"+str(int) if len(str(int)) == 1 else str(int)
    return string
