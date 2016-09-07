# main.py
from flask import Flask
from flask import request
import pigpio
import time
import authentication
import os

try:
   os.environ["GARAGE_HOST"]
except KeyError:
   print "Please set the environment variable GARAGE_HOST"
   sys.exit(1)

try:
    os.environ["GARAGE_PORT"]
except KeyError:
    print "Please set the environment variable GARAGE_PORT"
    sys.exit(1)

pi = pigpio.pi()

app = Flask(__name__)

@app.route("/")
def status():
    return "The server is UP!"

@app.route("/press")
@authentication.requires_auth
def actuate():
    pin = request.args.get('pin')
    if pin is None:
        return "Please provide a pin", 400
    pi.write(pin,1)
    time.sleep(0.2)
    pi.write(pin,0)
    return "Garage button pressed!"

if __name__ == "__main__":
    app.run(host=os.environ["GARAGE_HOST"], port=os.environ["GARAGE_PORT"])
