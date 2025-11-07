from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pweok>£$m'

users = [
    {
        'user1': {'username': 'serdar', 'password': generate_password_hash('serdar123', salt_length=8)},
        'user2': {'username': 'ekin', 'password': generate_password_hash('ekin123', salt_length=8)}
     }
]

messages = []

#*(users[0]['user1']['username']) -> to check credentials

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == users[0]['user1']['username'] and check_password_hash(users[0]['user1']['password'], password):
            session['username'] = username
            return render_template('index.html', username=username)
        elif username == users[0]['user2']['username'] and check_password_hash(users[0]['user2']['password'], password):
            session['username'] = username
            return render_template('index.html', username=username)
        else:
            return 'Invalid credentials.', 401
    else:
        return render_template('login.html')
    
@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))
    
@app.get('/api/messages')
def get_messages():
    return {'messages': messages[-100:]}

@app.post("/api/send")
def api_send():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or request.form.get("message") or "").strip()
    user = session.get("username")
    if not text:
        return {"ok": False, "error": "empty"}, 400
    messages.append({"user": user, "text": text, 'time': datetime.now()})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)