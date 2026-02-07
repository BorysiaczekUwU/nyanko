from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot jest aktywny! I'm alive!"

def run():
    # Render wymaga nasłuchiwania na porcie 0.0.0.0
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()