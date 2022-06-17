from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://WilfredM94code:Ralph2828@localhost:5432/flask_todolist'
app.config['SECRET_KEY'] = '\x9e\x95\xfd\na\x12t\xca&\x1c\x8a\x99\x18tD\xf12y\x11\xae\x1c\xfda\xfd'
db = SQLAlchemy(app)

class Topics(db.Model):
    __tablename__ = 'topics'
    topic_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(length=255))
    task  = db.relationship('Tasks', cascade = 'all, delete-orphan')

class Tasks(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key = True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    description = db.Column(db.String(length=255))
    topic = db.relationship('Topics', backref = 'topic')

@app.route('/')
def home():
    return render_template('home.html', topics = Topics.query.all())

@app.route('/topic/<topic_id>')
def topic(topic_id):
    return render_template('topic-task.html', topic = Topics.query.filter_by(topic_id = topic_id).first(), tasks = Tasks.query.filter_by(topic_id = topic_id).all())

@app.route('/add/topic/', methods=['POST'])
def add_topic():
    if not request.form['topic-title']:
        flash ('No topic title')
    else:
        topic = Topics(title = request.form['topic-title'])
        db.session.add(topic)
        db.session.commit()
        flash ('Topic added successfully')
    return redirect(url_for('home'))

@app.route('/add/task/<topic_id>', methods=['POST'])
def add_task(topic_id):
    if not request.form['task-description']:
        flash ('No task added')
    else:
        task = Tasks(topic_id = topic_id, description = request.form['task-description'])
        db.session.add(task)
        db.session.commit()
        flash ('Task added successfully')
    return redirect(url_for('topic', topic_id = topic_id))

@app.route('/delete/task/<task_id>', methods=['POST'])
def delete_task(task_id):
    task_to_delete = Tasks.query.filter_by(task_id = task_id).first()
    topic_id = task_to_delete.topic.topic_id
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('topic', topic_id = topic_id))

@app.route('/delete/topic/<topic_id>', methods=['POST'])
def delete_topic(topic_id):
    topic_to_delete = Topics.query.filter_by(topic_id = topic_id).first()
    db.session.delete(topic_to_delete)
    db.session.commit()
    return redirect(url_for('home', topic_id = topic_id))

if __name__ == '__main__':
    app.run(debug=True)