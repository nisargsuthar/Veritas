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
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class MyWidget(Widget):
	firstrv = ObjectProperty(None)
	secondrv = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(MyWidget, self).__init__(**kwargs)

	def openFile(self):
		self.file_chooser = FileChooserListView(path='.')
		popup = Popup(title='Choose a file', content=self.file_chooser, size_hint=(0.9, 0.9))
		self.file_chooser.bind(on_submit=lambda instance, value, *args: self.loadFileCallback(value[0], popup))
		popup.open()

	def loadFileCallback(self, file_path, popup):
		if file_path:
			loader.loadData(file_path, self.updateRecycleViews, popup)

	def updateRecycleViews(self, first_data, second_data, artifactsupported, file_path, popup):
		if artifactsupported:
			app = App.get_running_app()
			app.title = "Veritas - [{}]".format(file_path)

			self.ids.firstrv.data = first_data
			self.ids.secondrv.data = second_data

			# self.ids.openfile.size_hint_x = 0
			self.ids.openfile.opacity = 0
			self.ids.openfile.disabled = True

			self.ids.closefile.disabled = False
			# self.ids.closefile.size_hint_x = 1
			self.ids.closefile.opacity = 1
			popup.dismiss()			
		else:
			content_label = Label(
				text='Artifact not supported yet!\n\n'
					 'Check [ref=supported_artifacts][u]supported artifacts[/u][/ref] here.',
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
		app = App.get_running_app()
		app.title = "Veritas"
		self.ids.firstrv.data = []
		self.ids.secondrv.data = []

		self.ids.closefile.disabled = True
		self.ids.closefile.opacity = 0
		# self.ids.closefile.size_hint_x = 0

		self.ids.openfile.disabled = False
		self.ids.openfile.opacity = 1
		# self.ids.openfile.size_hint_x = 1

	def on_link_press(self, instance, ref):
		if ref == 'supported_artifacts':
			webbrowser.open('https://github.com/nisargsuthar/VeritasHexViewer#supported-artifacts')

class Veritas(App):
	def build(self):
		self.icon = r'images\Veritas.png'
		return MyWidget()

if __name__ == '__main__':
	Veritas().run()
