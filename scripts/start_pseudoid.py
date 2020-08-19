import flask
import sys

sys.path.append('C:\\Users\\rober\\PycharmProjects\\PseudoID_v2')
print(sys.path)
import pseudoID

app = pseudoID.create_app()
app.run()

print("Hello2PNI")
