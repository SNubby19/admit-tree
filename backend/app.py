from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Hello from Flask via uv!</p>"

if __name__ == "__main__":
    app.run()
