import binascii
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

def readPartialFile(file_path, numberofbytestoread):
	hexdata = []
	bytecount = 0
	with open(file_path, 'rb') as f:
		while bytecount <= numberofbytestoread:
			byte = f.read(1)
			if not byte:
				break  # Exit the loop if end of file is reached
			bytecount += 1
			hexdata.append(byte.hex())
	return hexdata

def readFile(file_path):
	formattedhexdata = []
	hexdata = []
	formattedasciidata = []
	bytecount = 0
	with open(file_path, 'rb') as f:
		for byte in iter(lambda: f.read(1), b''):
			bytecount += 1
			asciichar = int.from_bytes(byte, "big")
			hexdata.append(binascii.hexlify(byte).decode("utf-8"))
			if bytecount % 16 == 0:
				formattedhexdata.append(binascii.hexlify(byte).decode("utf-8")+"\n")
				if asciichar >= 32 and asciichar <= 126:
					formattedasciidata.append(chr(asciichar)+"\n")
				else:
					formattedasciidata.append(".\n")
			else:
				formattedhexdata.append(binascii.hexlify(byte).decode("utf-8"))
				if asciichar >= 32 and asciichar <= 126:
					formattedasciidata.append(chr(asciichar))
				else:
					formattedasciidata.append(".")

	return formattedhexdata, formattedasciidata, hexdata

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