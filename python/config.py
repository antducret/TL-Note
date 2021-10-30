import csv
import emoji

upload = 0

def get_config():

    filename="./config/config.csv"
    config_data = dict()

    with open(filename,'r') as data:
       for line in csv.reader(data,delimiter = ";"):
           config_data[line[0]]  = [x for x in line[1].split(',')]
    return config_data

def print_cf():
    data = get_config()
    for i in data:
        print(i,(10-len(i))*" ",lg(i) if (data[i][0][0] == ":") else data[i])

def get_id():

    filename="./pers/id.csv"
    id = dict()

    with open(filename,'r') as data:
       for line in csv.reader(data,delimiter = ";"):
            id[line[0]] = line[1].split(',')
    return id

def lg(key):
    data = get_config()
    return emoji.emojize(data[key][0])

#print_cf()
