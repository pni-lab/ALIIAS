#!/usr/bin/env python3
import pseudoID
import socket
import webbrowser
from datetime import datetime, date

_expiration_date_ = datetime(2020, 9, 30)

if date.today() < _expiration_date_.date():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    # url = IPAddr + "/pseudoID/generate"
    url = "http://127.0.0.1:5000/" + "/pseudoID/generate"
    print(url)

    webbrowser.open(url, new=2)

    app = pseudoID.create_app()
    print("Test version valid for", (_expiration_date_.date() - date.today()).days, "days!")
    app.run()

else:
    print("Test version expired!")
