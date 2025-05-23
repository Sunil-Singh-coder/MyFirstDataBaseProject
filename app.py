from flask import Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask app initialize kar rahe hain
app = Flask(__name__)
app.secret_key = '1231243523'


# Flask ko batate hain ki SQLite database ka path kya hai
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"

# Flask ke tracking system ko band kar rahe hain (ye performance ke liye hota hai)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy object ko Flask app ke saath initialize kar rahe hain
db = SQLAlchemy(app)

# Database ke liye ek model (table) define kar rahe hain
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)  # Primary key (unique id)
    Name = db.Column(db.String(100), nullable=False)  # Naam field, empty nahi ho sakta
    Hobbies = db.Column(db.String(100), nullable=False)  # Hobbies field, empty nahi ho sakta
    Date = db.Column(db.DateTime, default=datetime.utcnow)  # Date field, default current time set hota hai

    # Jab bhi object print hoga, ye function batayega kya show karna hai
    def __repr__(self) -> str:
        return f"{self.Name} {self.Hobbies}"

# Data delete karne ka route - sno ke basis par data delete karta hai
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()  # sno ke basis par data fetch karo
    db.session.delete(todo)  # data delete karo
    db.session.commit()  # database update karo
    return redirect('/')  # home page par wapas bhej do

# Data update karne ka route - GET se form show karta hai, POST se update karta hai
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        todo = Todo.query.filter_by(sno=sno).first()  # data fetch karo
        todo.Name = request.form['Name']  # form se updated name lo
        todo.Hobbies = request.form['Hobbies']  # form se updated hobbies lo
        db.session.add(todo)  # data ko session me daalo
        db.session.commit()  # changes commit karo
        return redirect('/')  # home page par bhej do

    todo = Todo.query.filter_by(sno=sno).first()  # agar GET request hai toh data fetch karo
    return render_template('update.html', todo=todo)  # update page render karo

# About page ka route
@app.route('/about')
def about():
    return render_template('about.html')  # about.html page return karo

# Main page ka route (home page) - yahan se data insert hota hai aur dikhaya bhi jata hai
@app.route('/', methods=['GET', 'POST'])
def Main_Page():
    if request.method == 'POST':
        NAME = request.form['Name']  # form se name lo
        HOBBIES = request.form['Hobbies']  # form se hobbies lo

        if(NAME==""and HOBBIES==""):
            flash("please enter Name and Your Task Details")
            return redirect('/')
 

        # Todo model ka object banao form ke data se
        todo = Todo(Name=NAME, Hobbies=HOBBIES)

        # object ko database me insert karo
        db.session.add(todo)
        db.session.commit()
        flash("You success added your task")

    # Sabhi data fetch karo database se
    allTodo = Todo.query.all()

    # index.html ko render karo aur saara data bhejo
    return render_template('index.html', allTodo=allTodo)

# App ko run karo debug mode me (development ke liye helpful hota hai)
if __name__ == "__main__":
    app.run(debug=True)
