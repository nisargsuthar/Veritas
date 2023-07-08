import binascii
from primer import *
from offsetter import *

######################################################################
	# TODO: #
	#########
	# Update markers for file metrics array and trace chains array to include structure of a single entry.
	# Implement logic to detect presence of hash string in Version 30, Variant 1. (As of now, it always assumes it present and so the template turns incorrect sometimes.)

def prefetchTemplate(file_path):
	prefetchtemplate = []
	prefetchsizes = []
	prefetchmarkers = []

	getdata = getHexAsciiFromBytes(file_path)
	formattedhexdata = getdata[0]
	formattedasciidata = getdata[1]
	hexdata = getdata[2]
	# print(formattedhexdata)
	# print(hexdata)
######################################################################
	# COMMON SECTION. #
	###################
	fileheader = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 60], [77, 4], [81, 4]]
	fileheadersize = 84
	prefetchmarkers.append("+4  Format version    \n17 (0x11) > Windows XP, Windows 2003    \n23 (0x17) > Windows Vista, Windows 7    \n26 (0x1A) > Windows 8.1    \n30 (0x1E) > Windows 10\n")
	prefetchmarkers.append("\n+4  Signature\n")
	prefetchmarkers.append("\n+4  Unknown\nSeen: 0x0000000F, 0x00000011\n")
	prefetchmarkers.append("\n+4  File size\n")
	prefetchmarkers.append("\n+60 Executable filename\nUTF-16 little-endian string with end-of-string character\n")
	prefetchmarkers.append("\n+4 Prefetch hash\nThis value should correspond with the hash in the Prefetch filename\n")
	prefetchmarkers.append("\n+4 Unknown (flags?)\n0x01 > is boot prefetch\n(Seen in: NTOSBOOT-B00DFAAD.pf, Op-EXPLORER.EXE-A80E4F97-000000F5.pf)\n")

	prefetchmarkers.append("\n+4 File metrics array offset\nThe offset is relative to the start of the file\n0x98 > Version 17\n0xF0 > Version 23\n0x3001 > Version 26\n0x3001 > Version 30, Variant 1\n0x2801 > Version 30, Variant 2\n")
	prefetchmarkers.append("\n+4 Number of file metrics entries\n")
	prefetchmarkers.append("\n+4 Trace chains array offset\nThe offset is relative to the start of the file\n")
	prefetchmarkers.append("\n+4 Number of trace chains array entries\n")
	prefetchmarkers.append("\n+4 Filename strings offset\n")
	prefetchmarkers.append("\n+4 Filename strings size\n")
	prefetchmarkers.append("\n+4 Volumes information offset\n")
	prefetchmarkers.append("\n+4 Number of volumes\n")
	prefetchmarkers.append("\n+4 Volumes information size\n")
	
	# sharedFileInfoByVar1AndVer26 = []
	# sharedFileInfoByVar1AndVer26.append("\n+8 Unknown (Empty values)\n")
	# sharedFileInfoByVar1AndVer26.append("\n+64 (8 * 8) Last run time(s)\nContains FILETIMEs, or 0 if not set\nThe first FILETIME is the most recent run time\n")
	# sharedFileInfoByVar1AndVer26.append("\n+16 Unknown\nMostly empty values but seem to get filled the run after the 8 last run times have been filled.\nCould be remnant values.\n")
	# sharedFileInfoByVar1AndVer26.append("\n+4 Run count\n")
	# sharedFileInfoByVar1AndVer26.append("\n+4 Unknown\nSeen: 0x01, 0x02, 0x07\n")
	# sharedFileInfoByVar1AndVer26.append("\n+4 Unknown\nSeen: 0x00, 0x03\n")
	# sharedFileInfoByVar1AndVer26.append("\n+88 Unknown (Empty values)\n")

	# sharedFileMetricsByVer232630 = []
	# sharedFileMetricsByVer232630.append("\n+4 Unknown (Prefetch start time in ms?)\nCould be the index into the trace chain array as well, is this relationship implicit or explicit?\n")
	# sharedFileMetricsByVer232630.append("\n+4 Unknown (Prefetch duration in ms?)\nCould be the number of entries in the trace chain as well, is this relationship implicit or explicit?\n")
	# sharedFileMetricsByVer232630.append("\n+4 Unknown (Average prefetch duration in ms?)\n")
	# sharedFileMetricsByVer232630.append("\n+4 Filename string offset\nThe offset is relative to the start of the filename strings\n")
	# sharedFileMetricsByVer232630.append("\n+4 Filename string number of characters\nDoes not include the end-of-string character\n")
	# sharedFileMetricsByVer232630.append("\n+4 Unknown (Flags?)\nSeen: 0x00000001, 0x00000002, 0x00000003, 0x00000200, 0x00000202\n")
	# sharedFileMetricsByVer232630.append("\n+8 File reference\nContains a file reference of the file corresponding to the filename string or 0 if not set\nNTFS:\nFirst 6 bytes > MFT entry index\nLast 2 bytes > Sequence number\n")

	# sharedTraceChainsByVer172326 = []
	# sharedTraceChainsByVer172326.append("\nNext array entry index\nContains the next trace chain array entry index in the chain, where the first entry index starts with 0, or -1 (0xFFFFFFFF) for the end-of-chain.\n")
	# sharedTraceChainsByVer172326.append("\nTotal block load count\nTotal number of blocks loaded (or fetched)\nThe block size 512k (512 * 1024) bytes\n")
	# sharedTraceChainsByVer172326.append("\nUnknown\nSeen: 0x02, 0x03, 0x04, 0x08, 0x0A\n")
	# sharedTraceChainsByVer172326.append("\nUnknown (Sample duration in ms?)\nSeen: 0x01\n")
	# sharedTraceChainsByVer172326.append("\nUnknown\nSeen: 0x0001, 0xFFFF\n")

