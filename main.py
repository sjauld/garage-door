# main.py
from flask import Flask
import pigpio
import time
import authentication

pi = pigpio.pi()

app = Flask(__name__)

@app.route("/")
@authentication.requires_auth
def hello():
    pi.write(25,1)
    time.sleep(0.2)
    pi.write(25,0)
    return "Garage button pressed!"

if __name__ == "__main__":
    app.run()
