from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return " \n \n \n  New Upates are released!! \n \n " \
    "This is version 2.1" 

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0")
