from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, UserMixin, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this in production

# -------------------------
# DATABASE CONFIG
# -------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lightning_warriors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------
# LOGIN MANAGER
# -------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -------------------------
# MODELS
# -------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    division = db.Column(db.String(120))
    coach = db.Column(db.String(120))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120))
    location = db.Column(db.String(120))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------------
# ROUTES
# -------------------------

@app.route('/')
def index():
    return render_template('dashboard.html')

# ----- AUTH -----

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing = User.query.filter_by(username=username).first()
        if existing:
            return "User already exists"

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return "Invalid username or password"

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ----- TEAMS -----

@app.route('/teams')
def teams():
    all_teams = Team.query.all()
    return render_template('teams.html', teams=all_teams)


@app.route('/team/<int:team_id>')
def team_detail(team_id):
    team = Team.query.get_or_404(team_id)
    return render_template('team_detail.html', team=team)


@app.route('/team/new', methods=['GET', 'POST'])
@login_required
def team_form():
    if request.method == 'POST':
        name = request.form['name']
        division = request.form.get('division')
        coach = request.form.get('coach')

        new_team = Team(name=name, division=division, coach=coach)
        db.session.add(new_team)
        db.session.commit()

        return redirect(url_for('teams'))

    return render_template('team_form.html')

# ----- EVENTS -----

@app.route('/events')
def events():
    all_events = Event.query.all()
    return render_template('events.html', events=all_events)


@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)


@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def event_form():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form.get('date')
        location = request.form.get('location')

        new_event = Event(title=title, date=date, location=location)
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('events'))

    return render_template('event_form.html')

# ----- MEMBERS -----

@app.route('/members')
def members():
    return render_template('members.html')

# -------------------------
# RUN APP
# -------------------------

if __name__ == '__main__':
    app.run(debug=True)
