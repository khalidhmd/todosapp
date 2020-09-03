from flask import Flask, render_template, redirect, request, url_for,jsonify,abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user1:user1@localhost:5432/tododb'

db = SQLAlchemy(app)

migrate = Migrate(app,db)


class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean(),nullable=False, default=False)

  def __repr__(self):
    return f'<Todo ID: {self.id}, description: {self.description}>'

# db.create_all() #disable this before flask db migrate


@app.route('/')
def index():
    return render_template('index.html', todos=Todo.query.all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:  
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
    body['id'] = todo.id
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return jsonify(body)


if __name__ == '__main__':
  app.run()