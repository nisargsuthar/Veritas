def getLinkFlags(linkflagsbitstring):
	linkflagnames = ["HasLinkTargetIDList", "HasLinkInfo", "HasName", "HasRelativePath", "HasWorkingDir", "HasArguments", "HasIconLocation", "IsUnicode", "ForceNoLinkInfo", "HasExpString", "RunInSeparateProcess", "Unused1", "HasDarwinID", "RunAsUser", "HasExpIcon", "NoPidlAlias", "Unused2", "RunWithShimLayer", "ForceNoLinkTrack", "EnableTargetMetadata", "DisableLinkPathTracking", "DisableKnownFolderTracking", "DisableKnownFolderAlias", "AllowLinkToLink", "UnaliasOnSave", "PreferEnvironmentPath", "KeepLocalIDListForUNCTarget"]
	linkflags = {name: int(linkflagsbitstring[31 - i]) for i, name in enumerate(linkflagnames)}
	return linkflags

def getFileAttributeFlags(fileattributeflagsbitstring):
	fileattributeflagnames = ["FILE_ATTRIBUTE_READONLY", "FILE_ATTRIBUTE_HIDDEN", "FILE_ATTRIBUTE_SYSTEM", "Reserved1", "FILE_ATTRIBUTE_DIRECTORY", "FILE_ATTRIBUTE_ARCHIVE", "Reserved2", "FILE_ATTRIBUTE_NORMAL", "FILE_ATTRIBUTE_TEMPORARY", "FILE_ATTRIBUTE_SPARSE_FILE", "FILE_ATTRIBUTE_REPARSE_POINT", "FILE_ATTRIBUTE_COMPRESSED", "FILE_ATTRIBUTE_OFFLINE", "FILE_ATTRIBUTE_NOT_CONTENT_INDEXED", "FILE_ATTRIBUTE_ENCRYTED"]
	fileattributeflags = {name: int(fileattributeflagsbitstring[31 - i]) for i, name in enumerate(fileattributeflagnames)}
	return fileattributeflags

def getCommonNetworkRelativeLinkFlags(commonnetworkrelativelinkflagsbitstring):
	commonnetworkrelativelinkflagnames = ["ValidDevice", "ValidNetType"]
	commonnetworkrelativelinkflags = {name: int(commonnetworkrelativelinkflagsbitstring[31 - i]) for i, name in enumerate(commonnetworkrelativelinkflagnames)}
	return commonnetworkrelativelinkflags
