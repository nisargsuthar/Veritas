import binascii
from prefetch import *

######################################################################################
	# TODO: #
	#########
	# Fix the corner case for artifact not in database.

def tempLoader():
	pairlist = []
	hexbytes = []
	hexdata = ""
	asciidata = ""
	bytecount = 0	
	with open('test.txt', 'rb') as f:
		for byte in iter(lambda: f.read(1), b''):
			hexbytes.append(binascii.hexlify(byte).decode("utf-8"))
			bytecount += 1
			asciichar = int.from_bytes(byte, "big")
			hexdata += binascii.hexlify(byte).decode("utf-8")+" "
			if asciichar >= 32 and asciichar <= 126:
				asciidata += chr(asciichar)+" "
			else:
				asciidata += ". "
			if bytecount % 16 == 0:
				hexdata = hexdata[:-1]
				hexdata += "\n"
				asciidata = asciidata[:-1]
				asciidata += "\n"
######################################################################################
	def isPrefetch():
		def isCompressed():
			magic = "".join(hexbytes[b] for b in range(3)).upper()
			if magic == "4D414D": # MAM
				print("Prefetch file is compressed!")
				return True
				# IMPLEMENT KIVY POPUP TO ALERT ABOUT COMPRESSION.
			else:
				magic = "".join(hexbytes[b] for b in range(4, 8)).upper()
				if magic == "53434341": # SCCA
					print("Prefetch file is not compressed!")
					return True
				return False
		return isCompressed()
######################################################################################
	def isMFT():
		magic = "".join(hexbytes[b] for b in range(4)).upper()
		if magic == "42414144": # BAAD
			print("Error found in MFT entry!")
			return True
		elif magic == "46494C45": # FILE
			print("MFT file is intact!")
			return True
		return False
######################################################################################
	def isRegistry():
		magic = "".join(hexbytes[b] for b in range(4)).upper()
		if magic == "72656766": # regf
			return True
		return False

	if isPrefetch():
		pairlist = prefetch()
	# elif isMFT():
	# elif isRegistry():
	else:
		pairlist = ["NOT", "FOUND"]

	return True, hexdata, asciidata, pairlist if isPrefetch() or isMFT() or isRegistry() else False, hexdata, asciidata, pairlist