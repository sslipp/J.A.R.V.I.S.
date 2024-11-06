from flask import Flask, render_template
import threading
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def run_server():
    app.run(debug=True, use_reloader=False)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Thread(target=run_server).start()
    open_browser()
