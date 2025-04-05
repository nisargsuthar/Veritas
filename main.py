import os, sys
from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.clock import Clock
from veritas import MyWidget

class MainPanel(TabbedPanel):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.background_color = (0, 0, 0, 1)
		self.do_default_tab = False
		self.my_tabs = []

		Window.bind(on_key_down=self._on_key_down)
		Window.bind(on_drop_file=self._on_file_drop)
		self.bind(current_tab=self._on_tab_switched)

		self.add_new_tab(prompt_open=False)
		
	def get_tab_by_filepath(self, file_path):
		for tab in self.my_tabs:
			viewer = getattr(tab, 'content', None)
			if hasattr(viewer, 'current_filepath') and viewer.current_filepath == file_path:
				return tab
		return None

	def open_file_from_widget(self, widget):
		file_path = widget.chooseFile()
		if file_path:
			existing_tab = self.get_tab_by_filepath(file_path)
			if existing_tab:
				self.switch_to(existing_tab)
			elif not getattr(widget, 'current_filepath', None):
				widget.openFile(file_path)
			else:
				self.add_new_tab(file_path=file_path)


	def _on_tab_switched(self, instance, tab):
		app = App.get_running_app()
		if not tab or not hasattr(tab, 'content'):
			app.title = "Veritas"
			return
		viewer = tab.content
		filepath = getattr(viewer, 'current_filepath', None)
		if filepath:
			app.title = f"Veritas - [{filepath}]"
		else:
			app.title = "Veritas"

	def _on_file_drop(self, window, file_path, x, y):
		file_path = file_path.decode("utf-8")
		print(f"Dropped file: {file_path}")
		current_viewer = getattr(self.current_tab, 'content', None)
		if current_viewer and not getattr(current_viewer, 'current_filepath', None):
			current_viewer.openFile(file_path)
		else:
			self.add_new_tab(file_path)


	def _on_key_down(self, window, key, scancode, codepoint, modifiers):
		if 'ctrl' in modifiers:
			if key == ord('o'):
				current_viewer = getattr(self.current_tab, 'content', None)
				selected_file = current_viewer.chooseFile() if current_viewer else None
				if selected_file:
					existing_tab = self.get_tab_by_filepath(selected_file)
					if existing_tab:
						self.switch_to(existing_tab)
					elif current_viewer and not getattr(current_viewer, 'current_filepath', None):
						current_viewer.openFile(selected_file)
					else:
						self.add_new_tab(file_path=selected_file)
			elif key == ord('w'):
				self.close_current_tab()
			elif key == 280:  # Ctrl + PageUp
				self.switch_tab(-1)
			elif key == 281:  # Ctrl + PageDown
				self.switch_tab(1)

	def switch_tab(self, direction):
		if not self.my_tabs:
			return
		try:
			index = self.my_tabs.index(self.current_tab)
		except ValueError:
			return
		new_index = (index + direction) % len(self.my_tabs)
		self.switch_to(self.my_tabs[new_index])

	def add_new_tab(self, file_path=None, prompt_open=True):
		if file_path:
			existing_tab = self.get_tab_by_filepath(file_path)
			if existing_tab:
				self.switch_to(existing_tab)
				return
		tab = TabbedPanelItem(text="New Tab")
		viewer = MyWidget()
		viewer._parent_tab = tab
		tab.content = viewer
		self.add_widget(tab)
		self.my_tabs.append(tab)

		def after_switch(_):
			self.switch_to(tab)
			current_viewer = getattr(self.current_tab, 'content', None)
			if current_viewer and hasattr(current_viewer, 'openFile') and file_path:
				current_viewer.openFile(file_path)
			elif current_viewer and hasattr(current_viewer, 'openFile') and prompt_open:
				current_viewer.openFile()
		Clock.schedule_once(after_switch, 0)

	def close_current_tab(self):
		current_viewer = getattr(self.current_tab, 'content', None)
		if current_viewer and hasattr(current_viewer, 'closeFile'):
			current_viewer.closeFile()

		tab_to_close = self.current_tab
		if not tab_to_close:
			return
		try:
			index = self.my_tabs.index(tab_to_close)
		except ValueError:
			return
		# Remove from panel and our custom list
		self.remove_widget(tab_to_close)
		self.my_tabs.remove(tab_to_close)
		# If there are no tabs left
		if not self.my_tabs:
			self.add_new_tab(prompt_open=False)
			return
		# Switch to tab on right if available, else go left
		if index < len(self.my_tabs):
			self.switch_to(self.my_tabs[index])  # tab on right
		else:
			self.switch_to(self.my_tabs[index - 1])  # tab on left

class VeritasApp(App):
	def build(self):
		self.icon = r'images\Veritas.png'
		return MainPanel()

if __name__ == '__main__':
	if hasattr(sys, '_MEIPASS'):
		resource_add_path(os.path.join(sys._MEIPASS))
	VeritasApp().run()
