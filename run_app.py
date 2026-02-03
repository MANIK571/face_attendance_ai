import webbrowser
import threading
import logging
from app_flask import app

# 🔑 Enable logging to file
logging.basicConfig(
    filename="desktop_app_error.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s"
)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    try:
        threading.Timer(2, open_browser).start()
        app.run(host="127.0.0.1", port=5000, debug=False)
    except Exception as e:
        logging.exception("Fatal error starting Flask app")
