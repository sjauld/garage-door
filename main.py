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
    return "The server is UP!\n<a href='/pi'>Continue to the Pi</a>"

@app.route("/pi")
@authentication.requires_auth
def handler():
    pin = request.args.get('pin')
    action = request.args.get('action')
    mode = request.args.get('mode')
    if pin is None:
        return "Please select a pin", 400
    if action is None:
        return "Pin {} selected. <a href='/pi?pin={}&action=press'>Would you like to press this pin?</a>".format(pin, pin)
    elif action is 'press':
        if mode is None:
            return "Pin {} (fake) pressed!".format(pin)
        elif mode is 'realz':
            pi.write(int(pin),1)
            time.sleep(0.2)
            pi.write(int(pin),0)
            return "Pin {} pressed for realz!".format(pin)
        else:
            return "Bad mode selected", 400
    else:
        return "Bad action selected", 400

if __name__ == "__main__":
    app.run(host=os.environ["GARAGE_HOST"], port=os.environ["GARAGE_PORT"])
