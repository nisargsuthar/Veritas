import binascii
import re

def colorBytes(data, col, pos, howmany):
	return data[:pos] + [col] + data[pos:pos + howmany - 1] + ["[/color]"] + data[pos + howmany - 1:]

def escapeMarkup(data):
	escaped_data = []
	replacements = {
		"&": "&amp;", "[": "&bl;", "]": "&br;",
		"&\n": "&amp;\n", "[\n": "&bl;\n", "]\n": "&br;\n",
	}
	for s in data:
		if s in replacements:
			escaped_data.append(replacements[s])
		else:
			escaped_data.append(s)
	return escaped_data

def listToString(l):
	return ''.join([str(char) for char in l])

def readPartialFile(file_path, numberofbytestoread):
	with open(file_path, 'rb') as f:
		data = f.read(numberofbytestoread)
		hexdata = [format(byte, '02X') for byte in data]
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
			hex_str = binascii.hexlify(byte).decode("cp1252").upper()
			hexdata.append(hex_str)
			ascii_str = chr(asciichar) if 32 <= asciichar <= 126 else "."
			if bytecount % 16 == 0:
				hex_str += "\n"
				ascii_str += "\n"
			else:
				hex_str += " "
			formattedhexdata.append(hex_str)
			formattedasciidata.append(ascii_str)
	return formattedhexdata, formattedasciidata, hexdata

def joinOffsetHexAscii(offsetdata, hexdata, asciidata):
	return {"offsettext": offsetdata, "hextext": hexdata, "asciitext": asciidata}

def getOffsets(bytecount):
	bytecount += 16 if bytecount % 16 != 0 else 0
	offsetdata = [f"{i:06X}" for i in range(0, bytecount, 16)]
	return offsetdata

def fixColorTags(data):
	data = data.replace("[/color]", "")
	data_lines = data.split('\n')
	output_lines = []
	current_color = None
	for line in data_lines:
		if line and line[0] != "[":
			output_lines.append(f"[color={current_color}]{line}")
		else:
			output_lines.append(line)
		color_matches = list(re.finditer(r'\[color=([0-9A-F]{6})\]', line))
		if color_matches:
			current_color = color_matches[-1].group(1)
	return '\n'.join(output_lines)