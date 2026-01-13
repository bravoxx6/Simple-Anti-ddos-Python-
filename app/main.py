from flask import Flask
from app.ddos_guard import ddos_protection

app = Flask(__name__)
app.before_request(ddos_protection)

@app.route("/")
def index():
    return "Protected server 🛡"

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run() # REMOVE WHILE TESTING

