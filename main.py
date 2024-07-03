from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config[
    'SECRET_KEY'] = 'your_secret_key'  # Replace with an appropriate secret key
socketio = SocketIO(app)

active_users = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@socketio.on('connect')
def handle_connect():
    username = request.args.get('username')
    if username:
        active_users[request.sid] = username
        emit('update_user_list', list(active_users.values()), broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in active_users:
        del active_users[request.sid]
        emit('update_user_list', list(active_users.values()), broadcast=True)


@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)


@socketio.on('private_message')
def handle_private_message(data):
    recipient_session_id = None
    for session_id, username in active_users.items():
        if username == data['recipient']:
            recipient_session_id = session_id
            break
    if recipient_session_id:
        emit('private_message', data['msg'], room=recipient_session_id)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
