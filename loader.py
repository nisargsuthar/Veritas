from prefetch import *
from primer import *

#######################################################################################################
	# TODO: #
	#########

hexdata = []
asciidata = []
templatedata = []
markerdata = []

def loadData(file_path, callback, popup):
	first = []
	second = []
	artifactsupported = False
	
	global hexdata, asciidata, templatedata, markerdata

	if isPrefetch(file_path):
		artifactsupported = True
		callPrefetch(file_path)
	elif isMFT(file_path):
		artifactsupported = True
		callMFT(file_path)
	elif isRegistry(file_path):
		artifactsupported = True
		callRegistry(file_path)
	else:
		callback(first, second, artifactsupported, file_path, popup)

	if artifactsupported:
		markerdatasize = len(markerdata)
		asciidata = escapeMarkup(asciidata)
		savecolor = []
		for color in c:
			for pair in reversed(templatedata):
				hexdata = colorBytes(hexdata, c[color], pair[0] - 1, pair[1] + 1)
				asciidata = colorBytes(asciidata, c[color], pair[0] - 1, pair[1] + 1)
				savecolor.append(color)
				del templatedata[-1]
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
		
		# print(hexdata)
		hexdata = fixHex(hexdata)
		asciidata = fixAscii(asciidata)
		# print(hexdata)
		# print(asciidata)

		def joinHexAscii(hdata, adata):
			return {"hextext": hdata, "asciitext": adata}
									
		for h, a in zip(hexdata.split("\n"), asciidata.split("\n")):
			first.append(joinHexAscii(h, a))
		second = [{"text": "{}".format(line)} for line in markerdata.split("\t")]
		# print(first)
		# print(second)
		callback(first, second, artifactsupported, file_path, popup)

def callPrefetch(file_path):
	global hexdata, asciidata, templatedata, markerdata
	prefetch = prefetchTemplate(file_path)
	hexdata = prefetch[0]
	asciidata = prefetch[1]
	templatedata = prefetch[2]
	markerdata = prefetch[3]

def callMFT(file_path):
	global hexdata, asciidata, templatedata, markerdata

def callRegistry(file_path):
	global hexdata, asciidata, templatedata, markerdata
