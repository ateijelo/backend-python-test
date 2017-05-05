from functools import wraps
from alayatodo import app
from flask import (
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
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

    sql = "SELECT * FROM users WHERE username = ? AND password = ?"
    cur = g.db.execute(sql, (username, password))
    user = cur.fetchone()
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/')


@app.route('/todo/<todo_id>/json', methods=['GET'])
@login_required
def todo_json(todo_id):
    user_id = session.get('user_id') # Guaranteed by login_required
    cur = g.db.execute("SELECT * FROM todos WHERE id = ? and user_id = ?", (todo_id, user_id))
    todo = cur.fetchone()
    if not todo:
        # Note: we could return code 404 (Not Found) when the todo_id is
        # not valid and 403 (Forbidden) when it's valid but doesn't belong
        # to user_id, but users could abuse this to find out which todos
        # exist and which don't.
        # In any case, from this user_id's perspective, the todo doesn't
        # exist, so 404.
        abort(404)
    return jsonify(dict(todo))


@app.route('/todo/<todo_id>', methods=['GET'])
@login_required
def todo(todo_id):
    cur = g.db.execute(
        "SELECT * FROM todos \
        WHERE id = ? AND user_id = ?",
        (todo_id, session['user_id'])
    )
    todo = cur.fetchone()
    if not todo:
        abort(404)
    return render_template('todo.html', todo=todo)


@app.route('/todo/', methods=['GET'])
@login_required
def todos():
    cur = g.db.execute(
        "SELECT * FROM todos \
        WHERE user_id = ?",
        (session['user_id'],)
    )
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


@app.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    description = request.form.get('description', '')
    if len(description) > 0:
        g.db.execute(
            "INSERT INTO todos (user_id, description) VALUES (?, ?)",
            (session['user_id'], description)
        )
        g.db.commit()
        flash("Todo added successfully", "success")
    else:
        flash("Description can not be empty", "danger")
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
@login_required
def todo_delete(todo_id):
    g.db.execute(
        "DELETE FROM todos \
         WHERE id ='%s' AND user_id = ?",
        (todo_id, session['user_id'])
    )
    g.db.commit()
    flash("Todo deleted successfully", "success")
    return redirect('/todo')


@login_required
def todo_set(todo_id, completed):
    g.db.execute(
        "UPDATE todos SET completed = ? \
         WHERE id = ? and user_id = ?",
        ((1 if completed else 0), todo_id, session['user_id'])
    )
    g.db.commit()
    return redirect(request.referrer or '/todo')


@app.route('/todo/complete/<id>', methods=['POST'])
def todo_complete(id):
    return todo_set(id, True)


@app.route('/todo/clear/<id>', methods=['POST'])
def todo_clear(id):
    return todo_set(id, False)
