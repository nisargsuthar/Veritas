import binascii
from colors import color_dict

def colorBytes(data, col, pos, howmany):
    return data[:pos] + [col] + data[pos:pos + howmany - 1] + ["[/color]"] + data[pos + howmany - 1:]

def escapeMarkup(data):
    escaped_data = []
    replacements = {
        "&": "&amp;",
        "[": "&bl;",
        "]": "&br;"
    }
    for c in data:
        if c in replacements:
            escaped_data.append(replacements[c])
        else:
            escaped_data.append(c)
    return escaped_data

def listToString(s):
    return ''.join([str(char) for char in s])

def readPartialFile(file_path, numberofbytestoread):
    with open(file_path, 'rb') as f:
        data = f.read(numberofbytestoread)
        hexdata = [format(byte, '02x') for byte in data]
    return hexdata

def readFile(file_path):
	formattedhexdata = []
	hexdata = []
	formattedasciidata = []
	bytecount = 0
	with open(file_path, 'rb') as f:
		while True:
			byte = f.read(1)
			if not byte:
				break
			bytecount += 1
			asciichar = int.from_bytes(byte, "big")
			hex_str = binascii.hexlify(byte).decode("cp1252")
			hexdata.append(hex_str)
			ascii_str = chr(asciichar) if 32 <= asciichar <= 126 else "."
			if bytecount % 16 == 0:
				hex_str += "\n"
				ascii_str += "\n"
			formattedhexdata.append(hex_str)
			formattedasciidata.append(ascii_str)
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