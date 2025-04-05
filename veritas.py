import os, sys, webbrowser, loader
from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from plyer import filechooser
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.resources import resource_add_path

class MyWidget(Widget):
	firstrv = ObjectProperty(None)
	secondrv = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(MyWidget, self).__init__(**kwargs)
		self.ids.offsetheader.disabled = True
		self.ids.offsetheader.opacity = 0

	def chooseFile(self):
		file_path = filechooser.open_file(multiple=False, filters=[["All files", "*.lnk", "*"]])
		if file_path:
			print(f"Selected file: {file_path[0]}")  # Debugging
			return file_path[0]
		return None

	def openFile(self, file_path):
		print(f"Selected file: {file_path}")  # Debugging
		bytecount = os.path.getsize(file_path)
		loader.loadFile(file_path, bytecount, self.updateRecycleViews)

	def updateRecycleViews(self, first_data, second_data, artifactsupported, file_path):
		if artifactsupported:
			self.current_filepath = file_path
			if hasattr(self, '_parent_tab'):
				filename = os.path.basename(file_path)
				short_name = (filename[:10] + '...') if len(filename) > 10 else filename
				self._parent_tab.text = short_name

			app = App.get_running_app()
			app.title = f"Veritas - [{file_path}]"

			self.ids.firstrv.data = first_data
			self.ids.secondrv.data = second_data

			self.ids.openfile.opacity = 0
			self.ids.openfile.disabled = True

			self.ids.closefile.disabled = False
			self.ids.closefile.opacity = 1

			self.ids.offsetheader.disabled = False
			self.ids.offsetheader.opacity = 1
		else:
			content_label = Label(
				text='Artifact not supported yet!\n\n'
					 'Check supported artifacts [ref=supported_artifacts][u]here[/u][/ref].',
				font_size='24sp',
				markup=True,
				halign='center',
				valign='middle',
				on_ref_press=self.on_link_press
			)
			popup = Popup(
				title='Uh-oh',
				title_size='26sp',
				content=content_label,
				size_hint=(0.6, 0.3)
			)
			popup.open()

	def closeFile(self):
		print("File actually closed")
		app = App.get_running_app()
		app.title = "Veritas"
		self.current_filepath = ""

		if hasattr(self, '_parent_tab'):
			self._parent_tab.text = "New Tab"

		self.ids.firstrv.data = []
		self.ids.secondrv.data = []

		self.ids.closefile.disabled = True
		self.ids.closefile.opacity = 0

		self.ids.openfile.disabled = False
		self.ids.openfile.opacity = 1

		self.ids.offsetheader.disabled = True
		self.ids.offsetheader.opacity = 0

	def on_link_press(self, instance, ref):
		if ref == 'supported_artifacts':
			webbrowser.open('https://github.com/nisargsuthar/Veritas#supported-artifacts')

class Veritas(App):
	def build(self):
		self.icon = r'images\Veritas.png'
		return MyWidget()

if __name__ == '__main__':
	if hasattr(sys, '_MEIPASS'):
		resource_add_path(os.path.join(sys._MEIPASS))
	Veritas().run()