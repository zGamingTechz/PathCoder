from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
url = "https://zenquotes.io/api/random"


# ToDo database
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String, nullable = False)

    def __repr__(self):
        return '<Task %r>' % self.id
    

# User database
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    quote = db.Column(db.String, default=requests.get(url).json()[0]['q'])
    language = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable = False)
    score = db.Column(db.Integer, nullable = False)
    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error in adding task"
    else:
        tasks = ToDo.query.order_by(ToDo.id).all()
        return render_template("index.html", tasks = tasks)
    

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
