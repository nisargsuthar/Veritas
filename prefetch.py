import binascii
from offsetter import *

######################################################################################
	# TODO: #
	#########
	# SECTION C, D, E & F

def prefetchMarkers():
	prefetchmarkers = []
	prefetchmarkers.append("+4  Format version    \n17 > Windows XP, Windows 2003    \n23 > Windows Vista, Windows 7    \n26 > Windows 8.1    \n30 > Windows 10")
	prefetchmarkers.append("\n+4  Signature")
	prefetchmarkers.append("\n+4  Unknown\nSeen: 0x0000000f, 0x00000011")
	prefetchmarkers.append("\n+4  File size")
	prefetchmarkers.append("\n+60 Executable filename\nUTF-16 little-endian string with end-of-string character")
	prefetchmarkers.append("\n+4 Prefetch hash\nThis value should correspond with the hash in the Prefetch filename")
	prefetchmarkers.append("\n+4 Unknown (flags?)\n0x01 > is boot prefetch\n(Seen in: NTOSBOOT-B00DFAAD.pf, Op-EXPLORER.EXE-A80E4F97-000000F5.pf)")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")
	prefetchmarkers.append("\n============================================\n")

	return prefetchmarkers

def prefetchTemplate():
	prefetchbytes = []
	prefetchtemp = []
	prefetchsizes = []
	with open('decomp.pf', 'rb') as f:
		for byte in iter(lambda: f.read(1), b''):
			prefetchbytes.append(binascii.hexlify(byte).decode("utf-8"))
######################################################################################
	# COMMON SECTION. #
	###################
	fileheader = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 60], [77, 4], [81, 4]]
	fileheadersize = 84
######################################################################################
	# VERSION SPECIFIC. #
	#####################
	version = "".join(prefetchbytes[b] for b in range(4)).upper()
	match version:
		case "11000000":
			# Was XP or 2003 > PFV 17
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 16], [61, 4], [65, 4]]
			fileinfosize = 68
			filemetrics = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4]]
			filemetricssize = 20
			tracechains = [[1, 4], [5, 4], [9, 1], [10, 1], [11, 2]]
			tracechainssize = 12
			# volinfo = 

		case "17000000":
			# Was Vista or 7 > PFV 23
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 8], [53, 16], [69, 4], [73, 4], [77, 80]]
			fileinfosize = 156
			filemetrics = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 8]]
			filemetricssize = 32
			tracechains = [[1, 4], [5, 4], [9, 1], [10, 1], [11, 2]]
			tracechainssize = 12

		case "1A000000":
			# Was 8.1 > PFV 26
			fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 8], [53, 56], [109, 16], [125, 4], [129, 4], [133, 4], [137, 88]]
			fileinfosize = 224
			filemetrics = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 8]]
			filemetricssize = 32
			tracechains = [[1, 4], [5, 4], [9, 1], [10, 1], [11, 2]]
			tracechainssize = 12

		case "1E000000":
			# Was 10 or 11 > PFV 30
			variant = "".join(prefetchbytes[b] for b in range(84, 88)).upper()
			match variant:
				case "30010000":
					# Variant 1
					fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 8], [53, 56], [109, 16], [125, 4], [129, 4], [133, 4], [137, 88]]
					fileinfosize = 224
				case "28010000":
					# Variant 2
					fileinfo = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 4], [29, 4], [33, 4], [37, 8], [45, 64], [109, 8], [117, 4], [121, 4], [125, 4], [129, 88]]
					fileinfosize = 216
			filemetrics = [[1, 4], [5, 4], [9, 4], [13, 4], [17, 4], [21, 4], [25, 8]]
			filemetricssize = 32
			tracechains = [[1, 4], [5, 1], [6, 1], [7, 2]]
			tracechainssize = 8

	prefetchtemp.append(fileheader)
	prefetchtemp.append(fileinfo)
	prefetchtemp.append(filemetrics)
	prefetchtemp.append(tracechains)
	
	prefetchsizes.append(fileheadersize)
	prefetchsizes.append(fileinfosize)
	prefetchsizes.append(filemetricssize)
	prefetchsizes.append(tracechainssize)

	return toAbsolute(prefetchtemp, prefetchsizes)