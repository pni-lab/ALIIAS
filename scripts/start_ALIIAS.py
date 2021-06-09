#!/usr/bin/env python3
import ALIIAS
import socket
import webbrowser
from datetime import datetime, date
from ALIIAS import config

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
# url = IPAddr + "/pseudoID/generate"
url = config.settings['BASE']['url']  # + "/pseudoID/login"

app = ALIIAS.create_app()

webbrowser.open(url, new=2)

app.run()




