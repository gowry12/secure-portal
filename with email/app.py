from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import bcrypt

app = Flask(__name__)

# Basic configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'gowry@12'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ngowry12@gmail.com'
app.config['MAIL_PASSWORD'] = 'pyyc jmou ypkb iecf'

db = SQLAlchemy(app)
mail = Mail(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

# Create database tables
with app.app_context():
    db.create_all()

# Helper function to send verification email
def send_verification_email(email):
    token = email  # Simplified for demonstration
    verification_url = url_for('confirm_email', token=token, _external=True)
    msg = Message('Verify Your Email', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Click here to verify your email: {verification_url}'
    mail.send(msg)

@app.route('/')
def index():
    return "Welcome to the Portal!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect('/register')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        send_verification_email(email)
        flash('Verification email sent! Please check your inbox.', 'info')
        return redirect('/login')

    return "Register Page"

@app.route('/confirm_email/<token>')
def confirm_email(token):
    user = User.query.filter_by(email=token).first()  # Simplified for demonstration
    if user:
        user.verified = True
        db.session.commit()
        flash('Email verified! You can now log in.', 'success')
        return redirect('/login')
    flash('Invalid verification link.', 'danger')
    return redirect('/register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if not user.verified:
                flash('Please verify your email first.', 'warning')
                return redirect('/login')

            session['email'] = user.email
            flash('Login successful!', 'success')
            return redirect('/dashboard')

        flash('Invalid credentials.', 'danger')

    return "Login Page"

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return f"Welcome {session['email']}!"
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logged out successfully.', 'info')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
