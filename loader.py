from prefetch import *
from primer import *

#######################################################################################################
	# TODO: #
	#########

def loadFile(file_path, callback, popup):
	first = []
	second = []
	hexdata = []
	asciidata = []
	templatedata = []
	markerdata = []
	artifactsupported = False
	
	# Read file partially once, upto bytes which are longest for an artifact among all artifacts.
	# Update maxmagicseekamongsupportedartifacts if it is greater than current value, for the artifact you are parsing.
	maxmagicseekamongsupportedartifacts = 8
	hexdata = readPartialFile(file_path, maxmagicseekamongsupportedartifacts)

	if isPrefetch(hexdata):
		artifactsupported = True
		prefetch = prefetchTemplate(file_path)
		hexdata = prefetch[0]
		asciidata = prefetch[1]
		templatedata = prefetch[2]
		markerdata = prefetch[3]
	elif isMFT(hexdata):
		artifactsupported = True
		mft = mftTemplate(file_path)
		hexdata = mft[0]
		asciidata = mft[1]
		templatedata = mft[2]
		markerdata = mft[3]
	elif isRegistry(hexdata):
		artifactsupported = True
		registry = registryTemplate(file_path)
		hexdata = registry[0]
		asciidata = registry[1]
		templatedata = registry[2]
		markerdata = registry[3]
	else:
		callback(first, second, artifactsupported, file_path, popup)

	if artifactsupported:
		markerdatasize = len(markerdata)
		asciidata = escapeMarkup(asciidata)
		savecolor = []
		for color in color_dict:
			for pair in reversed(templatedata):
				hexdata = colorBytes(hexdata, color_dict[color], pair[0] - 1, pair[1] + 1)
				asciidata = colorBytes(asciidata, color_dict[color], pair[0] - 1, pair[1] + 1)
				savecolor.append(color)
				del templatedata[-1]
				break
		savecolor = reversed(savecolor)
		i = 0
		for color in savecolor:
			while i < (markerdatasize-1)*3+2:
				markerdata = colorBytes(markerdata, color_dict[color], i, 2)
				i += 3
				break
		hexdata = [s.upper()+" " if len(s) == 2 else s for s in hexdata]
									
		hexdata = listToString(hexdata)
		asciidata = listToString(asciidata)
		markerdata = listToString(markerdata)
		
		hexdata = fixHex(hexdata)
		asciidata = fixAscii(asciidata)

		def joinHexAscii(hdata, adata):
			return {"hextext": hdata, "asciitext": adata}
									
		for h, a in zip(hexdata.split("\n"), asciidata.split("\n")):
			first.append(joinHexAscii(h, a))
		second = [{"text": "{}".format(line)} for line in markerdata.split("\t")]
		# print(first)
		# print(second)
		callback(first, second, artifactsupported, file_path, popup)
#######################################################################################################

def isPrefetch(hexdata):
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

def isMFT(hexdata):
	magic = "".join(hexdata[b] for b in range(4)).upper()
	if magic == "42414144": # BAAD
		print("Error found in MFT entry!")
		return True
	elif magic == "46494C45": # FILE
		print("MFT file is intact!")
		return True
	return False

#######################################################################################################

def isRegistry(hexdata):
	magic = "".join(hexdata[b] for b in range(4)).upper()
	if magic == "72656766": # regf
		return True
	return False

#######################################################################################################
