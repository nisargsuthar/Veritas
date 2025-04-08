import itertools
from artifacts.prefetch.prefetch import *
from artifacts.lnk.lnk import *
from colors import *

#######################################################################################################
	# TODO: #
	#########

def loadFile(file_path, bytecount, callback):
	first = []
	second = []
	offsetdata = getOffsets(int(bytecount))
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
		hexdata, asciidata, templatedata, markerdata = prefetchTemplate(file_path)
	elif isLNK(hexdata):
		artifactsupported = True
		hexdata, asciidata, templatedata, markerdata = lnkTemplate(file_path)
	# elif isMFT(hexdata):
	# 	artifactsupported = True
	# 	hexdata, asciidata, templatedata, markerdata = mftTemplate(file_path)
	# elif isRegistry(hexdata):
	# 	artifactsupported = True
	# 	hexdata, asciidata, templatedata, markerdata = registryTemplate(file_path)
	else:
		callback(first, second, artifactsupported, file_path)

	if artifactsupported:
		markerdatasize = len(markerdata)
		asciidata = escapeMarkup(asciidata)
		savecolor = []
		# Making an infinite iterator for color_dict so in case templatedata requires more colors than present in the dictionary, it can loop through it indefinitely.
		color_cycle = itertools.cycle(color_dict.keys())

		byte_ranges = []

		# templatedata list is reversed to avoid the template offsets being changed after injection of color tags. Instead of computing new offsets and reduce performance, tag injection is done in reverse to maintain original offsets.
		for pair in reversed(templatedata):
			# Storing start and end byte locations for each markers to facilitate row highlights.
			start_byte = pair[0] - 1
			length = pair[1] + 1
			end_byte = start_byte + length
			byte_ranges.insert(0, (start_byte, end_byte))  # insert at 0 to reverse match marker order
			color = next(color_cycle)
			# Injecting the [color=XXXXXX] & [/color] Kivy tags around the template section. 
			hexdata = colorBytes(hexdata, color_dict[color], start_byte, length)
			asciidata = colorBytes(asciidata, color_dict[color], start_byte, length)
			# Save the color order for processing markerdata later.
			savecolor.append(color)
			# Remove the last section for which color tags were just injected.
			del templatedata[-1]
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
									
		hexdata = listToString(hexdata)
		asciidata = listToString(asciidata)
		markerdata = listToString(markerdata)
		
		# Following functions exist since RecycleView processes each view as a dictionary, and so the newlines break the continuity of color tags. Hence a need to inject additional tags to "fix" the color formatting done by Kivy. Below is an example of broken continuity:

		# [color=0AC92B]1E 00 00 00 [/color][color=218868]53 43 43 41 [/color][color=302B54]11 00 00 00 [/color][color=4682B4]D6 0E 00 00
		# [/color][color=228B22]4F 00 70 00 2D 00 4D 00 53 00 45 00 44 00 47 00
		# 45 00 2E 00 45 00 58 00 45 00 2D 00 42 00 35 00
		# 39 00 34 00 38 00 37 00 43 00 34 00 00 00 00 00
		# 00 00 00 00 00 00 00 00 00 00 00 00 [/color][color=01C5BB]01 00 00 00

		# Each newline can either begin from a residual end color tag from previous section or it can begin from an ongoing section for which the newline broke continuity of the color tags in which case new [color=XXXXXX] tags must be added to the beginning of the line. Since Kivy doesn't mind missing closing tags, there's no need to add [/color] at the ends before the newline character. Moreover, all [/color] tags are removed for hexdata and asciidata for clean debugging process. markerdata still requires the closing tags in order to split on them.

		# Results after fixing:
		# [color=0AC92B]1E 00 00 00 [color=218868]53 43 43 41 [color=302B54]11 00 00 00 [color=4682B4]D6 0E 00 00
		# [color=228B22]4F 00 70 00 2D 00 4D 00 53 00 45 00 44 00 47 00
		# [color=228B22]45 00 2E 00 45 00 58 00 45 00 2D 00 42 00 35 00
		# [color=228B22]39 00 34 00 38 00 37 00 43 00 34 00 00 00 00 00
		# [color=228B22]00 00 00 00 00 00 00 00 00 00 00 00 [color=01C5BB]01 00 00 00
		hexdata = fixColorTags(hexdata)
		asciidata = fixColorTags(asciidata)

		# Combine offset, hex and ascii for a single RecycleView so they share common scrolling.
		for o, h, a in zip(offsetdata, hexdata.split("\n"), asciidata.split("\n")):
			first.append(joinOffsetHexAscii(o, h, a))
		# Again leveraging Kivy not minding missing closing color tags, markerdata is split on it.
		second = [{"text": f"{line}"} for line in markerdata.split("[/color]")]
		callback(first, second, artifactsupported, file_path, byte_ranges)

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

def isLNK(hexdata):
	magic = "".join(hexdata[b] for b in range(4)).upper()
	if magic == "4C000000": # L...
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
