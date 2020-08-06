import flask
import pseudoID

app = pseudoID.create_app()
app.run()

print("Hello2PNI")