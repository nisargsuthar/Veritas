import binascii
from offsetter import *

######################################################################
	# TODO: #
	#########
	# Write logic for marking dynamic data from template points.

def prefetchTemplate():
	prefetchbytes = []
	prefetchtemp = []
	prefetchsizes = []
	prefetchmarkers = []
	with open('decomp.pf', 'rb') as f:
		for byte in iter(lambda: f.read(1), b''):
			prefetchbytes.append(binascii.hexlify(byte).decode("utf-8"))
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
	
	sharedFileInfoByVar1AndVer26 = []
	sharedFileInfoByVar1AndVer26.append("\n+8 Unknown (Empty values)\n")
	sharedFileInfoByVar1AndVer26.append("\n+64 (8 * 8) Last run time(s)\nContains FILETIMEs, or 0 if not set\nThe first FILETIME is the most recent run time\n")
	sharedFileInfoByVar1AndVer26.append("\n+16 Unknown\nMostly empty values but seem to get filled the run after the 8 last run times have been filled.\nCould be remnant values.\n")
	sharedFileInfoByVar1AndVer26.append("\n+4 Run count\n")
	sharedFileInfoByVar1AndVer26.append("\n+4 Unknown\nSeen: 0x01, 0x02, 0x07\n")
	sharedFileInfoByVar1AndVer26.append("\n+4 Unknown\nSeen: 0x00, 0x03\n")
	sharedFileInfoByVar1AndVer26.append("\n+88 Unknown (Empty values)\n")

	sharedFileMetricsByVer232630 = []
	sharedFileMetricsByVer232630.append("\n+4 Unknown (Prefetch start time in ms?)\nCould be the index into the trace chain array as well, is this relationship implicit or explicit?\n")
	sharedFileMetricsByVer232630.append("\n+4 Unknown (Prefetch duration in ms?)\nCould be the number of entries in the trace chain as well, is this relationship implicit or explicit?\n")
	sharedFileMetricsByVer232630.append("\n+4 Unknown (Average prefetch duration in ms?)\n")
	sharedFileMetricsByVer232630.append("\n+4 Filename string offset\nThe offset is relative to the start of the filename strings\n")
	sharedFileMetricsByVer232630.append("\n+4 Filename string number of characters\nDoes not include the end-of-string character\n")
	sharedFileMetricsByVer232630.append("\n+4 Unknown (Flags?)\nSeen: 0x00000001, 0x00000002, 0x00000003, 0x00000200, 0x00000202\n")
	sharedFileMetricsByVer232630.append("\n+8 File reference\nContains a file reference of the file corresponding to the filename string or 0 if not set\nNTFS:\nFirst 6 bytes > MFT entry index\nLast 2 bytes > Sequence number\n")

	sharedTraceChainsByVer172326 = []
	sharedTraceChainsByVer172326.append("\nNext array entry index\nContains the next trace chain array entry index in the chain, where the first entry index starts with 0, or -1 (0xFFFFFFFF) for the end-of-chain.\n")
	sharedTraceChainsByVer172326.append("\nTotal block load count\nTotal number of blocks loaded (or fetched)\nThe block size 512k (512 * 1024) bytes\n")
	sharedTraceChainsByVer172326.append("\nUnknown\nSeen: 0x02, 0x03, 0x04, 0x08, 0x0A\n")
	sharedTraceChainsByVer172326.append("\nUnknown (Sample duration in ms?)\nSeen: 0x01\n")
	sharedTraceChainsByVer172326.append("\nUnknown\nSeen: 0x0001, 0xFFFF\n")

