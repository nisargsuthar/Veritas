def toAbsolute(template, sizes):
	for sizeindex in range(1, len(sizes)):
		# Convert sequential sizes to cumulative.
		sizes[sizeindex] += sizes[sizeindex-1]
	
	for vi in range(1, len(template)):
		# Add size of previous section to the relative offset.
		for pair in template[vi]:
			pair[0] += sizes[vi-1]
	
	returnlist = []
	for l in range(len(template)):
		returnlist += template[l]
	
	return returnlist

def swapEndianness(hexstring):
	ba = bytearray.fromhex(hexstring)
	ba.reverse()
	return ba.hex()

def parseIntByte(hexdata, byteoffset):
	return int("".join(hexdata[byteoffset]), 16)

def parseIntWord(hexdata, byteoffset, swapendianness = 0):
	value = "".join(hexdata[b] for b in range(byteoffset , byteoffset + 2))
	if not swapendianness:
		value = swapEndianness(value)
	return int(value, 16)

def parseIntDword(hexdata, byteoffset, swapendianness = 0):
	value = "".join(hexdata[b] for b in range(byteoffset , byteoffset + 4))
	if not swapendianness:
		value = swapEndianness(value)
	return int(value, 16)

def parseIntQword(hexdata, byteoffset, swapendianness = 0):
	value = "".join(hexdata[b] for b in range(byteoffset , byteoffset + 8))
	if not swapendianness:
		value = swapEndianness(value)
	return int(value, 16)

def getOffset(byteoffset):
	return f"0x{byteoffset:06X}"

def getNullTerminatedStringSize(hexstring):
	byte_data = bytes.fromhex(hexstring)
	try:
		return byte_data.index(0x00) + 1 
	except ValueError:
		return len(byte_data)
	
def getNullTerminatedUnicodeStringSize(hexstring):
	byte_data = bytes.fromhex(hexstring)
	for i in range(0, len(byte_data) - 1, 2):
		if byte_data[i] == 0x00 and byte_data[i + 1] == 0x00:
			return i + 2
	return len(byte_data)