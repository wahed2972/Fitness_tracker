from flask import Flask, render_template, request, redirect, url_for, session , flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from wtforms import HiddenField
from flask_wtf import FlaskForm

app = Flask(__name__, template_folder="Templates")
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)  # Initialize Flask-Bcrypt

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    fitness_goal = db.Column(db.String(50), nullable=True)
    focus_area = db.Column(db.String(50), nullable=True)

class RegistrationForm(FlaskForm):
    selectedGoal = HiddenField()
    selectedArea = HiddenField()
    
class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    goal = db.Column(db.String(50), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    info = db.Column(db.String(500), nullable=False)
    
class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)


class Nutrition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    
# Create the database and tables before running the app
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Add your dashboard logic here
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        # Retrieve the user's username from the database
        user = User.query.filter_by(id=user_id).first()
        if user:
            username = user.username
        else:
            username = None
        return render_template('Frontend/dashboard.html', username=username, logged_in=True)
    else:
        # User is not logged in
        return render_template('Frontend/dashboard.html', logged_in=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        email = request.form['email']
        password = request.form['password']
        selected_goal = request.form['selectedGoal']
        selected_area = request.form['selectedArea']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error_message = 'Username already exists. Please choose another username.'
            return render_template('register.html', error=error_message)
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, name=name, email=email, password=hashed_password, age=age, weight=weight, height=height, fitness_goal=selected_goal, focus_area=selected_area)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == '987':
            session['user_id'] = 'admin'  # Use a unique identifier for the admin, e.g., 'admin'
            return redirect(url_for('admin_dashboard'))

        # Retrieve user information from the database
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # User is authenticated, set up a session (use Flask-Session or Flask-Login)
            session['user_id'] = user.id

            # Redirect to the user's dashboard or another appropriate page
            return redirect(url_for('dashboard'))
        else:
            # Incorrect username or password, show an error message
            error_message = 'Invalid username or password.'
            return render_template('login.html', error=error_message)
    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # Add your admin dashboard logic here
    return render_template('admin_dashboard.html')

@app.route('/logout')
def logout():
    # Clear the user's session to log them out
    session.clear()

    # Redirect the user to the homepage or login page
    return redirect(url_for('index'))

@app.route('/add_plan', methods=['GET', 'POST'])
def add_plan():
    if request.method == 'POST':
        day = request.form['day']
        exercise_name = request.form['exercise_name']
        sets = int(request.form['sets'])
        reps = int(request.form['reps'])
        level = request.form['level']
        goal = request.form['goal']
        area = request.form['area']
        info = request.form['info']

        plan = WorkoutPlan(day=day, exercise_name=exercise_name, sets=sets, reps=reps, level=level, goal=goal, area=area, info = info)
        db.session.add(plan)
        db.session.commit()

        return redirect(url_for('add_plan'))

    return render_template('add_plan.html')

# Assume you have a User model and a WorkoutPlan model defined in your application

@app.route('/beginner')
def beginner_plan():
    # Get the user's registered goal and area
    user_id = session['user_id']  # Assuming you have a session for user authentication
    user = User.query.filter_by(id=user_id).first()
    user_goal = user.fitness_goal
    user_area = user.focus_area

    # Query the workout plan for beginners matching the user's goal and area
    workout_plan = WorkoutPlan.query.filter_by(level='beginner', goal=user_goal, area=user_area).all()

    if workout_plan:
        return render_template('beginner_plan.html', workout_plan=workout_plan)
    else:
        return redirect(url_for('dashboard'))
# Repeat the above code for intermediate and advanced routes with 'level' set to 'intermediate' and 'advanced'

@app.route('/intermediate')
def intermediate_plan():
    user_id = session['user_id']  # Assuming you have a session for user authentication
    user = User.query.filter_by(id=user_id).first()
    user_goal = user.fitness_goal
    user_area = user.focus_area

    # Query the workout plan for beginners matching the user's goal and area
    workout_plan = WorkoutPlan.query.filter_by(level='intermediate', goal=user_goal, area=user_area).first()

    if workout_plan:
        return render_template('intermediate_plan.html', workout_plan=[workout_plan])
    else:
        return redirect(url_for('dashboard'))
    # Similar to the beginner_plan route

@app.route('/advanced')
def advanced_plan():
    user_id = session['user_id']  # Assuming you have a session for user authentication
    user = User.query.filter_by(id=user_id).first()
    user_goal = user.fitness_goal
    user_area = user.focus_area

    # Query the workout plan for beginners matching the user's goal and area
    workout_plan = WorkoutPlan.query.filter_by(level='advanced', goal=user_goal, area=user_area).first()

    if workout_plan:
        return render_template('advanced_plan.html', workout_plan=[workout_plan])
    else:
        return redirect(url_for('dashboard'))
    # Similar to the beginner_plan route

@app.route('/users')
def user_list():
    # Retrieve all users from the 'user' table in the database
    users = User.query.all()
    
    return render_template('users.html', users=users)

# Route to render the user profile page
@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        # Retrieve the user's information from the database
        user = User.query.filter_by(id=user_id).first()
        if user:
            # Render the profile page and pass the user information to the template
            return render_template('profile.html', user=user)
    # Redirect to the login page if the user is not logged in
    return redirect(url_for('login'))

# Route to update the user's profile
@app.route('/update_profile', methods=['POST'])
def update_profile():
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        # Retrieve the user from the database
        user = User.query.filter_by(id=user_id).first()
        if user:
            # Update user information with data from the form
            user.username = request.form['username']
            user.name = request.form['name']
            user.age = int(request.form['age'])
            user.weight = int(request.form['weight'])
            user.height = int(request.form['height'])
            user.fitness_goal = request.form['goal']
            user.focus_area = request.form['area']
            
            # Check if a new password is provided and hash it
            new_password = request.form['password']
            if new_password:
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                user.password = hashed_password
            # Commit the changes to the database
            db.session.commit()
            # Redirect to the profile page after the update
            return redirect(url_for('profile'))
    # Redirect to the login page if the user is not logged in or if there's an issue with the update
    return redirect(url_for('login'))


@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/workout_plan')
def workout_plan():
    return render_template('workout_plan.html')

@app.route('/workout1')
def workout1():
    return render_template('workout1.html')


@app.route('/workout2')
def workout2():
    return render_template('workout2.html')


@app.route('/workout3')
def workout3():
    return render_template('workout3.html')


@app.route('/workout4')
def workout4():
    return render_template('workout4.html')


@app.route('/workout5')
def workout5():
    return render_template('workout5.html')


@app.route('/workout6')
def workout6():
    return render_template('workout6.html')


@app.route('/workout7')
def workout7():
    return render_template('workout7.html')

@app.route('/nutrition_plan')
def nutrition_plan():
    return render_template('nutrition_plan.html')

@app.route('/contact_us', methods=['POST','GET'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Create a new ContactSubmission object and add it to the database
        contact_submission = ContactSubmission(name=name, email=email, subject=subject, message=message)
        db.session.add(contact_submission)
        db.session.commit()

        # Optionally, you can display a flash message to indicate successful submission
        flash("Thank you for contacting us. We will get back to you soon.", "success")

        # Redirect the user to a different page after the submission
        return redirect(url_for('index'))

    # Handle cases where the request method is not POST (e.g., GET requests)
    # return redirect(url_for('contact_us'))
    return render_template('contact_us.html')

# Create the database and tables before running the app
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
