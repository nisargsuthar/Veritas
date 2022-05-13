import binascii
from prefetch import *

def tempLoader():
	hexbytes = []
	with open('decomp.pf', 'rb') as f:
		for byte in iter(lambda: f.read(1), b''):
			hexbytes.append(binascii.hexlify(byte).decode("utf-8"))
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
					# Call Template Generator.
					prefetch()
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

	return True if isPrefetch() or isMFT() or isRegistry() else False