from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from main import ai_response
import requests
import keys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SECRET_KEY'] = keys.secret_key
db = SQLAlchemy(app)
url = "https://zenquotes.io/api/random"


# ToDo database
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable = False)

    def __repr__(self):
        return '<Task %r>' % self.id
    

# User database
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    quote = db.Column(db.String, default=requests.get(url).json()[0]['q'])
    language = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable = False)
    experience = db.Column(db.String, nullable = False)
    score = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f'<User {self.id}:\n{self.name}\n{self.email}\n{self.password}\n{self.quote}\n{self.language}\n{self.experience}\n{self.score}>'
    

@app.route('/', methods=['GET', 'POST'])
def home():

    # REMOVEEEE !!!!!!!!
    #session["logged_in"] = False
    #session['answered'] = True
    # REMOVEEE  !!!!!!!!!!!!!!

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
        tasks = ToDo.query.filter(ToDo.email == session['user_email']).order_by(ToDo.id).all()

        if 'logged_in' in session and session['logged_in']:
            user = User.query.filter(User.email == session['user_email']).first()
            return render_template('home.html', user=user, tasks = tasks)
        elif 'answered' in session and not session['answered']:
            return redirect(url_for('questions'))
        return redirect(url_for('register'))


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    user = User.query.filter(User.email == session['user_email']).first()

    if request.method == "POST":
        tasks = ai_response(request)

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
    else:
        return render_template('questions.html', user=user)


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
                return render_template("login.html", error = 'Incorrect password')
        else:
            return render_template("login.html", error = 'User not found')
    return render_template("login.html", error = '')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        language = request.form['language']
        path = request.form['path']
        experience = request.form['experience']

        existing_user = User.query.filter(User.email == email).first()
        if existing_user is None:
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
            return render_template("register.html", error = 'Email already in use')
    else:
        return render_template("register.html")


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
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

if __name__ == "__main__":
    app.run(debug=True)
