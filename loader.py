from prefetch import *
from primer import *

#######################################################################################################
	# TODO: #
	#########

def load_data(file_path, callback, popup):
	file_name = getFilenameFromFilepath(file_path)
	file_extension = getFileExtensionFromFilename(file_name)
	first = []
	second = []
	hexdata = []
	asciidata = []
	templist = []
	markerdata = []
	artifactsupported = extensionmismatch = False
	supportedextensions = [".pf"]
	supportedfilenames = ["$MFT"] # For artifacts with no file extensions.

	if file_extension is None:
		# TODO: Handle automatic artifact detection.
		if file_name in supportedfilenames:
			match file_name:
				case "$MFT":
					if isMFT(file_path):
						artifactsupported = True
					else:
						extensionmismatch = True
					print("MFT")
				case _:
					artifactsupported = False
	else:
		if file_extension not in supportedextensions:
			callback(first, second, False, popup)
		else:
			match file_extension:
				case ".pf":
					if isPrefetch(file_path):
						artifactsupported = True
						prefetch = prefetchTemplate(file_path)
						hexdata = prefetch[0]
						asciidata = prefetch[1]
						templist = prefetch[2]
						markerdata = prefetch[3]
					else:
						extensionmismatch = True
				case _:
					artifactsupported = False

			#SHOW POPUP FOR EXTENSION MISMATCH

	if artifactsupported:
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

		callback(first, second, artifactsupported, popup)