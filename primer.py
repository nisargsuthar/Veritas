from colors import *

def colorBytes(data, col, pos, howmany):
	data.insert(pos, col)
	data.insert(pos+howmany, cc)
	# print(data)
	return data

def escapeMarkup(data):
	return [c.replace("&", "&amp;").replace("[", "&bl;").replace("]", "&br;") for c in data]

def listToString(s): 
    string = ""
    for char in s: 
        string += char  
    return string 