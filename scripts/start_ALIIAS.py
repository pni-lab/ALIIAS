#!/usr/bin/env python3
import ALIIAS
import socket
import webbrowser
from ALIIAS import config

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

url = config.settings['BASE']['url']

app = ALIIAS.create_app()

webbrowser.open(url, new=2)

app.run()




