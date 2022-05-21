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

def fixHex(data):
	bi = 0
	colors = {}
	removeEndIndices = []
	while bi < len(data):
		currentByte = data[bi:bi+2]
		if " " in currentByte:
			bi += 1
			continue
		elif "\n" in currentByte:
			bi += 1
			if data[bi:bi+2] == "[/":
				removeEndIndices.append(bi)
			else:
				colors.update({bi: lastColor})
		match currentByte:
			case "[c":
				lastColor = data[bi+7:bi+7+6]
				bi += 14
			case "[/":
				bi += 6
				lastColor = ""
		bi += 2
	
	colors = {key:val for key, val in colors.items() if val != ""}
	
	for key, val in reversed(colors.items()):
		data = data[:key] + "[color={}]".format(val) + data[key:]

	return data.replace("\n[/color]", "\n")

def fixAscii(data):
	bi = 0
	colors = {}
	removeEndIndices = []
	while bi < len(data):
		currentByte = data[bi:bi+1]
		if currentByte == "\n":
			bi += 1
			if data[bi:bi+2] == "[/":
				removeEndIndices.append(bi)
			else:
				colors.update({bi: lastColor})
		match currentByte:
			case "[" if data[bi+1:bi+2] == "c":
				lastColor = data[bi+7:bi+7+6]
				bi += 14
			case "[" if data[bi+1:bi+2] == "/":
				bi += 7
				lastColor = ""
		bi += 1
	
	colors = {key:val for key, val in colors.items() if val != ""}
	
	for key, val in reversed(colors.items()):
		data = data[:key] + "[color={}]".format(val) + data[key:]

	return data.replace("\n[/color]", "\n")