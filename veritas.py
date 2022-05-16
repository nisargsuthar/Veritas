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
		temp = tempLoader()
		if not temp[0]:
			print("Artifact not found in the current database!")
			# TODO: Add kivy popup.
		else:
			hexdata = temp[1]
			asciidata = temp[2]
			markerdata = temp[3]
			pairlist = temp[4]
			asciidata = escapeMarkup(asciidata)
			newmarkerdata = []

			for color in c:
				for pair in reversed(pairlist):
					hexdata = colorBytes(hexdata, c[color], pair[0] - 1, pair[1] + 1)
					asciidata = colorBytes(asciidata, c[color], pair[0] - 1, pair[1] + 1)
					# markerlist.append(pairlist[-1])
					del pairlist[-1]
					break

			print(newmarkerdata)

			self.ids.hex.text = listToString(hexdata)
			self.ids.ascii.text = listToString(asciidata)
			self.ids.markers.text = listToString(newmarkerdata)
			self.remove_widget(self.ids.openfile)

class Veritas(App):
	def build(self):
		return MainApp()

if __name__ == '__main__':
	Veritas().run()