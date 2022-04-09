from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.config import Config
import threading
import socket
import os
import json

Config.set = ('graphics', 'resizable', '0')
Config.set = ('kivy', 'exit_on_escape', '0')


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with open('settings.json', 'r') as conf:
            data = json.load(conf)
            self.port = data['port']

            if isinstance(data['host'], list):
                self.ip = 'change in settings.config'

            else:
                self.ip = data['host']

                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                self.server.bind((self.ip, self.port))
                self.server.listen()

        self.user = None
        self.address = None

        self.check_connection_thread = threading.Thread(target=self.check_connection)
        self.check_connection_thread.start()

        self.condition = Label(text="Not Сonnected", color=(0, 0, 0, 1), font_size='12dp')
        self.ip_label = Label(text=f"IP: {self.ip}", color=(0, 0, 0, 1), font_size='12dp')
        self.port_label = Label(text=f"Port: {self.port}", color=(0, 0, 0, 1), font_size='12dp')

    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (400, 300)
        gl = GridLayout(cols=2)
        b = BoxLayout(orientation='vertical')
        b.add_widget(self.condition)
        gl.add_widget(self.ip_label)
        gl.add_widget(self.port_label)
        b.add_widget(gl)

        return b

    def check_connection(self, *args):
        user, address = self.server.accept()
        self.condition.text = f'Connected: {address}'
        while True:
            data = user.recv(2048).decode()
            if data == 'off':
                os.system('shutdown -s')
            elif data == 'sleep':
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')


    def on_request_close(self, *args):
        os._exit(0)


if __name__ == "__main__":
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w') as conf:
            data = {
                'host':
                    socket.gethostbyname_ex(socket.gethostname())[2],
                'port':
                    1255
            }

            json.dump(data, conf)

    MyApp().run()
