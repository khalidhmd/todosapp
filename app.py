from flask import Flask, render_template, redirect, request, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user1:user1@localhost:5432/tododb'

db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repr__(self):
    return f'<Todo ID: {self.id}, description: {self.description}>'

db.create_all()


@app.route('/')
def index():
    return render_template('index.html', todos=Todo.query.all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({'id':todo.id,'description':todo.description})


if __name__ == '__main__':
  app.run()