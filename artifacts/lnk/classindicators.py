classindicatormappings = {
	"1F": "Root Folder",
	**{format(i, 'X'): "Volume" for i in range(0x20, 0x30)},
	**{format(i, 'X'): "File Entry" for i in range(0x30, 0x40)},
	**{format(i, 'X'): "Network Location" for i in range(0x40, 0x50)},
	"61": "URI"
}