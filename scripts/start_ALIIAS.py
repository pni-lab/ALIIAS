#!/usr/bin/env python3
import pseudoID
import socket
import webbrowser
from datetime import datetime, date
from pseudoID import config

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
# url = IPAddr + "/pseudoID/generate"
url = config.settings['BASE']['url']  # + "/pseudoID/login"

app = pseudoID.create_app()

webbrowser.open(url, new=2)

app.run()




