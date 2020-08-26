#!/usr/bin/env python3
import pseudoID
import socket
import webbrowser

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
# url = IPAddr + "/pseudoID/generate"
url = "http://127.0.0.1:5000/" + "/pseudoID/generate"
print(url)

webbrowser.open(url, new=2)

app = pseudoID.create_app()
app.run()