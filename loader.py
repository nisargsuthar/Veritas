import binascii
from prefetch import *

#######################################################################
	# TODO: #
	#########
	# Fix the corner case for artifact not in database.

def tempLoader():
	hexdata = []
	asciidata = []
	markerlist = []
	templist = []
	bytecount = 0
	with open('kape.pf', 'rb') as f:
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
#######################################################################
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
#######################################################################
	def isMFT():
		magic = "".join(hexdata[b] for b in range(4)).upper()
		if magic == "42414144": # BAAD
			print("Error found in MFT entry!")
			return True
		elif magic == "46494C45": # FILE
			print("MFT file is intact!")
			return True
		return False
#######################################################################
	def isRegistry():
		magic = "".join(hexdata[b] for b in range(4)).upper()
		if magic == "72656766": # regf
			return True
		return False

	isprefetch = isPrefetch()
	# ismft = isMFT()
	# isregistry = isRegistry()

	if isprefetch:
		prefetch = prefetchTemplate()
		templist = prefetch[0]
		markerdata = prefetch[1]
	# elif ismft:
	# elif isregistry:
	else:
		# ~~~TEMPORARY SPAGHETTI CODE~~~
		templist = ["NOT", "FOUND"]

	return True, hexdata, asciidata, markerdata, templist if isprefetch or ismft or isregistry else False, hexdata, asciidata, markerdata, templist