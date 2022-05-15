from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')

from loader import *
from primer import *
import binascii
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import escape_markup

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
			asciidata = escape_markup(asciidata)
			pairlist = temp[3]
			# print("PAIRLIST: ", pairlist)

			for color in c:
				for pair in reversed(pairlist):
					hexdata = colorBytes(0, hexdata, c[color], pair[0], pair[1])
					asciidata = colorBytes(1, asciidata, c[color], pair[0], pair[1])
					del pairlist[-1]
					break

			self.ids.hex.text = hexdata
			self.ids.ascii.text =  asciidata.replace(" ", "")
			self.remove_widget(self.ids.openfile)		

class Veritas(App):
	def build(self):
		return MainApp()

if __name__ == '__main__':
	Veritas().run()