######################################################################
	# VERSION SPECIFIC. #
	#####################
	version = "".join(prefetchbytes[b] for b in range(4)).upper()
	match version:
		case "11000000":
			# Was XP or 2003 > PFV 17
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 16], [61, 4], [65, 4]]
			fileinfosize = 68
			prefetchmarkers.append("\n+8 Last run time\nContains a FILETIME\n")
			prefetchmarkers.append("\n+16 Unknown (Empty values)\nSometimes contains remnant data?\n")
			prefetchmarkers.append("\n+4 Run count\n")
			prefetchmarkers.append("\n+4 Unknown\n")
			
			filemetrics = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4]]
			filemetricssize = 20
			prefetchmarkers.append("\nUnknown (Prefetch start time in ms?)\nCould be the index into the trace chain array as well, is this relationship implicit or explicit?\n")
			prefetchmarkers.append("\nUnknown (Prefetch duration in ms?)\nCould be the number of entries in the trace chain as well, is this relationship implicit or explicit?\n")
			prefetchmarkers.append("\nFilename string offset\nThe offset is relative to the start of the filename strings\n")
			prefetchmarkers.append("\nFilename string number of characters\nDoes not include the end-of-string character\n")
			prefetchmarkers.append("\nUnknown (Flags?)\n")

			tracechains = [[1, 4], [5, 4], [9, 1], [10, 1], [11, 2]]
			tracechainssize = 12
			prefetchmarkers.extend(sharedTraceChainsByVer172326)

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

			filemetrics = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 8]]
			filemetricssize = 32
			prefetchmarkers.extend(sharedFileMetricsByVer232630)

			tracechains = [[1, 4], [5, 4], [9, 1], [10, 1], [11, 2]]
			tracechainssize = 12
			prefetchmarkers.extend(sharedTraceChainsByVer172326)


		case "1A000000":
			# Was 8.1 > PFV 26
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 8], [53, 56], [109, 16], [125, 4], [129, 4], [133, 4], [137, 88]]
			fileinfosize = 224
			prefetchmarkers.extend(sharedFileInfoByVar1AndVer26)
			
			filemetrics = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 8]]
			filemetricssize = 32
			prefetchmarkers.extend(sharedFileMetricsByVer232630)

			tracechains = [[1, 4], [5, 4], [9, 1], [10, 1], [11, 2]]
			tracechainssize = 12
			prefetchmarkers.extend(sharedTraceChainsByVer172326)


		case "1E000000":
			# Was 10 or 11 > PFV 30
			variant = "".join(prefetchbytes[b] for b in range(84, 88)).upper()
			match variant:
				case "30010000":
					# Variant 1
					fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 8], [53, 56], [109, 16], [125, 4], [129, 4], [133, 4], [137, 88]]
					fileinfosize = 224
					prefetchmarkers.extend(sharedFileInfoByVar1AndVer26)
				case "28010000":
					# Variant 2
					fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 8], [117, 4], [121, 4], [125, 4], [129, 88]]
					fileinfosize = 216
					prefetchmarkers.append("\n+8 Unknown (Empty values)\n")
					prefetchmarkers.append("\n+64 (8 * 8) Last run time(s)\nContains FILETIMEs, or 0 if not set\nThe first FILETIME is the most recent run time\n")
					prefetchmarkers.append("\n+8 Unknown\nMostly empty values but seem to get filled the run after the 8 last run times have been filled.\nCould be remnant values.\n")
					prefetchmarkers.append("\n+4 Run count\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x01\n")
					prefetchmarkers.append("\n+4 Unknown\nSeen: 0x03\n")
					prefetchmarkers.append("\n+88 Unknown (Empty values)\n")
			filemetrics = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 8]]
			filemetricssize = 32
			prefetchmarkers.extend(sharedFileMetricsByVer232630)

			tracechains = [[1, 4], [5, 1], [6, 1], [7, 2]]
			tracechainssize = 8
			prefetchmarkers.append("\nTotal block load count\nTotal number of blocks loaded (or fetched)\nThe block size 512k (512 * 1024) bytes\n")
			prefetchmarkers.append("\nUnknown\nSeen: 0x02, 0x03, 0x04, 0x08, 0x0A\n")
			prefetchmarkers.append("\nUnknown (Sample duration in ms?)\nSeen: 0x01\n")
			prefetchmarkers.append("\nUnknown\nSeen: 0x0001, 0xFFFF\n")

	# prefetchmarkers.append("\nFile name strings\n")
	prefetchtemp.append(fileheader)
	prefetchtemp.append(fileinfo)
	prefetchtemp.append(filemetrics)
	prefetchtemp.append(tracechains)
	
	prefetchsizes.append(fileheadersize)
	prefetchsizes.append(fileinfosize)
	prefetchsizes.append(filemetricssize)
	prefetchsizes.append(tracechainssize)

	absolute = toAbsolute(prefetchtemp, prefetchsizes)
	# print(absolute)
	filenamestringsoffset = "".join(prefetchbytes[b] for b in range(100, 104)).upper()
	filenamestringssize = "".join(prefetchbytes[b] for b in range(104, 108)).upper()

	filenamestringsoffset = int(swapEndianness(filenamestringsoffset), 16)
	filenamestringssize = int(swapEndianness(filenamestringssize), 16)
	# print(filenamestringsoffset, filenamestringssize)
	# absolute.append([filenamestringsoffset, filenamestringssize])

	return absolute, prefetchmarkers