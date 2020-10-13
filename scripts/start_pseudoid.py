#!/usr/bin/env python3
import pseudoID
import socket
import webbrowser
from datetime import datetime, date
from pseudoID import config


_expiration_date_ = datetime(2020, 10, 31)

if date.today() < _expiration_date_.date():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    # url = IPAddr + "/pseudoID/generate"
    url = config.settings['BASE']['url'] + "/pseudoID/login"

    webbrowser.open(url, new=2)

    app = pseudoID.create_app()
    print("Test version valid for", (_expiration_date_.date() - date.today()).days, "days!")
    app.run()

else:
    print("Test version expired!")
