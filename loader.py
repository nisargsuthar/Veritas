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
			# templatedata list is reversed to avoid the template offsets being changed after injection of color tags. Instead of computing new offsets and reduce performance, tag injection is done in reverse to maintain original offsets.
			for pair in reversed(templatedata):
				# Injecting the [color=XXXXXX] & [/color] Kivy tags around the template section. 
				hexdata = colorBytes(hexdata, color_dict[color], pair[0] - 1, pair[1] + 1)
				asciidata = colorBytes(asciidata, color_dict[color], pair[0] - 1, pair[1] + 1)
				# Save the color order for processing markerdata later.
				savecolor.append(color)
				# Remove the last section for which color tags were just injected.
				del templatedata[-1]
				# Breaking to release the control to the outer loop.
				break
		# Reversing the saved colors to sync the parity between the color dictionary and saved colors so the injection process can be repeated in reverse again for the same reason of maintaining original indices.
		savecolor = reversed(savecolor)
		i = 0
		for color in savecolor:
			# Dynamic loop logic to inject both color tags for every string starting from 0 and jumping 2 elements for closing tag which increases the index of the next string in the list by 3 (2 tags for string + 1 string itself). The limit (markerdatasize-1)*3+2 is simply the number of total increase in the size of list which would be *3 for each string and +2 is to let the while loop just survive for the last iteration.
			while i < (markerdatasize-1)*3+2:
				markerdata = colorBytes(markerdata, color_dict[color], i, 2)
				i += 3
				break
		# Making hexadecimal uppercase and adding spaces every byte representation in list if length of the representation is 2.
		# This excludes both the color tags, and byte representations with a newline appended to them.
		hexdata = [s.upper()+" " if len(s) == 2 else s for s in hexdata]
									
		hexdata = listToString(hexdata)
		asciidata = listToString(asciidata)
		markerdata = listToString(markerdata)
		
		# Following functions exist since RecycleView processes each view as a dictionary, and so the newlines break the continuity of color tags. Hence a need to inject additional tags to "fix" the color formatting done by Kivy. Below is an example of broken continuity:

		# [color=0AC92B]1E 00 00 00 [/color][color=218868]53 43 43 41 [/color][color=302B54]11 00 00 00 [/color][color=4682B4]D6 0E 00 00
		# [/color][color=228B22]4F 00 70 00 2D 00 4D 00 53 00 45 00 44 00 47 00
		# 45 00 2E 00 45 00 58 00 45 00 2D 00 42 00 35 00
		# 39 00 34 00 38 00 37 00 43 00 34 00 00 00 00 00
		# 00 00 00 00 00 00 00 00 00 00 00 00 [/color][color=01C5BB]01 00 00 00

		# Each newline can either begin from a residual end color tag from previous section in which case seek out those 8 characters, or it can begin from an ongoing section for which the newline broke continuity of the color tags in which case new [color=XXXXXX] tags must be added to the beginning of the line. Since Kivy doesn't mind missing closing tags, there's no need to add [/color] at the ends before the newline character.

		# Results after fixing:
		# [color=0AC92B]1E 00 00 00 [/color][color=218868]53 43 43 41 [/color][color=302B54]11 00 00 00 [/color][color=4682B4]D6 0E 00 00
		# [color=228B22]4F 00 70 00 2D 00 4D 00 53 00 45 00 44 00 47 00
		# [color=228B22]45 00 2E 00 45 00 58 00 45 00 2D 00 42 00 35 00
		# [color=228B22]39 00 34 00 38 00 37 00 43 00 34 00 00 00 00 00
		# [color=228B22]00 00 00 00 00 00 00 00 00 00 00 00 [/color][color=01C5BB]01 00 00 00
		hexdata = fixHex(hexdata)
		asciidata = fixAscii(asciidata)

		# Construct a dictionary for RecycleViews.
		def joinHexAscii(hdata, adata):
			return {"hextext": hdata, "asciitext": adata}

		# Combine hex and ascii for a single RecycleView so they share common scrolling.
		for h, a in zip(hexdata.split("\n"), asciidata.split("\n")):
			first.append(joinHexAscii(h, a))
		# 
		second = [{"text": "{}".format(line)} for line in markerdata.split("\t")]
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
