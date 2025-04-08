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
from kivy.clock import Clock

class MyWidget(Widget):
	firstrv = ObjectProperty(None)
	secondrv = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(MyWidget, self).__init__(**kwargs)
		self.ids.offsetheader.disabled = True
		self.ids.offsetheader.opacity = 0

	def chooseFile(self):
		file_path = filechooser.open_file(multiple=True, filters=[["All files", "*.lnk", "*"]])
		if file_path:
			print(f"Selected files: {file_path}")  # Debugging
			return file_path
		return []

	def openFile(self, file_path):
		print(f"Selected file: {file_path}")  # Debugging
		bytecount = os.path.getsize(file_path)
		loader.loadFile(file_path, bytecount, self.updateRecycleViews)

	def updateRecycleViews(self, first_data, second_data, artifactsupported, file_path, byte_ranges=None):
		if artifactsupported:
			self.current_filepath = file_path
			self.byte_ranges = byte_ranges or []

			if hasattr(self, '_parent_tab'):
				filename = os.path.basename(file_path)
				short_name = (filename[:10] + '...') if len(filename) > 10 else filename
				self._parent_tab.text = short_name

			app = App.get_running_app()
			app.title = f"Veritas - [{file_path}]"

			self.ids.firstrv.data = first_data

			self.ids.secondrv.data = [
				{"text": m["text"], "index": i, "highlight": False}
				for i, m in enumerate(second_data)
			]

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

	def handle_marker_click(self, marker_index):
		if not self.byte_ranges or marker_index >= len(self.byte_ranges):
			return
		start_byte, end_byte = self.byte_ranges[marker_index]

		for i, row in enumerate(self.ids.firstrv.data):
			byte_offset = i * 16
			row["highlight"] = (byte_offset < end_byte - 1 and (byte_offset + 15) >= start_byte)
		
		for i, item in enumerate(self.ids.secondrv.data):
			item["highlight"] = (i == marker_index)

		self.ids.firstrv.refresh_from_data()
		self.ids.secondrv.refresh_from_data()

		def _scroll_to_highlighted_row(dt):
			rv = self.ids.firstrv
			highlighted_index = None
			for i, row in enumerate(rv.data):
				if row.get("highlight"):
					highlighted_index = i
					break
			if highlighted_index is None:
				return
			total_items = len(rv.data)
			scroll_position = 1.0 - (highlighted_index / max(1, total_items - 1))
			rv.scroll_y = max(0.0, min(1.0, scroll_position))
		Clock.schedule_once(_scroll_to_highlighted_row, 0)

	def closeFile(self):
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