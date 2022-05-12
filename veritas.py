from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')

from colors import *
from checkTemplate import *
import binascii
import kivy
from kivy.app import App
from kivy.uix.widget import Widget

class MainApp(Widget):
	def openFile(self):
		hexdata = ""
		asciidata = ""
		bytecount = 0

		def colorBytes(view, data, col, pos, howmany):
			# Function to insert color markup in final string.
			ogpos = pos
			oghowmany = howmany
			print("HOWMANY: ", howmany)

			if view == 0:
				pos = (pos-1)*3
				data = data[:pos] + col + data[pos:]
				# To seek past "[color=xxxxxx]".
				pos += 14
				# To seek past the bytes colored.
				if howmany % 16 == 0:
					howmany = (howmany-1)*3
				else:
					howmany = (howmany-1)*3+2
				newlinecount = data.count("\n", pos, pos+howmany)
				print("NEWLINE: ", newlinecount)
				for seek in range(howmany):
					pos += 1
				for newline in range(newlinecount):
					pos+=1
				data = data[:pos] + cc + data[pos:]
			else:
				pos -= 1
				data = data[:pos] + col + data[pos:]
				# To seek past "[color=xxxxxx]".
				pos+=14
				newlinecount = data.count("\n", pos, pos+howmany)
				print("NEWLINE: ", newlinecount)
				for seek in range(howmany):
					pos += 1
				for newline in range(newlinecount):
					pos+=1
				data = data[:pos] + cc + data[pos:]
			print(data)
			return data

		with open('test.txt', 'rb') as f:
			for byte in iter(lambda: f.read(1), b''):
				bytecount += 1
				asciichar = int.from_bytes(byte, "big")
				hexdata += binascii.hexlify(byte).decode("utf-8")+" "

				if asciichar >= 32 and asciichar <= 126:
					asciidata += chr(asciichar)
				else:
					asciidata += "."

				if bytecount % 16 == 0:
					hexdata = hexdata[:-1]
					hexdata += "\n"
					asciidata += "\n"

		if not checkTemp():
			print("Artifact not found in the current database!")
			#TODO: Add kivy popup.
			
		hexdata = colorBytes(0, hexdata, c["red"], 6, 32)
		asciidata = colorBytes(1, asciidata, c["red"], 6, 32)
		
		self.ids.hex.text = hexdata
		self.ids.ascii.text = asciidata

class Veritas(App):
	def build(self):
		return MainApp()

if __name__ == '__main__':
	Veritas().run()