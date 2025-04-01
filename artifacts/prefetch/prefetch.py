# Author: Nisarg Suthar

import binascii
from primer import *
from offsetter import *

#######################################################################################################
	# TODO: #
	#########

def prefetchTemplate(file_path):
	prefetchtemplate = []
	prefetchsizes = []
	prefetchmarkers = []

	formattedhexdata, formattedasciidata, hexdata = readFile(file_path)
#######################################################################################################
	# COMMON SECTION. #
	###################
	fileheader = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 60], [77, 4], [81, 4]]
	fileheadersize = 84
	prefetchmarkers.append("+4  Format version    \n    17 (0x00000011) > Windows XP, Windows 2003    \n    23 (0x00000017) > Windows Vista, Windows 7    \n    26 (0x0000001A) > Windows 8.1    \n    30 (0x0000001E) > Windows 10\n")
	prefetchmarkers.append("\n+4  Signature\n")
	prefetchmarkers.append("\n+4  Unknown\nSeen: 0x0000000F, 0x00000011\n")
	prefetchmarkers.append("\n+4  File size\n")
	prefetchmarkers.append("\n+60 Executable filename\nUTF-16 little-endian string with end-of-string character\n")
	prefetchmarkers.append("\n+4 Prefetch hash\nThis value should correspond with the hash in the Prefetch filename\n")
	prefetchmarkers.append("\n+4 Unknown (flags?)\n0x01 > is boot prefetch\n(Seen in: NTOSBOOT-B00DFAAD.pf, Op-EXPLORER.EXE-A80E4F97-000000F5.pf)\n")

	prefetchmarkers.append("\n+4 File metrics array offset\n    The offset is relative to the start of the file\n    0x00000098 > Version 17\n    0x000000F0 > Version 23\n    0x00000130 > Version 26\n    0x00000130 > Version 30, Variant 1\n    0x00000128 > Version 30, Variant 2\n")
	prefetchmarkers.append("\n+4 Number of file metrics entries\n")
	prefetchmarkers.append("\n+4 Trace chains array offset\nThe offset is relative to the start of the file\n")
	prefetchmarkers.append("\n+4 Number of trace chains array entries\n")
	prefetchmarkers.append("\n+4 Filename strings offset\n")
	prefetchmarkers.append("\n+4 Filename strings size\n")
	prefetchmarkers.append("\n+4 Volumes information offset\n")
	prefetchmarkers.append("\n+4 Number of volumes\n")
	prefetchmarkers.append("\n+4 Volumes information size\n")

	sharedFileMetricsByVer232630 = "    Each entry (+32) contains:\n        +4 Unknown (Prefetch start time in ms?)\n        Could be the index into the trace chain array as well, is this relationship implicit or explicit?\n        +4 Unknown (Prefetch duration in ms?)\n        Could be the number of entries in the trace chain as well, is this relationship implicit or explicit?\n        +4 Unknown (Average prefetch duration in ms?)\n        +4 Filename string offset\n        The offset is relative to the start of the filename strings\n        +4 Filename string number of characters\n        Does not include the end-of-string character\n        +4 Unknown (Flags?)\n        Seen: 0x00000001, 0x00000002, 0x00000003, 0x00000200, 0x00000202\n        +8 File reference\n        Contains a file reference of the file corresponding to the filename string or 0 if not set\n        NTFS:\n        First 6 bytes > MFT entry index\n        Last 2 bytes > Sequence number\n"

	sharedTraceChainsByVer172326 = "    Each entry (+12) contains:\n        +4 Next array entry index\n        Contains the next trace chain array entry index in the chain, where the first entry index starts with 0, or -1 (0xFFFFFFFF) for the end-of-chain.\n        +4 Total block load count\n        Total number of blocks loaded (or fetched)\n        The block size 512k (512 * 1024) bytes\n        +1 Unknown\n        Seen: 0x02, 0x03, 0x04, 0x08, 0x0A\n        +1 Unknown (Sample duration in ms?)\n        Seen: 0x01\n        +2 Unknown\n        Seen: 0x0001, 0xFFFF\n"

