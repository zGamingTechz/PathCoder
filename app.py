from flask import Flask, render_template, request, redirect, session, url_for, jsonify, Response, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
from sqlalchemy import desc
from threading import Thread
from main import ai_response, chatbot_response
from quote import get_random_tip_or_quote
from resources import return_resources
import requests
import keys
import subprocess
import random


# Definitions
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SECRET_KEY'] = keys.secret_key
db = SQLAlchemy(app)
url = "https://zenquotes.io/api/random"


# Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = keys.email
app.config['MAIL_PASSWORD'] = keys.email_pass

mail = Mail(app)


# ToDo database
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


# Chats database
class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    course = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.message


# Chatbot Messages database
class Chatbot_Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    message = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.message


# User database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    quote = db.Column(db.String, default=requests.get(url).json()[0]['q'])
    language = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.id}:\n{self.name}\n{self.email}\n{self.password}\n{self.quote}\n{self.language}\n{self.experience}\n{self.score}>'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = ToDo(content=task_content, email=session['user_email'])

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error in adding task"
    else:
        if 'logged_in' in session and session['logged_in']:
            user = User.query.filter(User.email == session['user_email']).first()
            tasks = ToDo.query.filter(ToDo.email == session['user_email']).order_by(ToDo.id).all()
            resources = return_resources(user.path)
            return render_template('home.html', user=user, tasks=tasks, resources=resources)
        elif 'answered' in session and not session['answered']:
            return redirect(url_for('questions'))
        return redirect(url_for('register'))


@app.route('/certification')
def get_certification():
    tasks = ToDo.query.filter(ToDo.email == session['user_email']).order_by(ToDo.id).all()
    if (len(tasks) < 1):
        return send_file("static/certificate.pdf", as_attachment=True)


@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data["email"]

    otp = str(random.randint(100000, 999999))
    session['otp'] = otp

    msg = Message('Your OTP Code', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is {otp}. It is valid for 5 minutes.'
    mail.send(msg)

    return jsonify(otp)


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    user = User.query.filter(User.email == session['user_email']).first()

    if request.method == "POST":
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        q6 = request.form['q6']
        q7 = request.form['q7']
        q8 = request.form['q8']
        q9 = request.form['q9']

        global Qs
        Qs = [q1, q2, q3, q4, q5, q6, q7, q8, q9]
        return redirect('/loading')
    else:
        return render_template('questions.html', user=user)


@app.route('/loading', methods=['GET', 'POST'])
def loading():
    quote = get_random_tip_or_quote()
    return render_template('loading.html', quote=quote)


@app.route('/fetch_tasks', methods=['GET', 'POST'])
def fetch_tasks():
    user = User.query.filter(User.email == session['user_email']).first()
    tasks = ai_response(Qs, user.language, user.path, user.experience)

    for task in tasks:
        new_task = ToDo(content=task, email=session['user_email'])

        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return "Error in adding task"

    session['logged_in'] = True
    session['answered'] = True
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        check = User.query.filter(User.email == email).first()
        if check is not None:
            if check.password == password:
                session['logged_in'] = True
                session['user_email'] = check.email
                return redirect('/')
            else:
                return render_template("login.html", error='Incorrect password')
        else:
            return render_template("login.html", error='User not found')
    return render_template("login.html", error='')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        otp = request.form['otp']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        language = request.form['language']
        path = request.form['path']
        experience = request.form['experience']

        existing_user = User.query.filter(User.email == email).first()
        if existing_user is None:
            if otp == session['otp']:
                new_user = User(
                    name=name,
                    email=email,
                    password=password,
                    language=language,
                    path=path,
                    experience=experience
                )

                if password != confirm_password:
                    return render_template("register.html")

                try:
                    db.session.add(new_user)
                    db.session.commit()
                    session['answered'] = False
                    session['user_email'] = email
                    return redirect('/questions')
                except Exception as e:
                    return f"Error in adding user: {str(e)}"
            else:
                return render_template("register.html", error='Incorrect OTP')
        else:
            return render_template("register.html", error='Email already in use')
    else:
        return render_template("register.html")


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)
    user = User.query.filter(User.email == session['user_email']).first()

    try:
        db.session.delete(task_to_delete)
        user.score += 100
        db.session.commit()
        return redirect('/')
    except:
        return "Failed to delete"


@app.route('/update/<int:id>', methods=["GET", 'POST'])
def update(id):
    task_to_update = ToDo.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            "Failed to update"
    else:
        return render_template('update.html', task=task_to_update)


@app.route('/logout')
def logout():
    session["logged_in"] = False
    session['answered'] = True

    return redirect('/login')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if request.method == "POST":
        user = User.query.filter(User.email == session['user_email']).first()
        new_message = Chats(
            email=session['user_email'],
            name=user.name,
            course=user.path,
            message=request.form['message']
        )

        try:
            db.session.add(new_message)
            user.score += 10
            db.session.commit()
            return redirect('/chatroom')
        except:
            "Failed to update"
    else:
        messages = Chats.query.order_by(Chats.id).all()
        return render_template('chatroom.html', messages=messages)


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    user = User.query.filter(User.email == session['user_email']).first()

    if request.method == "POST":
        message = request.form['message']

        user_message = Chatbot_Messages(
            name=user.name,
            email=user.email,
            message=message
        )

        try:
            db.session.add(user_message)
            user.score += 10
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Failed to update: {str(e)}"
        return redirect('/chatbot')

    else:
        messages = Chatbot_Messages.query.filter(Chatbot_Messages.email == session['user_email']).order_by(Chatbot_Messages.id).all()
        return render_template("chatbot.html", messages=messages, name=user.name)


@app.route('/chatbot/stream')
def chatbot_stream():
    user = User.query.filter(User.email == session['user_email']).first()

    def event_stream():
        messages = Chatbot_Messages.query.filter(Chatbot_Messages.email == session['user_email']).order_by(Chatbot_Messages.id).all()

        if messages and messages[-1].name != "Code Mentor":
            last_user_message = messages[-1].message
            response = chatbot_response(
                name=user.name,
                language=user.language,
                experience=user.experience,
                path=user.path,
                message=last_user_message
            )

            chatbot_message = Chatbot_Messages(
                name="Code Mentor",
                email=user.email,
                message=response
            )

            try:
                db.session.add(chatbot_message)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Failed to save AI response: {str(e)}")

            yield f"data: {response}\n\n"

        yield "data: END\n\n"

    return Response(stream_with_context(event_stream()), content_type='text/event-stream')


@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(desc(User.score)).all()

    return render_template('leaderboard.html', users=users)


@app.route('/ide')
def ide():
    user = User.query.filter(User.email == session['user_email']).first()
    return render_template('ide.html', language=user.language)


@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.form.get('code')
    user_input = request.form.get("input", "")
    language = request.form.get('language')

    if language in ["python", 'py', "python3"]:
        try:
            result = subprocess.run(
                ['python', '-c', code],
                input=user_input,
                capture_output=True, text=True, timeout=5
            )
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)
    else:
        output = "Unsupported language"

    return jsonify(output=output)


if __name__ == "__main__":
    app.run(debug=True)