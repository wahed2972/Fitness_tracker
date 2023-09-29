from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__, template_folder="D:/Final Year Project/Fitness Tracker/Templates")
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)  # Initialize Flask-Bcrypt

# Create a SQLite database connection
conn = sqlite3.connect('fitness.db')

@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Add your dashboard logic here
    return render_template('Frontend/dashboard.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password using Flask-Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Call the register_user function to insert the user into the database
        register_user(username, email, hashed_password)

        # Redirect to a login page or another appropriate page
        return redirect(url_for('login'))
    return render_template('register.html')  # Display the registration form


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve user information from the database
        user = get_user_by_username(username)

        if user and bcrypt.check_password_hash(user['password'], password):
            # User is authenticated, set up a session (use Flask-Session or Flask-Login)
            session['user_id'] = user['user_id']

            # Redirect to the user's dashboard or another appropriate page
            return redirect(url_for('dashboard'))
        else:
            # Incorrect username or password, show an error message
            error_message = 'Invalid username or password.'
            return render_template('login.html', error=error_message)
    return render_template('login.html')


def register_user(username, email, password):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (username, email, password))
    conn.commit()
    cursor.close()

def get_user_by_username(username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user


if __name__ == '__main__':
    app.run(debug=True)
