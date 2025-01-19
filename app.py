from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from questions_grader import retrieve_and_grade
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
    experience = db.Column(db.String, nullable = False)
    score = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f'<User {self.id}:\n{self.name}\n{self.email}\n{self.password}\n{self.quote}\n{self.language}\n{self.experience}\n{self.score}>'
    

@app.route('/', methods=['GET', 'POST'])
def index():

    # REMOVEEEE !!!!!!!!
    #session["logged_in"] = False
    # REMOVEEE  !!!!!!!!!!!!!!

    user = User.query.filter(User.email == session['user_email']).first()

    if request.method == "POST":
        retrieve_and_grade(request)
    else:
        if 'logged_in' in session and session['logged_in']:
            return render_template('index.html', user=user)
        return redirect(url_for('register'))


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
                return redirect(url_for('index'))
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
        experience = request.form['experience']

        existing_user = User.query.filter(User.email == email).first()
        if existing_user is None:
            new_user = User(
                name=name,
                email=email,
                password=password,
                language=language,
                experience=experience
            )

            if password != confirm_password:
                return render_template("register.html")

            try:
                db.session.add(new_user)
                db.session.commit()
                session['logged_in'] = True
                return redirect('/')
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
