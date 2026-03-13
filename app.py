# from flask import Flask


# from flask import Flask, render_template  # added render_template

# from flask import Flask, render_template, request, redirect, url_for
# ↑ make sure request, redirect, url_for are imported

from flask import Flask, render_template, request, redirect, url_for, flash
# make sure flash is imported

from flask_sqlalchemy import SQLAlchemy
import os

from flask_login import (
    LoginManager, UserMixin,
    login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)

app.secret_key = 'change-this-secret'  # near top, after app = Flask(__name__)


# 1) Configure SQLAlchemy to use your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2503@localhost:5432/tododb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # just disables a warning

# 2) Create a SQLAlchemy object, tied to this app
db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'  # name of our login view (we'll create it)




#==================== models ===================#
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    todos = db.relationship('Todo', backref='owner', lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.id} {self.username!r}>"




# --------- SQLAlchemy model (Python class -> DB table) ---------
class Todo(db.Model):
    __tablename__ = 'todos'  # optional, but explicit is nice

    id = db.Column(db.Integer, primary_key=True)              # SERIAL PRIMARY KEY
    title = db.Column(db.String(200), nullable=False)         # VARCHAR(200) NOT NULL
    completed = db.Column(db.Boolean, default=False)          # BOOLEAN DEFAULT FALSE

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Todo {self.id} {self.title!r} completed={self.completed}>"


#===========login loader ============#

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables once at startup (inside app context)
with app.app_context():
    print("Creating database tables...")
    db.create_all()


#=======routes =======#

# @app.route('/')
# def hello():
#     trainer_name = "Lokesh"  # normal Python variable
#     # todos = Todo.query.all()  # SELECT * FROM todos;
#     todos = Todo.query.order_by(Todo.id.desc()).all()  # newest first
#     return render_template('index.html', name=trainer_name, todos=todos)

# @app.route('/')
# @login_required
# def hello():
#     trainer_name = current_user.username
#     todos = Todo.query.order_by(Todo.id.asc()).all()  # still global for now
#     return render_template('index.html', name=trainer_name, todos=todos)

@app.route('/')
@login_required
def hello():
    trainer_name = current_user.username
    todos = Todo.query.filter_by(user_id=current_user.id)\
                      .order_by(Todo.id.asc())\
                      .all()
    return render_template('index.html', name=trainer_name, todos=todos)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # basic validation
        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('register'))

        # check if user already exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash('Username already taken. Choose another.')
            return redirect(url_for('register'))

        # create user
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))  # we'll create /login next

    # GET request
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        # correct credentials
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('hello'))  # go to home page

    # GET
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('login'))



# ... existing config, db, Todo, create_all, and '/' route ...

@app.route('/add', methods=['POST'])
@login_required
def add_todo():
    title = request.form.get('title')  # read input name="title" from form
    if title:  # simple validation
        new_todo = Todo(title=title, 
                        completed=False,
                        user_id=current_user.id)  # associate with current user
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('hello'))  # go back to home page

@app.route('/toggle/<int:todo_id>')
@login_required
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)  # 404 if not found
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('hello'))

@app.route('/delete/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        flash("Not allowed.")
        return redirect(url_for('hello'))
        
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello'))




if __name__ == '__main__':
    app.run(debug=True)