######################################################################
	# VERSION SPECIFIC. #
	#####################
	version = "".join(hexdata[b] for b in range(4)).upper()
	filemetricsoffset = int(swapEndianness("".join(hexdata[b] for b in range(84 , 88)).upper()), 16)
	numberoffilemetricsentries = int(swapEndianness("".join(hexdata[b] for b in range(88, 92)).upper()), 16)
	numberoftracechainsentries = int(swapEndianness("".join(hexdata[b] for b in range(96, 100)).upper()), 16)
	hashstringexists = False
	hashstringsize = hashstringoffset = 0
	filenamestringsoffset = int(swapEndianness("".join(hexdata[b] for b in range(100, 104)).upper()), 16)
	filenamestringssize = int(swapEndianness("".join(hexdata[b] for b in range(104, 108)).upper()), 16)
	volumesinformationoffset = int(swapEndianness("".join(hexdata[b] for b in range(108, 112)).upper()), 16)
	volumesinformationsize = int(swapEndianness("".join(hexdata[b] for b in range(116, 120)).upper()), 16)

	match version:
		case "11000000":
			# Was XP or 2003 > PFV 17
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 16], [61, 4], [65, 4]]
			fileinfosize = 68
			prefetchmarkers.append("\n+8 Last run time\nContains a FILETIME\n")
			prefetchmarkers.append("\n+16 Unknown (Empty values)\nSometimes contains remnant data?\n")
			prefetchmarkers.append("\n+4 Run count\n")
			prefetchmarkers.append("\n+4 Unknown\n")
			
			filemetricssize = numberoffilemetricsentries * 20 # 20 bytes per entry.
			filemetrics = [[1, filemetricssize]]
			prefetchmarkers.append("\n+{} File metrics array\n".format(filemetricssize))
			# filemetricsentrybytemask = [4, 4, 4, 4, 4]
			# filemetricsentry = generateEntriesFromByteMask(filemetricsentrybytemask, numberoffilemetricsentries * len(filemetricsentrybytemask))

			# prefetchmarkers.append("\nUnknown (Prefetch start time in ms?)\nCould be the index into the trace chain array as well, is this relationship implicit or explicit?\n")
			# prefetchmarkers.append("\nUnknown (Prefetch duration in ms?)\nCould be the number of entries in the trace chain as well, is this relationship implicit or explicit?\n")
			# prefetchmarkers.append("\nFilename string offset\nThe offset is relative to the start of the filename strings\n")
			# prefetchmarkers.append("\nFilename string number of characters\nDoes not include the end-of-string character\n")
			# prefetchmarkers.append("\nUnknown (Flags?)\n")

			tracechainssize = numberoftracechainsentries * 12
			tracechains = [[1, tracechainssize]]
			# tracechainsentrybytemask = [4, 4, 1, 1, 2]
			# tracechainsentry = generateEntriesFromByteMask(tracechainsentrybytemask, numberoftracechainsentries * len(tracechainsentrybytemask))

			# prefetchmarkers.extend(sharedTraceChainsByVer172326)
			prefetchmarkers.append("\n+{} Trace chains array\n".format(tracechainssize))

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
			prefetchmarkers.append("\n+{} File metrics array\n".format(filemetricssize))
			# filemetricsentrybytemask = [4, 4, 4, 4, 4, 4, 8]
			# filemetricsentry = generateEntriesFromByteMask(filemetricsentrybytemask, numberoffilemetricsentries * len(filemetricsentrybytemask))

			# prefetchmarkers.extend(sharedFileMetricsByVer232630)

			tracechainssize = numberoftracechainsentries * 12
			tracechains = [[1, tracechainssize]]
			# tracechainsentrybytemask = [4, 4, 1, 1, 2]
			# tracechainsentry = generateEntriesFromByteMask(tracechainsentrybytemask, numberoftracechainsentries * len(tracechainsentrybytemask))

			# prefetchmarkers.extend(sharedTraceChainsByVer172326)
			prefetchmarkers.append("\n+{} Trace chains array\n".format(tracechainssize))


		case "1A000000":
			# Was 8.1 > PFV 26
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 16], [125, 4], [129, 4], [133, 4], [137, 88]]
			fileinfosize = 224
			prefetchmarkers.extend(sharedFileInfoByVar1AndVer26)
			
			filemetricssize = numberoffilemetricsentries * 32
			filemetrics = [[1, filemetricssize]]
			prefetchmarkers.append("\n+{} File metrics array\n".format(filemetricssize))
			# filemetricsentrybytemask = [4, 4, 4, 4, 4, 4, 8]
			# filemetricsentry = generateEntriesFromByteMask(filemetricsentrybytemask, numberoffilemetricsentries * len(filemetricsentrybytemask))

			# prefetchmarkers.extend(sharedFileMetricsByVer232630)

			tracechainssize = numberoftracechainsentries * 12
			tracechains = [[1, tracechainssize]]
			# tracechainsentrybytemask = [4, 4, 1, 1, 2]
			# tracechainsentry = generateEntriesFromByteMask(tracechainsentrybytemask, numberoftracechainsentries * len(tracechainsentrybytemask))

			# prefetchmarkers.extend(sharedTraceChainsByVer172326)
			prefetchmarkers.append("\n+{} Trace chains array\n".format(tracechainssize))


		case "1E000000":
			# Was 10 or 11 > PFV 30
			variant = "".join(hexdata[b] for b in range(84, 88)).upper()

			match variant:
				case "30010000":
					# Variant 1
					hso = "".join(hexdata[b] for b in range(220, 224)).upper()
					if hso == "00000000":
						# Since both hash and non-hash variant 1 files have fileinfosize of 220.
						fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 16], [125, 4], [129, 4], [133, 4], [137, 84]]
					else:
						hashstringexists = True
						fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 16], [125, 4], [129, 4], [133, 4], [137, 4], [141, 4], [145, 76]]
					fileinfosize = 220
					prefetchmarkers.append("\n+8 Unknown (Empty values)\n")
					prefetchmarkers.append("\n+64 (8 * 8) Last run time(s)\nContains FILETIMEs, or 0 if not set\nThe first FILETIME is the most recent run time\n")
					prefetchmarkers.append("\n+16 Unknown\nMostly empty values but seem to get filled the run after the 8 last run times have been filled.\nCould be remnant values.\n")
					prefetchmarkers.append("\n+4 Run count\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x01, 0x02, 0x07\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x00, 0x03\n")
					if hashstringexists:
						prefetchmarkers.append("\n+4 Hash string offset\n")
						prefetchmarkers.append("\n+4 Hash string size\n")
						prefetchmarkers.append("\n+76 Unknown (Empty values)\n")
					else:
						prefetchmarkers.append("\n+84 Unknown (Empty values)\n")
				case "28010000":
					# Variant 2
					hashstringexists = True
					fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 8], [117, 4], [121, 4], [125, 4], [129, 4], [133, 4], [137, 76]]
					fileinfosize = 212
					prefetchmarkers.append("\n+8 Unknown (Empty values)\n")
					prefetchmarkers.append("\n+64 (8 * 8) Last run time(s)\nContains FILETIMEs, or 0 if not set\nThe first FILETIME is the most recent run time\n")
					prefetchmarkers.append("\n+8 Unknown\nMostly empty values but seem to get filled the run after the 8 last run times have been filled.\nCould be remnant values.\n")
					prefetchmarkers.append("\n+4 Run count\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x01\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x03\n")
					prefetchmarkers.append("\n+4 Hash string offset\n")
					prefetchmarkers.append("\n+4 Hash string size\n")
					prefetchmarkers.append("\n+76 Unknown (Empty values)\n")
			filemetricssize = numberoffilemetricsentries * 32
			filemetrics = [[1, filemetricssize]]
			prefetchmarkers.append("\n+{} File metrics array\n".format(filemetricssize))
			# filemetricsentrybytemask = [4, 4, 4, 4, 4, 4, 8]
			# filemetricsentry = generateEntriesFromByteMask(filemetricsentrybytemask, numberoffilemetricsentries * len(filemetricsentrybytemask))

			# prefetchmarkers.extend(sharedFileMetricsByVer232630)

			if hashstringexists:
				hashstringoffsetlocation = fileheadersize + fileinfosize - 76 - 4 - 4
				hashstringsizelocation = fileheadersize + fileinfosize - 76 - 4
				hashstringoffset = int(swapEndianness("".join(hexdata[b] for b in range(hashstringoffsetlocation, hashstringoffsetlocation+4)).upper()), 16)
				hashstringsize = int(swapEndianness("".join(hexdata[b] for b in range(hashstringsizelocation, hashstringsizelocation+4)).upper()), 16)

			tracechainssize = numberoftracechainsentries * 8
			tracechains = [[1, tracechainssize]]
			# tracechainsentrybytemask = [4, 1, 1, 2]
			# tracechainsentry = generateEntriesFromByteMask(tracechainsentrybytemask, numberoftracechainsentries * len(tracechainsentrybytemask))

			# prefetchmarkers.append("\nTotal block load count\nTotal number of blocks loaded (or fetched)\nThe block size 512k (512 * 1024) bytes\n")
			# prefetchmarkers.append("\nUnknown\nSeen: 0x02, 0x03, 0x04, 0x08, 0x0A\n")
			# prefetchmarkers.append("\nUnknown (Sample duration in ms?)\nSeen: 0x01\n")
			# prefetchmarkers.append("\nUnknown\nSeen: 0x0001, 0xFFFF\n")
			prefetchmarkers.append("\n+{} Trace chains array\n".format(tracechainssize))

	

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

	prefetchmarkers.append("\n+{} File name strings\n".format(filenamestringssize))
	if hashstringexists:
		prefetchmarkers.append("\n+{} Hash string\nApplication Prefetch > Path to executable responsible for the generated prefetch file.\nApplication Hosting Prefetch > Package name of hosted application.\n".format(hashstringsize))
	if hashstringorfilenamestringspaddingsize != 0:
		prefetchmarkers.append("\n+{} Padding\n".format(hashstringorfilenamestringspaddingsize))
	prefetchmarkers.append("\n+{} Volume information\n".format(volumesinformationsize))

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

	# print(prefetchtemplate)
	# print(prefetchsizes)
	templatedata = toAbsolute(prefetchtemplate, prefetchsizes)
	# print(templatedata)
	
	return formattedhexdata, formattedasciidata, templatedata, prefetchmarkers

# def generateEntriesFromByteMask(bytemask, loopcount):
# 	result = [[1, bytemask[0]]]
# 	for i in range(1, loopcount):
# 		previous = result[-1]  # Get the previous sublist
# 		index = previous[0] + previous[1]  # Generate the next index
# 		value = bytemask[i % len(bytemask)]  # Cyclically loop through the byte mask
# 		result.append([index, value])  # Append the new sublist to the result
# 	print(result)
# 	return result