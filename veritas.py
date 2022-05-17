from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from loader import *
from primer import *
import binascii
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
######################################################################################
	# TODO: #
	#########
	# Decode for extended ASCII set.
	# Add a HEX calculator.
	# Implement FileChooser.
	# Replace ScrollView with RecycleView.
	# Implement Tabs.

class MainApp(Widget):
	def openFile(self):
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

			self.ids.hex.text = listToString(hexdata)
			self.ids.ascii.text = listToString(asciidata)
			self.ids.markers.text = listToString(markerdata)
			self.remove_widget(self.ids.openfile)

class Veritas(App):
	def build(self):
		return MainApp()

if __name__ == '__main__':
	Veritas().run()