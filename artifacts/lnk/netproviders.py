def getNetVendor(networkprovidertype):
	vendorname = ""
	if networkprovidertype == 0x00000000:
		vendorname = "WNNC_NET_NONE"
	elif networkprovidertype == 0x00000002:
		vendorname = "WNNC_NET_TYPE"
	elif networkprovidertype == 0x00010000:
		vendorname = "WNNC_NET_MSNET"
	elif networkprovidertype == 0x00020000:
		vendorname = "WNNC_NET_SMB/WNNC_NET_LANMAN"
	elif networkprovidertype == 0x00030000:
		vendorname = "WNNC_NET_NETWARE"
	elif networkprovidertype == 0x00040000:
		vendorname = "WNNC_NET_VINES"
	elif networkprovidertype == 0x00050000:
		vendorname = "WNNC_NET_10NET"
	elif networkprovidertype == 0x00060000:
		vendorname = "WNNC_NET_LOCUS"
	elif networkprovidertype == 0x00070000:
		vendorname = "WNNC_NET_SUN_PC_NFS"
	elif networkprovidertype == 0x00080000:
		vendorname = "WNNC_NET_LANSTEP"
	elif networkprovidertype == 0x00090000:
		vendorname = "WNNC_NET_9TILES"
	elif networkprovidertype == 0x000A0000:
		vendorname = "WNNC_NET_LANTASTIC"
	elif networkprovidertype == 0x000B0000:
		vendorname = "WNNC_NET_AS400"
	elif networkprovidertype == 0x000C0000:
		vendorname = "WNNC_NET_FTP_NFS"
	elif networkprovidertype == 0x000D0000:
		vendorname = "WNNC_NET_PATHWORKS"
	elif networkprovidertype == 0x000E0000:
		vendorname = "WNNC_NET_LIFENET"
	elif networkprovidertype == 0x000F0000:
		vendorname = "WNNC_NET_POWERLAN"
	elif networkprovidertype == 0x00100000:
		vendorname = "WNNC_NET_BWNFS"
	elif networkprovidertype == 0x00110000:
		vendorname = "WNNC_NET_COGENT"
	elif networkprovidertype == 0x00120000:
		vendorname = "WNNC_NET_FARALLON"
	elif networkprovidertype == 0x00130000:
		vendorname = "WNNC_NET_APPLETALK"
	elif networkprovidertype == 0x00140000:
		vendorname = "WNNC_NET_INTERGRAPH"
	elif networkprovidertype == 0x00150000:
		vendorname = "WNNC_NET_SYMFONET"
	elif networkprovidertype == 0x00160000:
		vendorname = "WNNC_NET_CLEARCASE"
	elif networkprovidertype == 0x00170000:
		vendorname = "WNNC_NET_FRONTIER"
	elif networkprovidertype == 0x00180000:
		vendorname = "WNNC_NET_BMC"
	elif networkprovidertype == 0x00190000:
		vendorname = "WNNC_NET_DCE"
	elif networkprovidertype == 0x001A0000:
		vendorname = "WNNC_NET_AVID"
	elif networkprovidertype == 0x001B0000:
		vendorname = "WNNC_NET_DOCUSPACE"
	elif networkprovidertype == 0x001C0000:
		vendorname = "WNNC_NET_MANGOSOFT"
	elif networkprovidertype == 0x001D0000:
		vendorname = "WNNC_NET_SERNET"
	elif networkprovidertype == 0X001E0000:
		vendorname = "WNNC_NET_RIVERFRONT1"
	elif networkprovidertype == 0x001F0000:
		vendorname = "WNNC_NET_RIVERFRONT2"
	elif networkprovidertype == 0x00200000:
		vendorname = "WNNC_NET_DECORB"
	elif networkprovidertype == 0x00210000:
		vendorname = "WNNC_NET_PROTSTOR"
	elif networkprovidertype == 0x00220000:
		vendorname = "WNNC_NET_FJ_REDIR"
	elif networkprovidertype == 0x00230000:
		vendorname = "WNNC_NET_DISTINCT"
	elif networkprovidertype == 0x00240000:
		vendorname = "WNNC_NET_TWINS"
	elif networkprovidertype == 0x00250000:
		vendorname = "WNNC_NET_RDR2SAMPLE"
	elif networkprovidertype == 0x00260000:
		vendorname = "WNNC_NET_CSC"
	elif networkprovidertype == 0x00270000:
		vendorname = "WNNC_NET_3IN1"
	elif networkprovidertype == 0x00290000:
		vendorname = "WNNC_NET_EXTENDNET"
	elif networkprovidertype == 0x002A0000:
		vendorname = "WNNC_NET_STAC"
	elif networkprovidertype == 0x002B0000:
		vendorname = "WNNC_NET_FOXBAT"
	elif networkprovidertype == 0x002C0000:
		vendorname = "WNNC_NET_YAHOO"
	elif networkprovidertype == 0x002D0000:
		vendorname = "WNNC_NET_EXIFS"
	elif networkprovidertype == 0x002E0000:
		vendorname = "WNNC_NET_DAV"
	elif networkprovidertype == 0x002F0000:
		vendorname = "WNNC_NET_KNOWARE"
	elif networkprovidertype == 0x00300000:
		vendorname = "WNNC_NET_OBJECT_DIRE"
	elif networkprovidertype == 0x00310000:
		vendorname = "WNNC_NET_MASFAX"
	elif networkprovidertype == 0x00320000:
		vendorname = "WNNC_NET_HOB_NFS"
	elif networkprovidertype == 0x00330000:
		vendorname = "WNNC_NET_SHIVA"
	elif networkprovidertype == 0x00340000:
		vendorname = "WNNC_NET_IBMAL"
	elif networkprovidertype == 0x00350000:
		vendorname = "WNNC_NET_LOCK"
	elif networkprovidertype == 0x00360000:
		vendorname = "WNNC_NET_TERMSRV"
	elif networkprovidertype == 0x00370000:
		vendorname = "WNNC_NET_SRT"
	elif networkprovidertype == 0x00380000:
		vendorname = "WNNC_NET_QUINCY"
	elif networkprovidertype == 0x00390000:
		vendorname = "WNNC_NET_OPENAFS"
	elif networkprovidertype == 0X003A0000:
		vendorname = "WNNC_NET_AVID1"
	elif networkprovidertype == 0x003B0000:
		vendorname = "WNNC_NET_DFS"
	elif networkprovidertype == 0x003C0000:
		vendorname = "WNNC_NET_KWNP"
	elif networkprovidertype == 0x003D0000:
		vendorname = "WNNC_NET_ZENWORKS"
	elif networkprovidertype == 0x003E0000:
		vendorname = "WNNC_NET_DRIVEONWEB"
	elif networkprovidertype == 0x003F0000:
		vendorname = "WNNC_NET_VMWARE"
	elif networkprovidertype == 0x00400000:
		vendorname = "WNNC_NET_RSFX"
	elif networkprovidertype == 0x00410000:
		vendorname = "WNNC_NET_MFILES"
	elif networkprovidertype == 0x00420000:
		vendorname = "WNNC_NET_MS_NFS"
	elif networkprovidertype == 0x00430000:
		vendorname = "WNNC_NET_GOOGLE"
	elif networkprovidertype == 0x00440000:
		vendorname = "WNNC_NET_NDFS"
	elif networkprovidertype == 0x00450000:
		vendorname = "WNNC_NET_DOCUSHARE"
	elif networkprovidertype == 0x00460000:
		vendorname = "WNNC_NET_AURISTOR_FS"
	elif networkprovidertype == 0x00470000:
		vendorname = "WNNC_NET_SECUREAGENT"
	elif networkprovidertype == 0x00480000:
		vendorname = "WNNC_NET_9P"
	else:
		vendorname = "UNKNOWN_VENDOR"

	return vendorname