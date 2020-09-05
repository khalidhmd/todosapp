from flask import Flask, render_template, redirect, request, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user1:user1@localhost:5432/tododb'

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, description: {self.description}>'


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list')

    def __repr__(self):
        return f'<List ID: {self.id}, name: {self.name}>'


# db.create_all() #disable this before flask db migrate


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', lists=TodoList.query.all(), active_list=TodoList.query.get(list_id), todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())


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
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todos/set-completed', methods=['POST'])
def set_completed():
    try:
        completed = request.get_json()['completed']
        todo_id = request.get_json()['id']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('index.html', todos=Todo.query.order_by('id').all())


@app.route('/todos/delete', methods=['POST'])
def delete():
    try:
        todo_id = request.get_json()['id']
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('index.html', todos=Todo.query.order_by('id').all())


if __name__ == '__main__':
    app.run()