######################################################################
	# VERSION SPECIFIC. #
	#####################
	version = "".join(hexdata[b] for b in range(4))
	filemetricsoffset = int(swapEndianness("".join(hexdata[b] for b in range(84 , 88))), 16)
	numberoffilemetricsentries = int(swapEndianness("".join(hexdata[b] for b in range(88, 92))), 16)
	numberoftracechainsentries = int(swapEndianness("".join(hexdata[b] for b in range(96, 100))), 16)
	hashstringexists = False
	hashstringsize = hashstringoffset = 0
	filenamestringsoffset = int(swapEndianness("".join(hexdata[b] for b in range(100, 104))), 16)
	filenamestringssize = int(swapEndianness("".join(hexdata[b] for b in range(104, 108))), 16)
	volumesinformationoffset = int(swapEndianness("".join(hexdata[b] for b in range(108, 112))), 16)
	volumesinformationsize = int(swapEndianness("".join(hexdata[b] for b in range(116, 120))), 16)

	match version:
		case "11000000":
			# Was XP or 2003 > PFV 17
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 16], [61, 4], [65, 4]]
			fileinfosize = 68
			prefetchmarkers.append("\n+8 Last run time\nContains a FILETIME\n")
			prefetchmarkers.append("\n+16 Unknown (Empty values)\nSometimes contains remnant data?\n")
			prefetchmarkers.append("\n+4 Run count\n")
			prefetchmarkers.append("\n+4 Unknown\n")
			
			filemetricssize = numberoffilemetricsentries * 20
			filemetrics = [[1, filemetricssize]]
			prefetchmarkers.append(f"\n+{filemetricssize} File metrics array [{numberoffilemetricsentries} entries]\n    Each entry (+20) contains:\n        +4 Unknown (Prefetch start time in ms?)\n        Could be the index into the trace chain array as well, is this relationship implicit or explicit?\n        +4 Unknown (Prefetch duration in ms?)\n        Could be the number of entries in the trace chain as well, is this relationship implicit or explicit?\n        +4 Filename string offset\n        The offset is relative to the start of the filename strings\n        +4 Filename string number of characters\n        Does not include the end-of-string character\n        +4 Unknown (Flags?)\n")

			tracechainssize = numberoftracechainsentries * 12
			tracechains = [[1, tracechainssize]]

			prefetchmarkers.append(f"\n+{tracechainssize} Trace chains array [{numberoftracechainsentries} entries]\n{sharedTraceChainsByVer172326}")

		case "17000000":
			# Was Vista or 7 > PFV 23
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 8], [53, 16], [69, 4], [73, 4], [77, 80]]
			fileinfosize = 156
			prefetchmarkers.append("\n+8 Unknown (Empty values)\n")
			prefetchmarkers.append("\n+8 Last run time\nContains a FILETIME\n")
			prefetchmarkers.append("\n+16 Unknown (Empty values)\n")
			prefetchmarkers.append("\n+4 Run count\n")
			prefetchmarkers.append("\n+4 Unknown\nSeen: 0x01\n")
			prefetchmarkers.append("\n+80 Unknown (Empty values)\n")
			filemetricssize = numberoffilemetricsentries * 32
			filemetrics = [[1, filemetricssize]]
			prefetchmarkers.append(f"\n+{filemetricssize} File metrics array [{numberoffilemetricsentries} entries]\n{sharedFileMetricsByVer232630}")
			tracechainssize = numberoftracechainsentries * 12
			tracechains = [[1, tracechainssize]]
			prefetchmarkers.append(f"\n+{tracechainssize} Trace chains array [{numberoftracechainsentries} entries]\n{sharedTraceChainsByVer172326}")

		case "1A000000":
			# Was 8.1 > PFV 26
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 16], [125, 4], [129, 4], [133, 4], [137, 88]]
			fileinfosize = 224
			prefetchmarkers.append("\n+8 Unknown (Empty values)\n")
			prefetchmarkers.append("\n+64 (8 * 8) Last run time(s)\nContains FILETIMEs, or 0 if not set\nThe first FILETIME is the most recent run time\n")
			prefetchmarkers.append("\n+16 Unknown\nMostly empty values but seem to get filled the run after the 8 last run times have been filled.\nCould be remnant values.\n")
			prefetchmarkers.append("\n+4 Run count\n")
			prefetchmarkers.append("\n+4 Unknown\nSeen: 0x01, 0x02, 0x07\n")
			prefetchmarkers.append("\n+4 Unknown\nSeen: 0x00, 0x03\n")
			prefetchmarkers.append("\n+88 Unknown (Empty values)\n")
			filemetricssize = numberoffilemetricsentries * 32
			filemetrics = [[1, filemetricssize]]
			prefetchmarkers.append(f"\n+{filemetricssize} File metrics array [{numberoffilemetricsentries} entries]\n{sharedFileMetricsByVer232630}")
			tracechainssize = numberoftracechainsentries * 12
			tracechains = [[1, tracechainssize]]
			prefetchmarkers.append(f"\n+{tracechainssize} Trace chains array [{numberoftracechainsentries} entries]\n{sharedTraceChainsByVer172326}")

		case "1E000000":
			# Was 10 or 11 > PFV 30
			variant = "".join(hexdata[b] for b in range(84, 88))
			prefetchmarkers.append("\n+8 Unknown (Empty values)\n")
			prefetchmarkers.append("\n+64 (8 * 8) Last run time(s)\nContains FILETIMEs, or 0 if not set\nThe first FILETIME is the most recent run time\n")

			match variant:
				case "30010000":
					# Variant 1
					hso = "".join(hexdata[b] for b in range(220, 224))
					if hso == "00000000":
						fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 16], [125, 4], [129, 4], [133, 4], [137, 84]]
					else:
						hashstringexists = True
						fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 16], [125, 4], [129, 4], [133, 4], [137, 4], [141, 4], [145, 76]]
					fileinfosize = 220
					prefetchmarkers.append("\n+16 Unknown\nMostly empty values but seem to get filled the run after the 8 last run times have been filled.\nCould be remnant values.\n")
					prefetchmarkers.append("\n+4 Run count\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x01, 0x02, 0x07\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x00, 0x03\n")
				case "28010000":
					# Variant 2
					hso = "".join(hexdata[b] for b in range(212, 216))
					if hso == "00000000":
						fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 8], [117, 4], [121, 4], [125, 4], [129, 84]]
					else:
						hashstringexists = True
						fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 8], [117, 4], [121, 4], [125, 4], [129, 4], [133, 4], [137, 76]]
					fileinfosize = 212
					prefetchmarkers.append("\n+8 Unknown\nMostly empty values but seem to get filled the run after the 8 last run times have been filled.\nCould be remnant values.\n")
					prefetchmarkers.append("\n+4 Run count\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x01\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x03\n")
			if hashstringexists:
				prefetchmarkers.append("\n+4 Hash string offset\n")
				prefetchmarkers.append("\n+4 Hash string size\n")
				prefetchmarkers.append("\n+76 Unknown (Empty values)\n")
			else:
				prefetchmarkers.append("\n+84 Unknown (Empty values)\n")
			filemetricssize = numberoffilemetricsentries * 32
			filemetrics = [[1, filemetricssize]]
			prefetchmarkers.append(f"\n+{filemetricssize} File metrics array [{numberoffilemetricsentries} entries]\n{sharedFileMetricsByVer232630}")

			if hashstringexists:
				hashstringoffsetlocation = fileheadersize + fileinfosize - 76 - 4 - 4
				hashstringsizelocation = fileheadersize + fileinfosize - 76 - 4
				hashstringoffset = int(swapEndianness("".join(hexdata[b] for b in range(hashstringoffsetlocation, hashstringoffsetlocation+4))), 16)
				hashstringsize = int(swapEndianness("".join(hexdata[b] for b in range(hashstringsizelocation, hashstringsizelocation+4))), 16)

			tracechainssize = numberoftracechainsentries * 8
			tracechains = [[1, tracechainssize]]
			
			prefetchmarkers.append(f"\n+{tracechainssize} Trace chains array [{numberoftracechainsentries} entries]\n    Each entry (+8) contains:\n        +4 Total block load count\n        Total number of blocks loaded (or fetched)\n        The block size 512k (512 * 1024) bytes\n        +1 Unknown\n        Seen: 0x02, 0x03, 0x04, 0x08, 0x0A\n        +1 Unknown (Sample duration in ms?)\n        Seen: 0x01\n        +2 Unknown\n        Seen: 0x0001, 0xFFFF\n")

	sumtilltracechains = fileheadersize + fileinfosize + filemetricssize + tracechainssize	
	sumtillfilenamestrings = filenamestringssize + filenamestringsoffset
	sumtillhashstring = hashstringsize + hashstringoffset
	sumtillvolumeinformation = volumesinformationsize + volumesinformationoffset
	sumtillhashstringorfilenamestrings = sumtillhashstring if hashstringexists else sumtillfilenamestrings
	hashstringorfilenamestringspaddingsize = volumesinformationoffset - sumtillhashstringorfilenamestrings

	filenamestrings = [[1, filenamestringssize]]
	hashstring = [[1, hashstringsize]]
	hashstringorfilenamestringspadding = [[1, hashstringorfilenamestringspaddingsize]]
	volumeinformation = [[1, volumesinformationsize]]

	prefetchmarkers.append(f"\n+{filenamestringssize} File name strings\n")
	if hashstringexists:
		prefetchmarkers.append(f"\n+{hashstringsize} Hash string\nApplication Prefetch > Path to executable responsible for the generated prefetch file.\nApplication Hosting Prefetch > Package name of hosted application.\n")
	if hashstringorfilenamestringspaddingsize != 0:
		prefetchmarkers.append(f"\n+{hashstringorfilenamestringspaddingsize} Padding\n")
	prefetchmarkers.append(f"\n+{volumesinformationsize} Volume information\n")

	prefetchtemplate.append(fileheader)
	prefetchtemplate.append(fileinfo)
	prefetchtemplate.append(filemetrics)
	prefetchtemplate.append(tracechains)
	prefetchtemplate.append(filenamestrings)
	if hashstringexists:
		prefetchtemplate.append(hashstring)
	if hashstringorfilenamestringspaddingsize != 0:
		prefetchtemplate.append(hashstringorfilenamestringspadding)
	prefetchtemplate.append(volumeinformation)
	
	prefetchsizes.append(fileheadersize)
	prefetchsizes.append(fileinfosize)
	prefetchsizes.append(filemetricssize)
	prefetchsizes.append(tracechainssize)
	prefetchsizes.append(filenamestringssize)
	if hashstringexists:
		prefetchsizes.append(hashstringsize)
	if hashstringorfilenamestringspaddingsize != 0:
		prefetchsizes.append(hashstringorfilenamestringspaddingsize)
	prefetchsizes.append(volumesinformationsize)

	templatedata = toAbsolute(prefetchtemplate, prefetchsizes)
	
	return formattedhexdata, formattedasciidata, templatedata, prefetchmarkers