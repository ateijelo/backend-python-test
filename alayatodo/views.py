from functools import wraps

from alayatodo import app, db
from alayatodo.models import User, Todo

from flask import (
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
    )


def login_required(view_func):
    @wraps(view_func)
    def g(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return view_func(*args, **kwargs)
    return g


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.authenticate(username, password)
    if user:
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect('/todo')

    flash("Invalid username or password", "danger")
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/')


@app.route('/todo/<todo_id>/json', methods=['GET'])
@login_required
def todo_json(todo_id):
    todo = db.session.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == session['user_id']
    ).first_or_404()
    return jsonify(todo.to_dict())


@app.route('/todo/<todo_id>', methods=['GET'])
@login_required
def todo(todo_id):
    todo = db.session.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == session['user_id']
    ).first_or_404()
    return render_template('todo.html', todo=todo)


@app.route('/todo/', methods=['GET'])
@login_required
def todos():
    per_page = request.args.get('per_page', 10, int)
    page = request.args.get('page', 1, int)
    session['per_page'] = per_page
    session['page'] = page
    todos = db.session.query(Todo).filter(
        Todo.user_id == session['user_id']
    ).paginate(per_page=per_page)
    return render_template('todos.html', todos=todos, page=page)


@app.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    description = request.form.get('description', '')
    per_page = session.get('per_page', None)
    page = 1
    if len(description) > 0:
        todo = Todo(description=description, user_id=session['user_id'], completed=False)
        db.session.add(todo)
        db.session.commit()
        flash("Todo added successfully", "success")
        c = db.session.query(Todo).filter(
            Todo.user_id == session['user_id']
        ).count()
        page = 1 + (c - 1) // per_page
    else:
        flash("Description can not be empty", "danger")
    return redirect(url_for('todos', page=page, per_page=per_page))


@app.route('/todo/<todo_id>', methods=['POST'])
@login_required
def todo_delete(todo_id):
    todo = db.session.query(Todo).get(todo_id)
    page = session.get('page', None)
    per_page = session.get('per_page', None)
    if todo and todo.user_id == session['user_id']:
        if page and per_page:
            c = db.session.query(Todo).filter(
                Todo.user_id == session['user_id']
            ).count()
            last_page = 1 + (c - 1) // per_page
            if page == last_page and (c % per_page == 1):
                page = max(1, page - 1)
        db.session.delete(todo)
        db.session.commit()
        flash("Todo deleted successfully", "success")
    return redirect(url_for('todos', page=page, per_page=per_page))


@login_required
def todo_set(todo_id, completed):
    todo = db.session.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == session['user_id']
    ).first()
    if todo:
        todo.completed = completed
        db.session.commit()
    return redirect(request.referrer or '/todo')


@app.route('/todo/complete/<id>', methods=['POST'])
def todo_complete(id):
    return todo_set(id, True)


@app.route('/todo/clear/<id>', methods=['POST'])
def todo_clear(id):
    return todo_set(id, False)
