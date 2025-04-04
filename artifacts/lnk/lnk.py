# Author: Nisarg Suthar

from datetime import datetime, timedelta, timezone
from primer import *
from offsetter import *
from artifacts.lnk.classindicators import *
from artifacts.lnk.shellguids import *
from artifacts.lnk.netproviders import *
from artifacts.lnk.flags import *
from artifacts.lnk.hotkeys import *

#######################################################################################################
	# TODO: #
	#########
	# Confirm if class indicator categorization is correct
	# Parse extension blocks for root folder shell item
	# Look into Sort Indices for root folder shell item
	# Convert remaining seeks to offset parsing
	# Parse the GUIDS in tracker data block
	# Parse the serialized property storage structure in property store data block
#######################################################################################################

def lnkTemplate(file_path):
	lnktemplate = []
	lnksizes = []
	lnkmarkers = []

	formattedhexdata, formattedasciidata, hexdata = readFile(file_path)
	
	fileheader = [[1, 4], [5, 16], [21, 4], [25, 4], [29, 8], [37, 8], [45, 8], [53, 4], [57, 4], [61, 4], [65, 2], [67, 2], [69, 4], [73, 4]]
	fileheadersize = 76
	lnkmarkers.append("+4 The header size\n")
	lnkmarkers.append("\n+16 The LNK class identifier\nGUID: {00021401-0000-0000-c000-000000000046}\n")

	# Parsing link flags
	linkflagsbitstring = format(parseIntDword(hexdata, 20), '032b')
	linkflags = getLinkFlags(linkflagsbitstring)
	linkflagsset = "\n         ".join(name for name, value in linkflags.items() if value)
	lnkmarkers.append(f"\n+4 Link flags\n    SET: {linkflagsset}\n")

	# Parsing File Attribute Flags
	fileattributeflagsbitstring = format(parseIntDword(hexdata, 24), '032b')
	fileattributeflags = getFileAttributeFlags(fileattributeflagsbitstring)
	fileattributeflagsset = "\n         ".join(name for name, value in fileattributeflags.items() if value)
	lnkmarkers.append(f"\n+4 File attribute flags\n    SET: {fileattributeflagsset}\n")

	ctime = parseIntQword(hexdata, 28); atime = parseIntQword(hexdata, 36); mtime = parseIntQword(hexdata, 44)

	def getTimeString(time):
		epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
		timestamp = epoch + timedelta(seconds=time / 10000000)
		return timestamp if time > 0 else "Not set!"

	lnkmarkers.append(f"\n+8 Creation date and time ({getTimeString(ctime)})\n")
	lnkmarkers.append(f"\n+8 Last access date and time ({getTimeString(atime)})\n")
	lnkmarkers.append(f"\n+8 Last modification date and time ({getTimeString(mtime)})\n")

	filesize = parseIntDword(hexdata, 52)
	filesizestring = "\n+4 Least significant 32 bits of the link target file size\n" if filesize > 0xFFFFFFFF else f"\n+4 File size of the link target ({filesize} bytes)\n"

	lnkmarkers.append(filesizestring)

	iconindex = parseIntDword(hexdata, 56)
	lnkmarkers.append(f"\n+4 Icon index value ({iconindex})\n")

	showcommand = parseIntDword(hexdata, 60)
	if showcommand == 3:
		showcommandstring = "The application is open, and keyboard focus is given to the application, but its window is not shown"
	elif showcommand == 5:
		showcommandstring = "The application is open, but its window is not shown. It is not given the keyboard focus"
	else:
		showcommandstring = "The application is open and its window is open in a normal fashion"
	lnkmarkers.append(f"\n+4 Expected window state of application launched by the link\n{showcommandstring}\n")

	hotkeylowbyte = parseIntByte(hexdata, 64)
	hotkeyhighbyte = parseIntByte(hexdata, 65)
	hotkeylowstring = lowbyte[hotkeylowbyte] if hotkeylowbyte else ""
	hotkeyhighstring = " + ".join(highbyte[key] for key in highkeyorder if hotkeyhighbyte & key) if hotkeyhighbyte else ""
	hotkey = " + ".join(filter(None, [hotkeyhighstring, hotkeylowstring]))
	if not hotkey:
		hotkey =  "Not assigned!"
	lnkmarkers.append(f"\n+2 Hot key ({hotkey})\n")

	lnkmarkers.append("\n+2 Unknown (Reserved)\n")
	lnkmarkers.append("\n+4 Unknown (Reserved)\n")
	lnkmarkers.append("\n+4 Unknown (Reserved)\n")

	lnktemplate.append(fileheader)
	lnksizes.append(fileheadersize)

	linktargetidlistsize = 0
	if linkflags['HasLinkTargetIDList']:
		linktargetidlist = [[1, 2]]
		linktargetidlistsize = 2

		parsedlinktargetidlistsize = parseIntWord(hexdata, fileheadersize)
		lnkmarkers.append(f"+2 Link Target ID List Size ({parsedlinktargetidlistsize} bytes)")

		temp = parsedlinktargetidlistsize
		itemidsizelist = []
		classtypeindicatorlist = []
		pointerlist = []
		pointer = fileheadersize + 2
		while temp > 0:
			itemidsize = parseIntWord(hexdata, pointer)
			classtypeindicator = "".join(hexdata[b] for b in range(pointer + 2, pointer + 2 + 1))
			if itemidsize == 0:
				break
			itemidsizelist.append(itemidsize)
			classtypeindicatorlist.append(classtypeindicator)
			pointerlist.append(pointer)
			pointer += itemidsize
			temp -= itemidsize

		start = sum(linktargetidlist[-1])
		for index, size in enumerate(itemidsizelist):
			linktargetidlist.append([start, size])
			linktargetidlistsize += size
			str1 = f"\n    +{size} {classindicatormappings[classtypeindicatorlist[index]]} Shell Item\n"
			str2 = f"        >2 Item ID Size (including this field)\n"
			str3 = f"        >1 Class Type Indicator\n"
			shellitemstrings = str1+str2+str3

			match classindicatormappings[classtypeindicatorlist[index]]:
				case "Root Folder":
					str4 = f"        >1 Sort Index\n"
					guidpointer = pointerlist[index] + 4
					guidstring = guidstringfromhex("".join(hexdata[b] for b in range(guidpointer, guidpointer + 16)))
					result = shellguids.get(guidstring.lower(), "Unknown GUID")
					str5 = f"        >16 Shell Folder GUID: {guidstring}\n                               {result}"
					print("GUID string from root folder shell item: ", guidstring)
					shellitemstrings += str4 + str5

					# TODO: If shell item size > 20
					# if size > 20:
				case "Volume":
					str4 = f""
				case "File Entry":
					str4 = f""
				case "Network Location":
					str4 = f""
				case "URI":
					str4 = f""

			lnkmarkers.append(shellitemstrings) # Append concatenation here
			start += size
		linktargetidlist.append([start, 2]) # TerminalID
		linktargetidlistsize += 2

		lnkmarkers.append(f"    +2 TerminalID")
		lnktemplate.append(linktargetidlist)
		lnksizes.append(linktargetidlistsize)

	linkinfosize = 0
	if linkflags['HasLinkInfo']:
		linkinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4]]
		linkinfosize = 28	

		seek = linkinfooffset = fileheadersize + linktargetidlistsize
		parsedlinkinfosize = parseIntDword(hexdata, seek)
		parsedlinkinfoheadersize = parseIntDword(hexdata, seek + 4)

		lnkmarkers.append(f"\n+4 LinkInfoSize including these 4 bytes ({parsedlinkinfosize} bytes)\n")
		lnkmarkers.append(f"\n    +4 Link Info Header Size ({parsedlinkinfoheadersize})\n")

		linkinfoflags = format(parseIntDword(hexdata, seek + 8), 'b').zfill(32)
		VolumeIDAndLocalBasePath = int(linkinfoflags[31]); CommonNetworkRelativeLinkAndPathSuffix = int(linkinfoflags[30])
		linkinfoflag_vars = {"VolumeIDAndLocalBasePath": VolumeIDAndLocalBasePath,	"CommonNetworkRelativeLinkAndPathSuffix": CommonNetworkRelativeLinkAndPathSuffix}
		linkinfoflagsset = "\n             ".join(name for name, value in linkinfoflag_vars.items() if value == 1)
		lnkmarkers.append(f"\n    +4 Link Info flags\n        SET: {linkinfoflagsset}\n")
		
		volumeinformationoffset = linkinfooffset + parseIntDword(hexdata, seek + 12)
		localbasepathoffset = linkinfooffset + parseIntDword(hexdata, seek + 16)
		if VolumeIDAndLocalBasePath:
			lnkmarkers.append(f"\n    +4 Offset to the volume information\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(volumeinformationoffset)}\n")
			lnkmarkers.append(f"\n    +4 Offset to the local base path\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(localbasepathoffset)}\n")
		else:
			lnkmarkers.append("\n    +4 Offset to the volume information\n       0x00000000 as the flag VolumeIDAndLocalBasePath is not set\n")
			lnkmarkers.append("\n    +4 Offset to the local base path\n       0x00000000 as the flag VolumeIDAndLocalBasePath is not set\n")

		seek = fileheadersize + linktargetidlistsize
		commonnetworkrelativelinkoffset = linkinfooffset + parseIntDword(hexdata, seek + 20)
		if CommonNetworkRelativeLinkAndPathSuffix:
			lnkmarkers.append(f"\n    +4 Offset to the common network relative link\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(commonnetworkrelativelinkoffset)}\n")
		else:
			lnkmarkers.append("\n    +4 Offset to the common network relative link\n       0x00000000 as the flag CommonNetworkRelativeLinkAndPathSuffix is not set\n")

		commonpathsuffixoffset = linkinfooffset + parseIntDword(hexdata, seek + 24)
		lnkmarkers.append(f"\n    +4 Offset to the common path suffix\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(commonpathsuffixoffset)}\n")

		# ------------------------------------------------------------------------------------------------------
		# Parsing FIELDS LocalBasePathOffsetUnicode and CommonPathSuffixOffsetUnicode
		if parsedlinkinfoheadersize >= 36:
			linkinfo.append([sum(linkinfo[-1]), 4]); linkinfosize += 4
			localbasepathunicodeoffset = linkinfooffset + parseIntDword(hexdata, seek + 28)
			if VolumeIDAndLocalBasePath:
				lnkmarkers.append(f"\n    +4 Offset to the local base path in unicode\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(localbasepathunicodeoffset)}\n")
			else:
				lnkmarkers.append("    +4 Offset to the local base path in unicode\n       0x00000000 as the flag VolumeIDAndLocalBasePath is not set\n")

			linkinfo.append([sum(linkinfo[-1]), 4]); linkinfosize += 4
			commonpathsuffixunicodeoffset = linkinfooffset + parseIntDword(hexdata, seek + 32)
			lnkmarkers.append(f"\n    +4 Offset to the common path suffix in unicode\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(commonpathsuffixunicodeoffset)}\n")

		# Parsing STRUCT VolumeID and FIELD LocalBasePath
		if VolumeIDAndLocalBasePath:
			# VolumeID Data Structure
			seek = fileheadersize + linktargetidlistsize + linkinfosize
			for _ in range(4):
				linkinfo.append([sum(linkinfo[-1]), 4]); linkinfosize += 4

			parsedvolumeidsize = parseIntDword(hexdata, seek)
			lnkmarkers.append(f"\n    +4 VolumeIDSize (> 16) including these 4 bytes: {parsedvolumeidsize}\n")

			drivetype = parseIntDword(hexdata, seek + 4)
			drivetypestring = ""
			if drivetype == 0:
				drivetypestring = "The drive type cannot be determined."
			elif drivetype == 1:
				drivetypestring = "The root path is invalid; for example, there is no volume mounted at the path."
			elif drivetype == 2:
				drivetypestring = "The drive has removable media, such as a floppy drive, thumb drive, or flash card reader."
			elif drivetype == 3:
				drivetypestring = "The drive has fixed media, such as a hard drive or flash drive."
			elif drivetype == 4:
				drivetypestring = "The drive is a remote (network) drive."
			elif drivetype == 5:
				drivetypestring = "The drive is a CD-ROM drive."
			elif drivetype == 6:
				drivetypestring = "The drive is a RAM disk."
			lnkmarkers.append(f"\n        +4 Drive type:\n        {drivetypestring}")

			driveserialnumber = swapEndianness("".join(hexdata[b] for b in range(seek + 8, seek + 12)))
			lnkmarkers.append("\n        +4 Drive serial number\n")

			volumelabeloffset = swapEndianness("".join(hexdata[b] for b in range(seek + 12, seek +16)))
			lnkmarkers.append("\n        +4 Offset to the volume label\n")
			if volumelabeloffset == "00000014":
				linkinfo.append([sum(linkinfo[-1]), 4]); linkinfosize += 4
				lnkmarkers.append("\n        +4 Offset to the volume label in unicode (Ignore previous offset)\n")

			# bigseek = seek + parsedvolumeidsize
			# lilseek = fileheadersize + linktargetidlistsize + linkinfosize
			# volumelabelsize = bigseek - lilseek
			# if volumelabelsize > 0:
			# 	linkinfo.append([sum(linkinfo[-1]), volumelabelsize]); linkinfosize += volumelabelsize
			# 	lnkmarkers.append(f"\n        +{volumelabelsize} Volume label of the drive (null-terminated)\n")

			seek = fileheadersize + linktargetidlistsize + linkinfosize
			volumelabelsize = getNullTerminatedStringSize("".join(hexdata[seek:]))
			if volumelabelsize > 0:
				linkinfo.append([sum(linkinfo[-1]), volumelabelsize]); linkinfosize += volumelabelsize
				lnkmarkers.append(f"\n        +{volumelabelsize} Volume label of the drive (null-terminated)\n")

			# LocalBasePath
			localbasepathsize = getNullTerminatedStringSize("".join(hexdata[seek + volumelabelsize:]))
			# localbasepath = "".join(hexdata[b] for b in range(seek + volumelabelsize, seek + volumelabelsize + localbasepathsize))
			linkinfo.append([sum(linkinfo[-1]), localbasepathsize]); linkinfosize += localbasepathsize
			lnkmarkers.append(f"\n    +{localbasepathsize} Local base path (null-terminated)\n")

		# Parsing STRUCT CommonNetworkRelativeLink 
		if CommonNetworkRelativeLinkAndPathSuffix:
			seek = fileheadersize + linktargetidlistsize + linkinfosize
			sizeofunknown = commonnetworkrelativelinkoffset - seek
			if sizeofunknown > 0:
				linkinfo.append([sum(linkinfo[-1]), sizeofunknown]); linkinfosize += sizeofunknown
				lnkmarkers.append(f"\n+{sizeofunknown} !!!UNKNOWN FIELD TO BE DEBUGGED!!!\n")
			
			
			for _ in range(5):
				linkinfo.append([sum(linkinfo[-1]), 4]); linkinfosize += 4

			parsedcommonnetworkrelativelinksize = parseIntDword(hexdata, commonnetworkrelativelinkoffset)
			lnkmarkers.append(f"\n    +4 CommonNetworkRelativeLinkSize (>= 20): {parsedcommonnetworkrelativelinksize}\n")
			
			commonnetworkrelativelinkflagsbitstring = format(parseIntDword(hexdata, commonnetworkrelativelinkoffset + 4), '032b')
			commonnetworkrelativelinkflags = getCommonNetworkRelativeLinkFlags(commonnetworkrelativelinkflagsbitstring)
			commonnetworkrelativelinkflagsset = "\n         ".join(name for name, value in commonnetworkrelativelinkflags.items() if value == 1)
			lnkmarkers.append(f"\n        +4 CommonNetworkRelativeLinkFlags\n            SET: {commonnetworkrelativelinkflagsset}\n")

			netnameoffset = parseIntDword(hexdata, commonnetworkrelativelinkoffset + 8)
			lnkmarkers.append("\n        +4 Offset to the net name\n           Relative to the CommonNetworkRelativeLink struct\n")
			
			if commonnetworkrelativelinkflags['ValidDevice']:
				lnkmarkers.append("\n        +4 Offset to the device name\n           Relative to the CommonNetworkRelativeLink struct")
			else:
				lnkmarkers.append("\n        +4 Offset to the device name\n           0x00000000 as the flag ValidDevice is not set\n")

			if commonnetworkrelativelinkflags['ValidNetType']:
				networkprovidertype = parseIntDword(hexdata, commonnetworkrelativelinkoffset + 16)
				lnkmarkers.append(f"\n        +4 Network provider type ({getNetVendor(networkprovidertype)})\n")
			else:
				lnkmarkers.append("\n        +4 Network provider type\n           Ignore as the flag ValidNetType is not set")

			print("NETNAMEOFFSET: ", netnameoffset)
			if netnameoffset > 20:
				linkinfo.append([sum(linkinfo[-1]), 4]); linkinfosize += 4
				lnkmarkers.append("\n        +4 Offset to the net name in unicode\n           Relative to the CommonNetworkRelativeLink struct")

				linkinfo.append([sum(linkinfo[-1]), 4]); linkinfosize += 4
				if commonnetworkrelativelinkflags['ValidDevice']:
					lnkmarkers.append("\n        +4 Offset to the device name in unicode\n           Relative to the CommonNetworkRelativeLink struct")
				else:
					lnkmarkers.append("\n        +4 Offset to the device name in unicode\n           0x00000000 as the flag ValidDevice is not set\n")
				

			seek = fileheadersize + linktargetidlistsize + linkinfosize
			netnamesize = getNullTerminatedStringSize("".join(hexdata[seek:]))
			linkinfo.append([sum(linkinfo[-1]), netnamesize]); linkinfosize += netnamesize
			lnkmarkers.append(f"\n        +{netnamesize} Net name (null-terminated)\n")

			if commonnetworkrelativelinkflags['ValidDevice']: ##########################
				devicenamesize = getNullTerminatedStringSize("".join(hexdata[seek + netnamesize:]))
				linkinfo.append([sum(linkinfo[-1]), devicenamesize]); linkinfosize += devicenamesize
				lnkmarkers.append(f"\n        +{devicenamesize} Device name (null-terminated)\n")

			if netnameoffset > 20:
				seek = fileheadersize + linktargetidlistsize + linkinfosize
				netnameunicodesize = getNullTerminatedUnicodeStringSize("".join(hexdata[seek:]))
				linkinfo.append([sum(linkinfo[-1]), netnameunicodesize]); linkinfosize += netnameunicodesize
				lnkmarkers.append(f"\n        +{netnameunicodesize} Net name in unicode (null-terminated)\n")

				if commonnetworkrelativelinkflags['ValidDevice']: ##########################
					seek = fileheadersize + linktargetidlistsize + linkinfosize
					devicenameunicodesize = getNullTerminatedUnicodeStringSize("".join(hexdata[seek:]))
					linkinfo.append([sum(linkinfo[-1]), devicenameunicodesize]); linkinfosize += devicenameunicodesize
					lnkmarkers.append(f"\n        +{devicenameunicodesize} Device name in unicode (null-terminated)\n")
			
		# Parsing FIELD CommonPathSuffix
		seek = fileheadersize + linktargetidlistsize + linkinfosize
		commonpathsuffixsize = getNullTerminatedStringSize("".join(hexdata[seek:]))
		# commonpathsuffix = "".join(hexdata[b] for b in range(seek, seek + commonpathsuffixsize))
		linkinfo.append([sum(linkinfo[-1]), commonpathsuffixsize]); linkinfosize += commonpathsuffixsize
		lnkmarkers.append(f"\n    +{commonpathsuffixsize} Common path suffix (null-terminated)\n")
		# print(f"FULL TARGET PATH: {localbasepath+commonpathsuffix}")

		# Parsing FIELDS LocalBasePathUnicode and CommonPathSuffixUnicode
		if parsedlinkinfoheadersize >= 36:
			# LocalBasePathUnicode
			if VolumeIDAndLocalBasePath:
				localbasepathunicodesize = getNullTerminatedUnicodeStringSize("".join(hexdata[seek+commonpathsuffixsize:]))
				linkinfo.append([sum(linkinfo[-1]), localbasepathunicodesize]); linkinfosize += localbasepathunicodesize
				lnkmarkers.append(f"\n    +{localbasepathunicodesize} Local base path in unicode\n")

			# CommonPathSuffixUnicode
			seek = fileheadersize + linktargetidlistsize + linkinfosize
			commonpathsuffixunicodesize = getNullTerminatedUnicodeStringSize("".join(hexdata[commonpathsuffixunicodeoffset:]))
			unknownsize = commonpathsuffixunicodeoffset - seek

			if unknownsize > 0:
				linkinfo.append([sum(linkinfo[-1]), unknownsize]); linkinfosize += unknownsize
				lnkmarkers.append(f"+{unknownsize} !!!UNKNOWN FIELD TO BE DEBUGGED!!!")
			
			linkinfo.append([sum(linkinfo[-1]), commonpathsuffixunicodesize]); linkinfosize += commonpathsuffixunicodesize
			lnkmarkers.append(f"\n    +{commonpathsuffixunicodesize} Common path suffix in unicode\n")

		lnktemplate.append(linkinfo)
		lnksizes.append(linkinfosize)
	
	# Parsing STRUCT StringData
	def parseStringData(hexdata, seek, IsUnicode, stringdata, stringdatasize, lnkmarkers, description):
		charcount = parseIntWord(hexdata, seek)
		datasize = charcount * 2 if IsUnicode else charcount
		stringdata.append([1, 2 + datasize] if not stringdata else [sum(stringdata[-1]), 2 + datasize])
		stringdatasize += 2 + datasize
		lnkmarkers.append(f"\n+{2 + datasize} {description} (First 2 bytes is character count)\n")
		seek += 2 + datasize
		return seek, stringdata, stringdatasize

	stringdatasize = 0
	stringdata = []
	seek = fileheadersize + linktargetidlistsize + linkinfosize

	if linkflags['HasName']:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, linkflags['IsUnicode'], stringdata, stringdatasize, lnkmarkers, "Shortcut description")
	if linkflags['HasRelativePath']:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, linkflags['IsUnicode'], stringdata, stringdatasize, lnkmarkers, "Relative path of target w.r.t. this LNK file")
	if linkflags['HasWorkingDir']:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, linkflags['IsUnicode'], stringdata, stringdatasize, lnkmarkers, "Working directory to be used when activating the link target")
	if linkflags['HasArguments']:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, linkflags['IsUnicode'], stringdata, stringdatasize, lnkmarkers, "Command line arguments at the time of activating the link target")
	if linkflags['HasIconLocation']:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, linkflags['IsUnicode'], stringdata, stringdatasize, lnkmarkers, "Icon location")

	lnktemplate.append(stringdata)
	lnksizes.append(stringdatasize)

	# Parsing ExtraData
	seek = fileheadersize + linktargetidlistsize + linkinfosize + stringdatasize

	def getDataBlockSignature(seek, hexdata):
		if seek + 8 > len(hexdata):
			return None
		sig = swapEndianness("".join(hexdata[b] for b in range(seek + 4 , seek + 8)))
		return sig.upper()
	
	while seek < len(hexdata):
		if getDataBlockSignature(seek, hexdata) == "A0000002":
			print("DATA BLOCK PRESENT: CONSOLE")
			# TODO: Parse specific fields
			consoledatablock = [[1, 4], [5, 4], [9, 2], [11, 2], [13, 2], [15, 2], [17, 2], [19, 2], [21, 2], [23, 2], [25, 4], [29, 4], [33, 4], [37, 4], [41, 4], [45, 64], [109, 4], [113, 4], [117, 4], [121, 4], [125, 4], [129, 4], [133, 4], [137, 4], [141, 64]]
			consoledatablocksize = 204

			lnkmarkers.append("\n+4 Console Data Block size including these 4 bytes (Must be 0x000000CC)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA0000002)")
			lnkmarkers.append("    +2 Fill attributes") # TODO: Parse attributes
			lnkmarkers.append("    +2 Popup fill attributes") # TODO: Parse attributes

			# TODO: Parse all sizes
			lnkmarkers.append("    +2 Horizontal size of the console window buffer (in characters)")
			lnkmarkers.append("    +2 Vertical size of the console window buffer (in characters)")
			lnkmarkers.append("    +2 Horizontal window size of the console window (in characters)")
			lnkmarkers.append("    +2 Vertical window size of the console window (in characters)")
			lnkmarkers.append("    +2 Horizontal coordinate of the console window origin (in pixels)")
			lnkmarkers.append("    +2 Vertical coordinate of the console window origin (in pixels)")

			lnkmarkers.append("    +4 Unused1 (A value that is undefined and MUST be ignored.)")
			lnkmarkers.append("    +4 Unused2 (A value that is undefined and MUST be ignored.)")
			lnkmarkers.append("    +4 Size of font used in the console window") # TODO: Parse the 2 words
			lnkmarkers.append("    +4 Family of font used in the console window") # TODO: Parse font families
			lnkmarkers.append("    +4 Stroke weight of font used in the console window") # TODO: Parse value
			lnkmarkers.append("    +64 Face name of font used in the console window in unicode")
			lnkmarkers.append("    +4 Size of cursor used in the console window (in pixels)")
			lnkmarkers.append("    +4 Full-screen mode status") # TODO: Parse value
			lnkmarkers.append("    +4 QuickEdit mode status (In QuickEdit mode, the mouse can be used to cut, copy, and paste text in the console window.)") # TODO: Parse value
			lnkmarkers.append("    +4 Insert mode status") # TODO: Parse value
			lnkmarkers.append("    +4 Auto-position mode status") # TODO: Parse value
			lnkmarkers.append("    +4 Size of the buffer used to store history of the user input in the console window (in characters)")
			lnkmarkers.append("    +4 Number of history buffers to use")
			lnkmarkers.append("    +4 Grant status of duplicates in history") # TODO: Parse value
			lnkmarkers.append("    +64 RGB colors used for text in the console window\n") # TODO: Parse value

			lnktemplate.append(consoledatablock)
			lnksizes.append(consoledatablocksize)
			seek += consoledatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000004":
			print("DATA BLOCK PRESENT: CONSOLEFE")
			consolefedatablock = [[1, 4], [5, 4], [9, 4]]
			consolefedatablocksize = 12

			lnkmarkers.append("\n+4 Console FE Data Block size including these 4 bytes (Must be 0x0000000C)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA0000004)")
			lnkmarkers.append("    +4 Code page language code identifier\n") # TODO: see [MS-LCID]

			lnktemplate.append(consolefedatablock)
			lnksizes.append(consolefedatablocksize)
			seek += consolefedatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000006":
			print("DATA BLOCK PRESENT: DARWIN")
			darwindatablock = [[1, 4], [5, 4], [9, 260], [269, 520]]
			darwindatablocksize = 788
			
			lnkmarkers.append("\n+4 Darwin Data Block size including these 4 bytes (Must be 0x00000314)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA0000006)")
			lnkmarkers.append("    +260 MSI application identifier (Should be ignored) (null-terminated)")
			lnkmarkers.append("    +520 MSI application identifier in unicode (null-terminated)\n")

			lnktemplate.append(darwindatablock)
			lnksizes.append(darwindatablocksize)
			seek += darwindatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000001":
			print("DATA BLOCK PRESENT: ENVIRONMENT VARIABLE")
			environmentvariabledatablock = [[1, 4], [5, 4], [9, 260], [269, 520]]
			environmentvariabledatablocksize = 788
			
			lnkmarkers.append("\n+4 Environment Variable Data Block size including these 4 bytes (Must be 0x00000314)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA0000001)")
			lnkmarkers.append("    +260 Path to environment variable information (null-terminated)")
			lnkmarkers.append("    +520 Path to environment variable information in unicode (null-terminated)\n")

			lnktemplate.append(environmentvariabledatablock)
			lnksizes.append(environmentvariabledatablocksize)
			seek += environmentvariabledatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000007":
			print("DATA BLOCK PRESENT: ICON ENVIRONMENT")
			iconenvironmentdatablock = [[1, 4], [5, 4], [9, 260], [269, 520]]
			iconenvironmentdatablocksize = 788
			
			lnkmarkers.append("\n+4 Icon Environment Data Block size including these 4 bytes (Must be 0x00000314)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA0000007)")
			lnkmarkers.append("    +260 Path constructed with environment variables (null-terminated)")
			lnkmarkers.append("    +520 Path constructed with environment variables in unicode (null-terminated)\n")

			lnktemplate.append(iconenvironmentdatablock)
			lnksizes.append(iconenvironmentdatablocksize)
			seek += iconenvironmentdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A000000B":
			print("DATA BLOCK PRESENT: KNOWN FOLDER")
			# not DisableKnownFolderTracking
			knownfolderdatablock = [[1, 4], [5, 4], [9, 16], [25, 4]]
			knownfolderdatablocksize = 28

			lnkmarkers.append("\n+4 Known Folder Data Block size including these 4 bytes (Must be 0x0000001C)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA000000B)")
			lnkmarkers.append("    +16 Folder GUID")
			lnkmarkers.append("    +4 Offset to the ItemID of the first child segment of the above IDList\n")

			lnktemplate.append(knownfolderdatablock)
			lnksizes.append(knownfolderdatablocksize)
			seek += knownfolderdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000009":
			print("DATA BLOCK PRESENT: PROPERTY STORE")
			# TODO: Parse Serialized Property Storage Struct from [MS-PROPSTORE]
			propertystoredatablock = [[1, 4], [5, 4]]
			propertystoredatablocksize = parseIntDword(hexdata, seek)
			propertystoredatablock.append([sum(propertystoredatablock[-1]), propertystoredatablocksize - 8])

			lnkmarkers.append("\n+4 Property Store Data Block size including these 4 bytes (Must be >= 0x0000000C)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA0000009)")
			lnkmarkers.append(f"    +{propertystoredatablocksize-8} Serialized property storage structure\n")
			
			lnktemplate.append(propertystoredatablock)
			lnksizes.append(propertystoredatablocksize)
			seek += propertystoredatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000008":
			print("DATA BLOCK PRESENT: SHIM")
			shimdatablock = [[1, 4], [5, 4]]
			shimdatablocksize = parseIntDword(hexdata, seek)

			lnkmarkers.append("\n+4 Shim Data Block size including these 4 bytes (Must be >= 0x00000088)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA0000008)")

			# layernamesize = getNullTerminatedUnicodeStringSize("".join(hexdata[seek + 8:]))
			shimdatablock.append([sum(shimdatablock[-1]), shimdatablocksize - 8])
			lnkmarkers.append(f"    +{shimdatablocksize-8} Shim layer name to apply to a link target when activated in unicode (null-terminated)\n")

			lnktemplate.append(shimdatablock)
			lnksizes.append(shimdatablocksize)
			seek += shimdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000005":
			print("DATA BLOCK PRESENT: SPECIAL FOLDER")
			specialfolderdatablock = [[1, 4], [5, 4], [9, 4], [13, 4]]
			specialfolderdatablocksize = 16

			lnkmarkers.append("\n+4 Special Folder Data Block size including these 4 bytes (Must be 0x00000010)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA0000005)")
			lnkmarkers.append("    +4 Folder integer ID")
			lnkmarkers.append("    +4 Offset to the ItemID of the first child segment of the above IDList\nRelative to the LinkTargetIDList struct\n")

			lnktemplate.append(specialfolderdatablock)
			lnksizes.append(specialfolderdatablocksize)
			seek += specialfolderdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000003":
			print("DATA BLOCK PRESENT: TRACKER")
			trackerdatablock = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 16], [33, 16], [49, 16], [65, 16], [81, 16]]
			trackerdatablocksize = 96

			lnkmarkers.append("\n+4 Tracker Data Block size including these 4 bytes (Must be 0x00000060)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA0000003)")
			lnkmarkers.append("    +4 Size of rest of Tracker Data Block, including these 4 bytes (Must be 0x00000058)")
			lnkmarkers.append("    +4 Version (Must be 0x00000000)")
			lnkmarkers.append("    +16 NetBIOS name of the machine where the link target was last known to reside (null-terminated with unused bytes set to 0)")
			lnkmarkers.append("    +16 Droid volume identifier (GUID containing an NTFS object identifier)")
			lnkmarkers.append("    +16 Droid file identifier (GUID containing an NTFS object identifier)")
			lnkmarkers.append("    +16 Birth droid volume identifier (GUID containing an NTFS object identifier)")
			lnkmarkers.append("    +16 Birth droid file identifier (GUID containing an NTFS object identifier)\n")

			lnktemplate.append(trackerdatablock)
			lnksizes.append(trackerdatablocksize)
			seek += trackerdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A000000C":
			parsedlastdatablocksize = parseIntDword(hexdata, seek)
			print("DATA BLOCK PRESENT: VISTA")
			vistaandaboveidlistdatablock = [[1, 4], [5, 4]]
			vistaandaboveidlistdatablocksize = 8

			idlistsize = parsedlastdatablocksize - vistaandaboveidlistdatablocksize

			lnkmarkers.append("\n+4 Vista And Above ID List Data Block size including these 4 bytes (Must be >= 0x0000000A)")
			lnkmarkers.append("    +4 Block signature (Must be 0xA000000C)")
			lnkmarkers.append(f"    +{idlistsize} IDList\n") # TODO: Parse ItemIDList

			vistaandaboveidlistdatablock.append([sum(vistaandaboveidlistdatablock[-1]), idlistsize])
			vistaandaboveidlistdatablocksize += idlistsize
			lnktemplate.append(vistaandaboveidlistdatablock)
			lnksizes.append(parsedlastdatablocksize)
			seek += vistaandaboveidlistdatablocksize

		# Check for terminal block
		if swapEndianness("".join(hexdata[b] for b in range(seek , seek + 4))) == "00000000":
			print("DATA BLOCK PRESENT: TERMINAL")
			terminalblock = [[1, 4]]
			lnkmarkers.append("\n+4 Terminal block (0x00000000)\n")
			lnktemplate.append(terminalblock)
			lnksizes.append(4)
			# seek += 4
			break

# ----------------------------------------------------------------------------------------------------------------
	templatedata = toAbsolute(lnktemplate, lnksizes)

	return formattedhexdata, formattedasciidata, templatedata, lnkmarkers