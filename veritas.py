from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from loader import *
from primer import *
import binascii
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
#######################################################################
	# TODO: #
	#########
	# Decode for extended ASCII set.
	# Add a HEX calculator.
	# Implement FileChooser.
	# Implement Tabs.
class MyWidget(Widget):
	firstrv = ObjectProperty(None)
	secondrv = ObjectProperty(None)

	def openFile(self):
		app = App.get_running_app()
		loader = tempLoader()
		if not loader[0]:
			print("Artifact not found in the current database!")
			# TODO: Add kivy popup.
		else:
			hexdata = loader[1]
			asciidata = loader[2]
			markerdata = loader[3]
			markerdatasize = len(markerdata)
			templist = loader[4]
			asciidata = escapeMarkup(asciidata)
			savecolor = []
			for color in c:
				for pair in reversed(templist):
					hexdata = colorBytes(hexdata, c[color], pair[0] - 1, pair[1] + 1)
					asciidata = colorBytes(asciidata, c[color], pair[0] - 1, pair[1] + 1)
					savecolor.append(color)
					del templist[-1]
					break
			savecolor = reversed(savecolor)
			i = 0
			for color in savecolor:
				while i < (markerdatasize-1)*3+2:
					markerdata = colorBytes(markerdata, c[color], i, 2)
					i += 3
					break
			hexdata = [s.upper()+" " if len(s) == 2 else s for s in hexdata]

			hexdata = listToString(hexdata)
			asciidata = listToString(asciidata)
			markerdata = listToString(markerdata)

			hexdata = fixHex(hexdata)
			asciidata = fixAscii(asciidata)
			# print(hexdata)
			print(asciidata)

			def joinHexAscii(hexd, asciid):
				return {"hextext": hexd, "asciitext": asciid}
			
			first = []
			for h, a in zip(hexdata.split("\n"), asciidata.split("\n")):
				first.append(joinHexAscii(h, a))
			second = [{"text": "{}".format(line)} for line in markerdata.split("\t")]
			# print(first)
			# print(second)

			self.ids.firstrv.data = first
			self.ids.secondrv.data = second
			self.remove_widget(self.ids.openfile)

class Veritas(App):
	def build(self):
		return MyWidget()

if __name__ == '__main__':
	Veritas().run()