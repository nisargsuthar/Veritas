import binascii
from prefetch import *
from primer import *

#######################################################################################################
	# TODO: #
	#########

def load_data(file_path, callback, popup):
	hexdata = []
	asciidata = []
	markerlist = []
	templist = []
	first = []
	second = []
	bytecount = 0
	with open(file_path, 'rb') as f:
		for byte in iter(lambda: f.read(1), b''):
			bytecount += 1
			asciichar = int.from_bytes(byte, "big")
			if bytecount % 16 == 0:
				hexdata.append(binascii.hexlify(byte).decode("utf-8")+"\n")
				if asciichar >= 32 and asciichar <= 126:
					asciidata.append(chr(asciichar)+"\n")
				else:
					asciidata.append(".\n")
			else:
				hexdata.append(binascii.hexlify(byte).decode("utf-8"))
				if asciichar >= 32 and asciichar <= 126:
					asciidata.append(chr(asciichar))
				else:
					asciidata.append(".")
#######################################################################################################
	def isPrefetch():
		magic = "".join(hexdata[b] for b in range(3)).upper()
		if magic == "4D414D": # MAM
			print("Prefetch file is compressed!")
			return True
			# IMPLEMENT KIVY POPUP TO ALERT ABOUT COMPRESSION.
		else:
			magic = "".join(hexdata[b] for b in range(4, 8)).upper()
			if magic == "53434341": # SCCA
				print("Prefetch file is not compressed!")
				return True
			return False
#######################################################################################################
	def isMFT():
		magic = "".join(hexdata[b] for b in range(4)).upper()
		if magic == "42414144": # BAAD
			print("Error found in MFT entry!")
			return True
		elif magic == "46494C45": # FILE
			print("MFT file is intact!")
			return True
		return False
#######################################################################################################
	def isRegistry():
		magic = "".join(hexdata[b] for b in range(4)).upper()
		if magic == "72656766": # regf
			return True
		return False
#######################################################################################################
	isprefetch = isPrefetch()
	# ismft = isMFT()
	# isregistry = isRegistry()

	if isprefetch:
		prefetch = prefetchTemplate(file_path)
		templist = prefetch[0]
		markerdata = prefetch[1]
	# elif ismft:
	# elif isregistry:
#######################################################################################################
	if isprefetch:
		#or ismft or isregistry
		artifactsupported = True

		markerdatasize = len(markerdata)
		asciidata = escapeMarkup(asciidata)
		savecolor = []
		for color in c:
			for pair in reversed(templist):
				hexdata = colorBytes(hexdata, c[color], pair[0] - 1, pair[1] + 1)
				asciidata = colorBytes(asciidata, c[color], pair[0] - 1, pair[1] + 1)
				savecolor.append(color)
				del templist[-1]
				break
		savecolor = reversed(savecolor)
		i = 0
		for color in savecolor:
			while i < (markerdatasize-1)*3+2:
				markerdata = colorBytes(markerdata, c[color], i, 2)
				i += 3
				break
		hexdata = [s.upper()+" " if len(s) == 2 else s for s in hexdata]
	
		hexdata = listToString(hexdata)
		asciidata = listToString(asciidata)
		markerdata = listToString(markerdata)
	
		hexdata = fixHex(hexdata)
		asciidata = fixAscii(asciidata)
		# print(hexdata)
		# print(asciidata)

		def joinHexAscii(hexd, asciid):
			return {"hextext": hexd, "asciitext": asciid}
		
		for h, a in zip(hexdata.split("\n"), asciidata.split("\n")):
			first.append(joinHexAscii(h, a))
		second = [{"text": "{}".format(line)} for line in markerdata.split("\t")]
		# print(first)
		# print(second)
	else:
		artifactsupported = False

	callback(first, second, artifactsupported, popup)