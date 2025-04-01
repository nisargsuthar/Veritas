# Author: Nisarg Suthar

import binascii
from primer import *
from offsetter import *
from artifacts.lnk.classindicators import *
from artifacts.lnk.shellguids import *
from artifacts.lnk.netproviders import *

#######################################################################################################
	# TODO: #
	#########
	# Replace see sections in markers
	# Confirm if class indicator categorization is correct
	# Parse extension blocks for root folder shell item
	# Look into Sort Indices for root folder shell item
	# Replace start lines to shorten it
	# Convert seeks to offset parsing
	# Parse the GUIDS in extra data blocks
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

	# Parsing data flags
	linkflags = format(int(swapEndianness("".join(hexdata[b] for b in range(20 , 24))), 16), 'b').zfill(32)
	HasLinkTargetIDList = int(linkflags[31]); HasLinkInfo = int(linkflags[30]); HasName = int(linkflags[29]); HasRelativePath = int(linkflags[28]); HasWorkingDir = int(linkflags[27]); HasArguments = int(linkflags[26]); HasIconLocation = int(linkflags[25]); IsUnicode = int(linkflags[24]); ForceNoLinkInfo = int(linkflags[23]); HasExpString = int(linkflags[22]); RunInSeparateProcess = int(linkflags[21]); Unused1 = int(linkflags[20]); HasDarwinID = int(linkflags[19]); RunAsUser = int(linkflags[18]); HasExpIcon = int(linkflags[17]); NoPidlAlias = int(linkflags[16]); Unused2 = int(linkflags[15]); RunWithShimLayer = int(linkflags[14])	; ForceNoLinkTrack = int(linkflags[13]); EnableTargetMetadata = int(linkflags[12]); DisableLinkPathTracking = int(linkflags[11]); DisableKnownFolderTracking = int(linkflags[10]); DisableKnownFolderAlias = int(linkflags[9]); AllowLinkToLink = int(linkflags[8]); UnaliasOnSave = int(linkflags[7]); PreferEnvironmentPath = int(linkflags[6]); KeepLocalIDListForUNCTarget = int(linkflags[5])

	linkflag_vars = {"HasLinkTargetIDList": HasLinkTargetIDList,	"HasLinkInfo": HasLinkInfo,	"HasName": HasName,	"HasRelativePath": HasRelativePath,	"HasWorkingDir": HasWorkingDir,	"HasArguments": HasArguments,	"HasIconLocation": HasIconLocation,	"IsUnicode": IsUnicode,	"ForceNoLinkInfo": ForceNoLinkInfo,	"HasExpString": HasExpString,	"RunInSeparateProcess": RunInSeparateProcess,	"Unused1": Unused1,	"HasDarwinID": HasDarwinID,	"RunAsUser": RunAsUser,	"HasExpIcon": HasExpIcon,	"NoPidlAlias": NoPidlAlias,	"Unused2": Unused2,	"RunWithShimLayer": RunWithShimLayer,	"ForceNoLinkTrack": ForceNoLinkTrack,	"EnableTargetMetadata": EnableTargetMetadata,	"DisableLinkPathTracking": DisableLinkPathTracking,	"DisableKnownFolderTracking": DisableKnownFolderTracking,	"DisableKnownFolderAlias": DisableKnownFolderAlias,	"AllowLinkToLink": AllowLinkToLink,	"UnaliasOnSave": UnaliasOnSave,	"PreferEnvironmentPath": PreferEnvironmentPath,	"KeepLocalIDListForUNCTarget": KeepLocalIDListForUNCTarget}
	linkflagsset = "\n         ".join(name for name, value in linkflag_vars.items() if value == 1)
	lnkmarkers.append(f"\n+4 Link flags\n    SET: {linkflagsset}\n")

	# Parsing File Attribute Flags
	fileattributeflags = format(int(swapEndianness("".join(hexdata[b] for b in range(24 , 28))), 16), 'b').zfill(32)
	FILE_ATTRIBUTE_READONLY = int(fileattributeflags[31]); FILE_ATTRIBUTE_HIDDEN = int(fileattributeflags[30]); FILE_ATTRIBUTE_SYSTEM = int(fileattributeflags[29]); Reserved1 = int(fileattributeflags[28]); FILE_ATTRIBUTE_DIRECTORY = int(fileattributeflags[27]); FILE_ATTRIBUTE_ARCHIVE = int(fileattributeflags[26]); Reserved2 = int(fileattributeflags[25]); FILE_ATTRIBUTE_NORMAL = int(fileattributeflags[24]); FILE_ATTRIBUTE_TEMPORARY = int(fileattributeflags[23]); FILE_ATTRIBUTE_SPARSE_FILE = int(fileattributeflags[22]); FILE_ATTRIBUTE_REPARSE_POINT = int(fileattributeflags[21]); FILE_ATTRIBUTE_COMPRESSED = int(fileattributeflags[20]); FILE_ATTRIBUTE_OFFLINE = int(fileattributeflags[19]); FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = int(fileattributeflags[18]); FILE_ATTRIBUTE_ENCRYTED = int(fileattributeflags[17])

	fileattributeflag_vars = {"FILE_ATTRIBUTE_READONLY": FILE_ATTRIBUTE_READONLY, "FILE_ATTRIBUTE_HIDDEN": FILE_ATTRIBUTE_HIDDEN, "FILE_ATTRIBUTE_SYSTEM": FILE_ATTRIBUTE_SYSTEM, "Reserved1": Reserved1, "FILE_ATTRIBUTE_DIRECTORY": FILE_ATTRIBUTE_DIRECTORY, "FILE_ATTRIBUTE_ARCHIVE": FILE_ATTRIBUTE_ARCHIVE, "Reserved2": Reserved2, "FILE_ATTRIBUTE_NORMAL": FILE_ATTRIBUTE_NORMAL, "FILE_ATTRIBUTE_TEMPORARY": FILE_ATTRIBUTE_TEMPORARY, "FILE_ATTRIBUTE_SPARSE_FILE": FILE_ATTRIBUTE_SPARSE_FILE, "FILE_ATTRIBUTE_REPARSE_POINT": FILE_ATTRIBUTE_REPARSE_POINT, "FILE_ATTRIBUTE_COMPRESSED": FILE_ATTRIBUTE_COMPRESSED, "FILE_ATTRIBUTE_OFFLINE": FILE_ATTRIBUTE_OFFLINE, "FILE_ATTRIBUTE_NOT_CONTENT_INDEXED": FILE_ATTRIBUTE_NOT_CONTENT_INDEXED, "FILE_ATTRIBUTE_ENCRYTED": FILE_ATTRIBUTE_ENCRYTED}

	fileattributeflagsset = "\n         ".join(name for name, value in fileattributeflag_vars.items() if value == 1)
	lnkmarkers.append(f"\n+4 Link flags\n    SET: {fileattributeflagsset}\n")


	lnkmarkers.append("\n+4 File attribute flags\nSee section: File attribute flags\n")
	lnkmarkers.append("\n+8 Creation date and time\nContains a FILETIME or 0 if not set\n")
	lnkmarkers.append("\n+8 Last access date and time\nContains a FILETIME or 0 if not set\n")
	lnkmarkers.append("\n+8 Last modification date and time\nContains a FILETIME or 0 if not set\n")
	lnkmarkers.append("\n+4 File size in bytes\nContains an unsigned integer\n")
	lnkmarkers.append("\n+4 Icon index value\nContains a signed integer\n")
	lnkmarkers.append("\n+4 ShowWindow value\nContains an unsigned integer\nSee section: Show Window definitions\n")
	lnkmarkers.append("\n+2 Hot key\nSee section: Hot Key definitions\n")
	lnkmarkers.append("\n+2 Unknown (Reserved)\n")
	lnkmarkers.append("\n+4 Unknown (Reserved)\n")
	lnkmarkers.append("\n+4 Unknown (Reserved)\n")

	lnktemplate.append(fileheader)
	lnksizes.append(fileheadersize)

	linktargetidlistsize = 0
	if HasLinkTargetIDList:
		linktargetidlist = [[1, 2]]
		linktargetidlistsize = 2

		parsedlinktargetidlistsize = int(swapEndianness("".join(hexdata[b] for b in range(fileheadersize , fileheadersize + 2))), 16)
		lnkmarkers.append(f"+2 Link Target ID List Size ({parsedlinktargetidlistsize} bytes)")

		temp = parsedlinktargetidlistsize
		itemidsizelist = []
		classtypeindicatorlist = []
		pointerlist = []
		pointer = fileheadersize + 2
		while temp > 0:
			itemidsize = int(swapEndianness("".join(hexdata[b] for b in range(pointer, pointer + 2))), 16)
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
	if HasLinkInfo:
		linkinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4]]
		linkinfosize = 28	

		seek = linkinfooffset = fileheadersize + linktargetidlistsize
		parsedlinkinfosize = int(swapEndianness("".join(hexdata[b] for b in range(seek , seek + 4))), 16)
		parsedlinkinfoheadersize = int(swapEndianness("".join(hexdata[b] for b in range(seek + 4, seek + 8))), 16)

		lnkmarkers.append(f"\n+4 LinkInfoSize including these 4 bytes ({parsedlinkinfosize} bytes)\n")
		lnkmarkers.append(f"\n    +4 Link Info Header Size ({parsedlinkinfoheadersize})\n")

		linkinfoflags = format(int(swapEndianness("".join(hexdata[b] for b in range(seek + 8, seek + 12))), 16), 'b').zfill(32)
		VolumeIDAndLocalBasePath = int(linkinfoflags[31]); CommonNetworkRelativeLinkAndPathSuffix = int(linkinfoflags[30])
		linkinfoflag_vars = {"VolumeIDAndLocalBasePath": VolumeIDAndLocalBasePath,	"CommonNetworkRelativeLinkAndPathSuffix": CommonNetworkRelativeLinkAndPathSuffix}
		linkinfoflagsset = "\n             ".join(name for name, value in linkinfoflag_vars.items() if value == 1)
		lnkmarkers.append(f"\n    +4 Link Info flags\n        SET: {linkinfoflagsset}\n")
		
		volumeinformationoffset = linkinfooffset + int(swapEndianness("".join(hexdata[b] for b in range(seek + 12 , seek + 16))), 16)
		localbasepathoffset = linkinfooffset + int(swapEndianness("".join(hexdata[b] for b in range(seek + 16, seek + 20))), 16)
		if VolumeIDAndLocalBasePath:
			lnkmarkers.append(f"\n    +4 Offset to the volume information\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(volumeinformationoffset)}\n")
			lnkmarkers.append(f"\n    +4 Offset to the local base path\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(localbasepathoffset)}\n")
		else:
			lnkmarkers.append("\n    +4 Offset to the volume information\n       0x00000000 as the flag VolumeIDAndLocalBasePath is not set\n")
			lnkmarkers.append("\n    +4 Offset to the local base path\n       0x00000000 as the flag VolumeIDAndLocalBasePath is not set\n")

		seek = fileheadersize + linktargetidlistsize
		commonnetworkrelativelinkoffset = linkinfooffset + int(swapEndianness("".join(hexdata[b] for b in range(seek +  20, seek + 24))), 16)
		if CommonNetworkRelativeLinkAndPathSuffix:
			lnkmarkers.append(f"\n    +4 Offset to the common network relative link\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(commonnetworkrelativelinkoffset)}\n")
		else:
			lnkmarkers.append("\n    +4 Offset to the common network relative link\n       0x00000000 as the flag CommonNetworkRelativeLinkAndPathSuffix is not set\n")

		commonpathsuffixoffset = linkinfooffset + int(swapEndianness("".join(hexdata[b] for b in range(seek +  24, seek + 28))), 16)
		lnkmarkers.append(f"\n    +4 Offset to the common path suffix\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(commonpathsuffixoffset)}\n")

		# ------------------------------------------------------------------------------------------------------
		# Parsing FIELDS LocalBasePathOffsetUnicode and CommonPathSuffixOffsetUnicode
		if parsedlinkinfoheadersize >= 36:
			start = sum(linkinfo[-1]); linkinfo.append([start, 4]); linkinfosize += 4
			localbasepathunicodeoffset = linkinfooffset + int(swapEndianness("".join(hexdata[b] for b in range(seek + 28, seek + 32))), 16)
			if VolumeIDAndLocalBasePath:
				lnkmarkers.append(f"\n    +4 Offset to the local base path in unicode\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(localbasepathunicodeoffset)}\n")
			else:
				lnkmarkers.append("    +4 Offset to the local base path in unicode\n       0x00000000 as the flag VolumeIDAndLocalBasePath is not set\n")

			start = sum(linkinfo[-1]); linkinfo.append([start, 4]); linkinfosize += 4
			commonpathsuffixunicodeoffset = linkinfooffset + int(swapEndianness("".join(hexdata[b] for b in range(seek + 32, seek + 36))), 16)
			lnkmarkers.append(f"\n    +4 Offset to the common path suffix in unicode\n       Relative to the LinkInfo struct\n       Absolute offset: {getOffset(commonpathsuffixunicodeoffset)}\n")

		# Parsing STRUCT VolumeID and FIELD LocalBasePath
		if VolumeIDAndLocalBasePath:
			# VolumeID Data Structure
			seek = fileheadersize + linktargetidlistsize + linkinfosize
			for _ in range(4):
				start = sum(linkinfo[-1]); linkinfo.append([start, 4]); linkinfosize += 4

			parsedvolumeidsize = int(swapEndianness("".join(hexdata[b] for b in range(seek, seek + 4))), 16)
			lnkmarkers.append(f"\n    +4 VolumeIDSize (> 16) including these 4 bytes: {parsedvolumeidsize}\n")

			drivetype = int(swapEndianness("".join(hexdata[b] for b in range(seek + 4, seek + 4 + 4))), 16)
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

			driveserialnumber = swapEndianness("".join(hexdata[b] for b in range(seek + 4 + 4, seek + 4 + 4 + 4)))
			lnkmarkers.append("\n        +4 Drive serial number\n")

			volumelabeloffset = swapEndianness("".join(hexdata[b] for b in range(seek + 4 + 4 + 4, seek + 4 + 4 + 4 + 4)))
			lnkmarkers.append("\n        +4 Offset to the volume label\n")
			if volumelabeloffset == "00000014":
				start = sum(linkinfo[-1]); linkinfo.append([start, 4]); linkinfosize += 4
				lnkmarkers.append("\n        +4 Offset to the volume label in unicode (Ignore previous offset)\n")

			# bigseek = seek + parsedvolumeidsize
			# lilseek = fileheadersize + linktargetidlistsize + linkinfosize
			# volumelabelsize = bigseek - lilseek
			# if volumelabelsize > 0:
			# 	start = sum(linkinfo[-1]); linkinfo.append([start, volumelabelsize]); linkinfosize += volumelabelsize
			# 	lnkmarkers.append(f"\n        +{volumelabelsize} Volume label of the drive (null-terminated)\n")

			seek = fileheadersize + linktargetidlistsize + linkinfosize
			volumelabelsize = getNullTerminatedStringSize("".join(hexdata[seek:]))
			if volumelabelsize > 0:
				start = sum(linkinfo[-1]); linkinfo.append([start, volumelabelsize]); linkinfosize += volumelabelsize
				lnkmarkers.append(f"\n        +{volumelabelsize} Volume label of the drive (null-terminated)\n")

			# LocalBasePath
			localbasepathsize = getNullTerminatedStringSize("".join(hexdata[seek + volumelabelsize:]))
			# localbasepath = "".join(hexdata[b] for b in range(seek + volumelabelsize, seek + volumelabelsize + localbasepathsize))
			start = sum(linkinfo[-1]); linkinfo.append([start, localbasepathsize]); linkinfosize += localbasepathsize
			lnkmarkers.append(f"\n    +{localbasepathsize} Local base path (null-terminated)\n")

		# Parsing STRUCT CommonNetworkRelativeLink 
		if CommonNetworkRelativeLinkAndPathSuffix:
			bigseek = fileheadersize + linktargetidlistsize + linkinfosize
			seek = commonnetworkrelativelinkoffset
			sizeofunknown = seek-bigseek
			if sizeofunknown > 0:
				start = sum(linkinfo[-1]); linkinfo.append([start, sizeofunknown]); linkinfosize += sizeofunknown
				lnkmarkers.append(f"\n+{sizeofunknown} !!!UNKNOWN FIELD TO BE DEBUGGED!!!\n")
			for _ in range(5):
				start = sum(linkinfo[-1]); linkinfo.append([start, 4]); linkinfosize += 4
			

			parsedcommonnetworkrelativelinksize = int(swapEndianness("".join(hexdata[b] for b in range(seek, seek + 4))), 16)
			lnkmarkers.append(f"\n    +4 CommonNetworkRelativeLinkSize (>= 20): {parsedcommonnetworkrelativelinksize}\n")
			
			commonnetworkrelativelinkflags = format(int(swapEndianness("".join(hexdata[b] for b in range(seek + 4, seek + 8))), 16), 'b').zfill(32)
			ValidDevice = int(commonnetworkrelativelinkflags[31]); ValidNetType = int(commonnetworkrelativelinkflags[30])
			commonnetworkrelativelinkflag_vars = {"ValidDevice": ValidDevice,	"ValidNetType": ValidNetType}
			commonnetworkrelativelinkflagsset = "\n         ".join(name for name, value in commonnetworkrelativelinkflag_vars.items() if value == 1)
			lnkmarkers.append(f"\n        +4 CommonNetworkRelativeLinkFlags\n            SET: {commonnetworkrelativelinkflagsset}\n")

			netnameoffset = int(swapEndianness("".join(hexdata[b] for b in range(seek + 8, seek + 12))), 16)
			lnkmarkers.append("\n        +4 Offset to the net name\n           Relative to the CommonNetworkRelativeLink struct\n")
			
			if ValidDevice:
				lnkmarkers.append("\n        +4 Offset to the device name\n           Relative to the CommonNetworkRelativeLink struct")
			else:
				lnkmarkers.append("\n        +4 Offset to the device name\n           0x00000000 as the flag ValidDevice is not set\n")

			if ValidNetType:
				networkprovidertype = int(swapEndianness("".join(hexdata[b] for b in range(seek + 16, seek + 20))), 16)
				lnkmarkers.append(f"\n        +4 Network provider type ({getNetVendor(networkprovidertype)})\n")
			else:
				lnkmarkers.append("\n        +4 Network provider type\n           Ignore as the flag ValidNetType is not set")

			print("NETNAMEOFFSET: ", netnameoffset)
			if netnameoffset > 20:
				start = sum(linkinfo[-1]); linkinfo.append([start, 4]); linkinfosize += 4
				lnkmarkers.append("\n        +4 Offset to the net name in unicode\n           Relative to the CommonNetworkRelativeLink struct")

				start = sum(linkinfo[-1]); linkinfo.append([start, 4]); linkinfosize += 4
				if ValidDevice:
					lnkmarkers.append("\n        +4 Offset to the device name in unicode\n           Relative to the CommonNetworkRelativeLink struct")
				else:
					lnkmarkers.append("\n        +4 Offset to the device name in unicode\n           0x00000000 as the flag ValidDevice is not set\n")
				

			seek = fileheadersize + linktargetidlistsize + linkinfosize
			netnamesize = getNullTerminatedStringSize("".join(hexdata[seek:]))
			start = sum(linkinfo[-1]); linkinfo.append([start, netnamesize]); linkinfosize += netnamesize
			lnkmarkers.append(f"\n        +{netnamesize} Net name (null-terminated)\n")

			if ValidDevice: ##########################
				devicenamesize = getNullTerminatedStringSize("".join(hexdata[seek + netnamesize:]))
				start = sum(linkinfo[-1]); linkinfo.append([start, devicenamesize]); linkinfosize += devicenamesize
				lnkmarkers.append(f"\n        +{devicenamesize} Device name (null-terminated)\n")

			if netnameoffset > 20:
				seek = fileheadersize + linktargetidlistsize + linkinfosize
				netnameunicodesize = getNullTerminatedUnicodeStringSize("".join(hexdata[seek:]))
				start = sum(linkinfo[-1]); linkinfo.append([start, netnameunicodesize]); linkinfosize += netnameunicodesize
				lnkmarkers.append(f"\n        +{netnameunicodesize} Net name in unicode (null-terminated)\n")

				if ValidDevice: ##########################
					seek = fileheadersize + linktargetidlistsize + linkinfosize
					devicenameunicodesize = getNullTerminatedUnicodeStringSize("".join(hexdata[seek:]))
					start = sum(linkinfo[-1]); linkinfo.append([start, devicenameunicodesize]); linkinfosize += devicenameunicodesize
					lnkmarkers.append(f"\n        +{devicenameunicodesize} Device name in unicode (null-terminated)\n")
			
		# Parsing FIELD CommonPathSuffix
		seek = fileheadersize + linktargetidlistsize + linkinfosize
		commonpathsuffixsize = getNullTerminatedStringSize("".join(hexdata[seek:]))
		# commonpathsuffix = "".join(hexdata[b] for b in range(seek, seek + commonpathsuffixsize))
		start = sum(linkinfo[-1]); linkinfo.append([start, commonpathsuffixsize]); linkinfosize += commonpathsuffixsize
		lnkmarkers.append(f"\n    +{commonpathsuffixsize} Common path suffix (null-terminated)\n")
		# print(f"FULL TARGET PATH: {localbasepath+commonpathsuffix}")

		# Parsing FIELDS LocalBasePathUnicode and CommonPathSuffixUnicode
		if parsedlinkinfoheadersize >= 36:
			# LocalBasePathUnicode
			if VolumeIDAndLocalBasePath:
				localbasepathunicodesize = getNullTerminatedUnicodeStringSize("".join(hexdata[seek+commonpathsuffixsize:]))
				start = sum(linkinfo[-1]); linkinfo.append([start, localbasepathunicodesize]); linkinfosize += localbasepathunicodesize
				lnkmarkers.append(f"\n    +{localbasepathunicodesize} Local base path in unicode\n")

			# CommonPathSuffixUnicode
			seek = fileheadersize + linktargetidlistsize + linkinfosize
			commonpathsuffixunicodesize = getNullTerminatedUnicodeStringSize("".join(hexdata[commonpathsuffixunicodeoffset:]))
			unknownsize = commonpathsuffixunicodeoffset - seek

			start = sum(linkinfo[-1]); linkinfo.append([start, unknownsize]); linkinfosize += unknownsize
			lnkmarkers.append(f"+{unknownsize}!!!UNKNOWN FIELD TO BE DEBUGGED!!!")
			
			start = sum(linkinfo[-1]); linkinfo.append([start, commonpathsuffixunicodesize]); linkinfosize += commonpathsuffixunicodesize
			lnkmarkers.append(f"\n    +{commonpathsuffixunicodesize} Common path suffix in unicode\n")

		lnktemplate.append(linkinfo)
		lnksizes.append(linkinfosize)
	
	# Parsing STRUCT StringData
	def parseStringData(hexdata, seek, IsUnicode, stringdata, stringdatasize, lnkmarkers, description):
		charcount = int(swapEndianness("".join(hexdata[b] for b in range(seek, seek + 2))), 16)
		datasize = charcount * 2 if IsUnicode else charcount
		stringdata.append([1, 2 + datasize] if not stringdata else [sum(stringdata[-1]), 2 + datasize])
		stringdatasize += 2 + datasize
		lnkmarkers.append(f"\n+{2 + datasize} {description} (First 2 bytes is character count)\n")
		seek += 2 + datasize
		return seek, stringdata, stringdatasize

	stringdatasize = 0
	stringdata = []
	seek = fileheadersize + linktargetidlistsize + linkinfosize

	if HasName:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, IsUnicode, stringdata, stringdatasize, lnkmarkers, "Shortcut description")
	if HasRelativePath:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, IsUnicode, stringdata, stringdatasize, lnkmarkers, "Relative path of target w.r.t. this LNK file")
	if HasWorkingDir:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, IsUnicode, stringdata, stringdatasize, lnkmarkers, "Working directory to be used when activating the link target")
	if HasArguments:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, IsUnicode, stringdata, stringdatasize, lnkmarkers, "Command line arguments at the time of activating the link target")
	if HasIconLocation:
		seek, stringdata, stringdatasize = parseStringData(hexdata, seek, IsUnicode, stringdata, stringdatasize, lnkmarkers, "Icon location")

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

			lnkmarkers.append("\n+4 Console Data Block size including these 4 bytes (Must be 0x000000CC)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA0000002)\n")
			lnkmarkers.append("\n    +2 Fill attributes\n") # TODO: Parse attributes
			lnkmarkers.append("\n    +2 Popup fill attributes\n") # TODO: Parse attributes

			# TODO: Parse all sizes
			lnkmarkers.append("\n    +2 Horizontal size of the console window buffer (in characters)\n")
			lnkmarkers.append("\n    +2 Vertical size of the console window buffer (in characters)\n")
			lnkmarkers.append("\n    +2 Horizontal window size of the console window (in characters)\n")
			lnkmarkers.append("\n    +2 Vertical window size of the console window (in characters)\n")
			lnkmarkers.append("\n    +2 Horizontal coordinate of the console window origin (in pixels)\n")
			lnkmarkers.append("\n    +2 Vertical coordinate of the console window origin (in pixels)\n")

			lnkmarkers.append("\n    +4 Unused1 (A value that is undefined and MUST be ignored.)\n")
			lnkmarkers.append("\n    +4 Unused2 (A value that is undefined and MUST be ignored.)\n")
			lnkmarkers.append("\n    +4 Size of font used in the console window\n") # TODO: Parse the 2 words
			lnkmarkers.append("\n    +4 Family of font used in the console window\n") # TODO: Parse font families
			lnkmarkers.append("\n    +4 Stroke weight of font used in the console window\n") # TODO: Parse value
			lnkmarkers.append("\n    +64 Face name of font used in the console window in unicode\n")
			lnkmarkers.append("\n    +4 Size of cursor used in the console window (in pixels)\n")
			lnkmarkers.append("\n    +4 Full-screen mode status\n") # TODO: Parse value
			lnkmarkers.append("\n    +4 QuickEdit mode status (In QuickEdit mode, the mouse can be used to cut, copy, and paste text in the console window.)\n") # TODO: Parse value
			lnkmarkers.append("\n    +4 Insert mode status\n") # TODO: Parse value
			lnkmarkers.append("\n    +4 Auto-position mode status\n") # TODO: Parse value
			lnkmarkers.append("\n    +4 Size of the buffer used to store history of the user input in the console window (in characters)\n")
			lnkmarkers.append("\n    +4 Number of history buffers to use\n")
			lnkmarkers.append("\n    +4 Grant status of duplicates in history\n") # TODO: Parse value
			lnkmarkers.append("\n    +64 RGB colors used for text in the console window\n") # TODO: Parse value

			lnktemplate.append(consoledatablock)
			lnksizes.append(consoledatablocksize)
			seek += consoledatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000004":
			print("DATA BLOCK PRESENT: CONSOLEFE")
			consolefedatablock = [[1, 4], [5, 4], [9, 4]]
			consolefedatablocksize = 12

			lnkmarkers.append("\n+4 Console FE Data Block size including these 4 bytes (Must be 0x0000000C)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA0000004)\n")
			lnkmarkers.append("\n    +4 Code page language code identifier\n") # TODO: see [MS-LCID]

			lnktemplate.append(consolefedatablock)
			lnksizes.append(consolefedatablocksize)
			seek += consolefedatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000006":
			print("DATA BLOCK PRESENT: DARWIN")
			darwindatablock = [[1, 4], [5, 4], [9, 260], [269, 520]]
			darwindatablocksize = 788
			
			lnkmarkers.append("\n+4 Darwin Data Block size including these 4 bytes (Must be 0x00000314)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA0000006)\n")
			lnkmarkers.append("\n    +260 MSI application identifier (Should be ignored) (null-terminated)\n")
			lnkmarkers.append("\n    +520 MSI application identifier in unicode (null-terminated)\n")

			lnktemplate.append(darwindatablock)
			lnksizes.append(darwindatablocksize)
			seek += darwindatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000001":
			print("DATA BLOCK PRESENT: ENVIRONMENT VARIABLE")
			environmentvariabledatablock = [[1, 4], [5, 4], [9, 260], [269, 520]]
			environmentvariabledatablocksize = 788
			
			lnkmarkers.append("\n+4 Environment Variable Data Block size including these 4 bytes (Must be 0x00000314)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA0000001)\n")
			lnkmarkers.append("\n    +260 Path to environment variable information (null-terminated)\n")
			lnkmarkers.append("\n    +520 Path to environment variable information in unicode (null-terminated)\n")

			lnktemplate.append(environmentvariabledatablock)
			lnksizes.append(environmentvariabledatablocksize)
			seek += environmentvariabledatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000007":
			print("DATA BLOCK PRESENT: ICON ENVIRONMENT")
			iconenvironmentdatablock = [[1, 4], [5, 4], [9, 260], [269, 520]]
			iconenvironmentdatablocksize = 788
			
			lnkmarkers.append("\n+4 Icon Environment Data Block size including these 4 bytes (Must be 0x00000314)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA0000007)\n")
			lnkmarkers.append("\n    +260 Path constructed with environment variables (null-terminated)\n")
			lnkmarkers.append("\n    +520 Path constructed with environment variables in unicode (null-terminated)\n")

			lnktemplate.append(iconenvironmentdatablock)
			lnksizes.append(iconenvironmentdatablocksize)
			seek += iconenvironmentdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A000000B":
			print("DATA BLOCK PRESENT: KNOWN FOLDER")
			# not DisableKnownFolderTracking
			knownfolderdatablock = [[1, 4], [5, 4], [9, 16], [25, 4]]
			knownfolderdatablocksize = 28

			lnkmarkers.append("\n+4 Known Folder Data Block size including these 4 bytes (Must be 0x0000001C)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA000000B)\n")
			lnkmarkers.append("\n    +16 Folder GUID\n")
			lnkmarkers.append("\n    +4 Offset to the ItemID of the first child segment of the above IDList\n")

			lnktemplate.append(knownfolderdatablock)
			lnksizes.append(knownfolderdatablocksize)
			seek += knownfolderdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000009":
			print("DATA BLOCK PRESENT: PROPERTY STORE")
			# TODO: Parse Serialized Property Storage Struct from [MS-PROPSTORE]
			propertystoredatablock = [[1, 4], [5, 4]]
			propertystoredatablocksize = int(swapEndianness("".join(hexdata[b] for b in range(seek, seek + 4))), 16)
			start = sum(propertystoredatablock[-1]); propertystoredatablock.append([start, propertystoredatablocksize - 8]); 

			lnkmarkers.append("\n+4 Property Store Data Block size including these 4 bytes (Must be >= 0x0000000C)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA0000009)\n")
			lnkmarkers.append(f"\n    +{propertystoredatablocksize-8} Serialized property storage structure\n")
			
			lnktemplate.append(propertystoredatablock)
			lnksizes.append(propertystoredatablocksize)
			seek += propertystoredatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000008":
			print("DATA BLOCK PRESENT: SHIM")
			shimdatablock = [[1, 4], [5, 4]]
			shimdatablocksize = int(swapEndianness("".join(hexdata[b] for b in range(seek , seek + 4))), 16)

			lnkmarkers.append("\n+4 Shim Data Block size including these 4 bytes (Must be >= 0x00000088)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA0000008)\n")

			# layernamesize = getNullTerminatedUnicodeStringSize("".join(hexdata[seek + 8:]))
			start = sum(shimdatablock[-1]); shimdatablock.append([start, shimdatablocksize-8])
			lnkmarkers.append(f"\n    +{shimdatablocksize-8} Shim layer name to apply to a link target when activated in unicode (null-terminated)\n")

			lnktemplate.append(shimdatablock)
			lnksizes.append(shimdatablocksize)
			seek += shimdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000005":
			print("DATA BLOCK PRESENT: SPECIAL FOLDER")
			specialfolderdatablock = [[1, 4], [5, 4], [9, 4], [13, 4]]
			specialfolderdatablocksize = 16

			lnkmarkers.append("\n+4 Special Folder Data Block size including these 4 bytes (Must be 0x00000010)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA0000005)\n")
			lnkmarkers.append("\n    +4 Folder integer ID\n")
			lnkmarkers.append("\n    +4 Offset to the ItemID of the first child segment of the above IDList\nRelative to the LinkTargetIDList struct")

			lnktemplate.append(specialfolderdatablock)
			lnksizes.append(specialfolderdatablocksize)
			seek += specialfolderdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A0000003":
			print("DATA BLOCK PRESENT: TRACKER")
			trackerdatablock = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 16], [33, 16], [49, 16], [65, 16], [81, 16]]
			trackerdatablocksize = 96

			lnkmarkers.append("\n+4 Tracker Data Block size including these 4 bytes (Must be 0x00000060)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA0000003)\n")
			lnkmarkers.append("\n    +4 Size of rest of Tracker Data Block, including these 4 bytes (Must be 0x00000058)\n")
			lnkmarkers.append("\n    +4 Version (Must be 0x00000000)\n")
			lnkmarkers.append("\n    +16 NetBIOS name of the machine where the link target was last known to reside (null-terminated with unused bytes set to 0)\n")
			lnkmarkers.append("\n    +16 Droid volume identifier (GUID containing an NTFS object identifier)\n")
			lnkmarkers.append("\n    +16 Droid file identifier (GUID containing an NTFS object identifier)\n")
			lnkmarkers.append("\n    +16 Birth droid volume identifier (GUID containing an NTFS object identifier)\n")
			lnkmarkers.append("\n    +16 Birth droid file identifier (GUID containing an NTFS object identifier)\n")

			lnktemplate.append(trackerdatablock)
			lnksizes.append(trackerdatablocksize)
			seek += trackerdatablocksize

		if getDataBlockSignature(seek, hexdata) == "A000000C":
			parsedlastdatablocksize = int(swapEndianness("".join(hexdata[b] for b in range(seek , seek + 4))), 16)
			print("DATA BLOCK PRESENT: VISTA")
			vistaandaboveidlistdatablock = [[1, 4], [5, 4]]
			vistaandaboveidlistdatablocksize = 8

			idlistsize = parsedlastdatablocksize - vistaandaboveidlistdatablocksize

			lnkmarkers.append("\n+4 Vista And Above ID List Data Block size including these 4 bytes (Must be >= 0x0000000A)\n")
			lnkmarkers.append("\n    +4 Block signature (Must be 0xA000000C)\n")
			lnkmarkers.append(f"\n    +{idlistsize} IDList\n") # TODO: Parse ItemIDList

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