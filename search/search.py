from flask import Flask
app = Flask(__name__)

@app.route("/")
def search():
  return "Found!"

if __name__ == "_main_":
  app.run()
