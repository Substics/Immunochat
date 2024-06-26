from flask import Flask, render_template
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.config['SECRET_KEY'] = 'theHairsOnCrimsonsComputer?'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app,
                debug=False,
                use_reloader=True,
                log_output=True,
                host='0.0.0.0',
                allow_unsafe_werkzeug=True)
