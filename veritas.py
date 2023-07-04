from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from loader import *
from primer import *
import binascii
import kivy
import webbrowser
import loader
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder

class MyWidget(Widget):
	firstrv = ObjectProperty(None)
	secondrv = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(MyWidget, self).__init__(**kwargs)

	def openFile(self):
		self.file_chooser = FileChooserIconView(path='.')
		popup = Popup(title='Choose a file', content=self.file_chooser, size_hint=(0.9, 0.9))
		self.file_chooser.bind(on_submit=lambda instance, value, *args: self.loadFileCallback(value[0], popup))
		popup.open()

	def loadFileCallback(self, file_path, popup):
		if file_path:
			loader.load_data(file_path, self.updateRecycleViews, popup)

	def updateRecycleViews(self, first_data, second_data, artifactsupported, popup):
		if artifactsupported:
			print("Callback flag is True")
			self.ids.firstrv.data = first_data
			self.ids.secondrv.data = second_data
			self.ids.closefile.disabled = False
			self.ids.closefile.opacity = 1
			self.ids.openfile.disabled = True
			self.ids.openfile.opacity = 0
			popup.dismiss()
		else:
			content_label = Label(
				text='Artifact not supported yet!\n\n'
					 'Check [ref=more_info][u]supported artifacts[/u][/ref] here.',
				font_size='24sp',
				markup=True,
				halign='center',
				valign='middle',
				on_ref_press=self.on_link_press
			)
			popup = Popup(
				title='Error',
				title_size='26sp',
				content=content_label,
				size_hint=(0.6, 0.3)
			)
			popup.open()

	def closeFile(self):
		self.ids.firstrv.data = []
		self.ids.secondrv.data = []
		self.ids.closefile.disabled = True
		self.ids.closefile.opacity = 0
		self.ids.openfile.disabled = False
		self.ids.openfile.opacity = 1

	def on_link_press(self, instance, ref):
		if ref == 'more_info':
			# Handle the link click
			print("Opening more information...")
			webbrowser.open('https://github.com/nisargsuthar/VeritasHexViewer#supported-artifacts')

class Veritas(App):
	def build(self):
		return MyWidget()

if __name__ == '__main__':
	Veritas().run()
