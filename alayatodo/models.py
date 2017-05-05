from alayatodo import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User: id=%r username=%r>' % (
            self.id, self.username
        )

    @staticmethod
    def authenticate(username, password):
        return db.session.query(User).filter(
            User.username == username,
            User.password == password
        ).first()

class Todo(db.Model):

    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            description=self.description,
            completed=self.completed
        )

    def __repr__(self):
        return '<Todo: id=%r user_id=%r desc=%r completed=%r>' % (
            self.id, self.user_id, self.description, self.completed
        )
