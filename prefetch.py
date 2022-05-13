import binascii

######################################################################################
	# TODO: #
	#########
	# SECTION C, D, E & F

def prefetch():
	prefetchbytes = []
	prefetchtemp = []
######################################################################################
	# COMMON SECTION. #
	###################
	fileheader = [(1, 4), (5, 4), (9, 4), (13, 4), (17, 60), (77, 4), (81, 4)]
	tracechains = [(1, 4), (5,  4), (9, 1), (10, 1), (11, 2)] # Same for PFVs 17, 23 and 26. If PFV 30 has changes, remove this list from the common section.
	with open('decomp.pf', 'rb') as f:
		for byte in iter(lambda: f.read(1), b''):
			prefetchbytes.append(binascii.hexlify(byte).decode("utf-8"))
######################################################################################
	# VERSION SPECIFIC. #
	#####################
	version = "".join(prefetchbytes[b] for b in range(4)).upper()
	match version:
		case "11000000":
			# Was XP or 2003 > PFV 17
			fileinfo = [(1, 4), (5, 4), (9, 4), (13, 4), (17, 4), (21, 4), (25, 4), (29, 4), (33, 4), (37, 8), (45, 16), (61, 4), (65, 4)]
			filemetrics = [(1, 4), (5, 4), (9, 4), (13, 4), (17, 4)]

		case "17000000":
			# Was Vista or 7 > PFV 23
			fileinfo = [(1, 4), (5, 4), (9, 4), (13, 4), (17, 4), (21, 4), (25, 4), (29, 4), (33, 4), (37, 8), (45 , 8), (53 , 16), (69 , 4), (73 , 4), (77 , 80)]
			filemetrics = [(1, 4), (5, 4), (9, 4), (13, 4), (17, 4), (21, 4), (25, 8)]
		case "1A000000":
			# Was 8.1 > PFV 26
			fileinfo = [(1, 4), (5, 4), (9, 4), (13, 4), (17, 4), (21, 4), (25, 4), (29, 4), (33, 4), (37, 8), (45, 8), (53, 56), (109, 16), (125, 4), (129, 4), (133, 4), (137, 88)]
			filemetrics = [(1, 4), (5, 4), (9, 4), (13, 4), (17, 4), (21, 4), (25, 8)]
		case "1E000000":
			# Was 10 or 11 > PFV 30
			fileinfo = []
			filemetrics = []
