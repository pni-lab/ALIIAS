#!/usr/bin/env python3
import pseudoID
import socket
import webbrowser

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
url = IPAddr + "/pseudoID/generate"
print(url)

webbrowser.open(url, new=2)

app = pseudoID.create_app()
app.run()