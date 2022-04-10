from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from ipaddress import ip_address
import socket

ip_main = "Enter IP"
port_main = "Enter Port"


class MyApp(App):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ip = ""
		self.port = ""
		self.main_btn = Button(text="Connect", size_hint=(.2, None),
							   on_press=self.connect_btn)

		self.ip_inp = TextInput(text=ip_main, multiline=False,
								size_hint=(.2, None))

		self.port_input = TextInput(text=port_main, multiline=False,
									size_hint=(.2, None))

		self.condition = Label(text="Not Connected", color=(0, 0, 0, 1),
							   size_hint=(.2, None))

		self.off_power_btn = Button(text="Turn off", size_hint=(.1, None))
		self.sleep_btn = Button(text="Sleep mode", size_hint=(.1, None))

	def build(self):
		Window.clearcolor = (1, 1, 1, 1)

		b = BoxLayout(orientation='vertical')

		gl = GridLayout(cols=1)

		gl.add_widget(self.ip_inp)
		gl.add_widget(self.port_input)

		gl.add_widget(self.main_btn)
		gl.add_widget(Widget(size_hint=(1.5, None)))
		gl.add_widget(self.condition)

		gl1 = GridLayout(cols=2)

		gl1.add_widget(self.off_power_btn)
		gl1.add_widget(self.sleep_btn)

		b.add_widget(gl); b.add_widget(gl1)

		return b

	def off_power(self, *args):
		self.client.send('off'.encode())

	def sleep_mode(self, *args):
		self.client.send('sleep'.encode())

	def connect_btn(self, value):
		self.condition.text = ""
		self.ip = self.ip_inp.text
		self.port = self.port_input.text
		try:
			ip_address(self.ip)
		except ValueError:
			self.ip_inp.text = "Incorrect IP!"
			self.ip = ''
		finally:
			try:
				self.port = int(self.port)
				if self.port > 65536 or 0 > self.port:
					raise ValueError()
				self.connect()
			except ValueError:
				self.port_input.text = "Incorrect Port!"
				self.port = ''

	def connect(self):
		try:
			self.client.connect((self.ip, self.port))
			self.condition.text = f'Connected {self.ip}'

			self.off_power_btn.bind(on_release=self.off_power)
			self.sleep_btn.bind(on_release=self.sleep_mode)

		except Exception:
			pass


if __name__ == "__main__":
	MyApp().run()
