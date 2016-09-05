# main.py
from flask import Flask
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
@authentication.requires_auth
def hello():
    pi.write(25,1)
    time.sleep(0.2)
    pi.write(25,0)
    return "Garage button pressed!"

if __name__ == "__main__":
    app.run(host=os.environ["GARAGE_HOST"], port=os.environ["GARAGE_PORT"])
