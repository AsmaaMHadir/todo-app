from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_migrate import Migrate
from sqlalchemy import func


app = Flask(__name__) # referencing this file 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 back slashes indicate a relative path
db = SQLAlchemy(app)    # initialize the database 
migrate = Migrate(app, db)


class Todo(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    deadline = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return '<Task %r>' % self.id 





@app.route('/', methods=['POST','GET']) # sets up the route
def index():
    if request.method =='POST':
        task_content = request.form['content'] # get the input with id=='content'
        task_deadline_str = request.form['deadline']  # Get the deadline as a string from the form
        task_deadline = datetime.strptime(task_deadline_str, '%Y-%m-%d').date()  # Convert to date object
        new_task = Todo(content=task_content, deadline=task_deadline) # create todo task object
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
        
    else:
        
        tasks = Todo.query.order_by(Todo.date_created).all() # return all tasks 
        return render_template('index.html', tasks=tasks, date_now=date.today())


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete =  Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        
        return "Ops, couldn't delete the task"


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content'] # update the content to the content to be sent in the POST request
        deadline_str = request.form['deadline']
    
        try:
            task.deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
            db.session.commit()
            return redirect('/')
        
        except:
            return "couldn't update"
    
    else:
        return render_template('update.html',task=task)
    


if __name__ == '__main__':
    app.run(debug=True)
