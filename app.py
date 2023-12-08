from flask import Flask, render_template, request, redirect, url_for, session , flash , jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from wtforms import HiddenField
from flask_wtf import FlaskForm
from datetime import datetime
import pandas as pd
import numpy as np 
from flask import session
from datetime import datetime
import csv
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
    security_question = db.Column(db.String(50), nullable=False)
    security_answer = db.Column(db.String(20), nullable=False)

class RegistrationForm(FlaskForm):
    selectedGoal = HiddenField()
    selectedArea = HiddenField()
    
# class WorkoutPlan(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     day = db.Column(db.String(10), nullable=False)
#     exercise_name = db.Column(db.String(100), nullable=False)
#     sets = db.Column(db.Integer, nullable=False)
#     reps = db.Column(db.Integer, nullable=False)
#     level = db.Column(db.String(50), nullable=False)
#     goal = db.Column(db.String(50), nullable=False)
#     area = db.Column(db.String(50), nullable=False)
#     info = db.Column(db.String(500), nullable=False)
    
class WorkoutPlan(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('day', 'goal', 'area'),
    )
    id = db.Column(db.Integer, autoincrement=True)
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


class NutritionEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    serving_size_g = db.Column(db.Float, nullable=False)
    fat_total_g = db.Column(db.Float, nullable=False)
    fat_saturated_g = db.Column(db.Float, nullable=False)
    protein_g = db.Column(db.Float, nullable=False)
    sodium_mg = db.Column(db.Float, nullable=False)
    potassium_mg = db.Column(db.Float, nullable=False)
    cholesterol_mg = db.Column(db.Float, nullable=False)
    carbohydrates_total_g = db.Column(db.Float, nullable=False)
    fiber_g = db.Column(db.Float, nullable=False)
    sugar_g = db.Column(db.Float, nullable=False)
    
    user = db.relationship('User', backref=db.backref('nutrition_entries', lazy=True))


class WeightEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref=db.backref('weights', lazy=True))

class WorkoutLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    user = db.relationship('User', backref=db.backref('workout_logs', lazy=True))
# import requests
# from flask import request, session , jsonify


# @app.route('/store_nutrition', methods=['POST','GET'])
# def store_nutrition():
#     # Retrieve data from the form submission and user ID from the session
#     user_id = session.get('user_id')
#     date = datetime.now().date()
#     name = request.form['name']
    
#     # Make a request to the API to retrieve nutrition data
#     api_url = 'https://api.api-ninjas.com/v1/nutrition?query=' + name
#     api_key = 'Jlh7a0UtRAQh9kONpuEYHA==1ku9R1AoxhprEdHG'  # Replace with your actual API key

#     response = requests.get(api_url, headers={'X-Api-Key': api_key})

#     if response.status_code == 200:
#         api_data = response.json()
#         print(f"Received API data: {api_data}")
#         # Extract the relevant nutrition information from the API response
        
#         calorie = api_data.get('calories', 0)
#         serving_size = api_data.get('serving_size_g', 0)
#         fat_total = api_data.get('fat_total_g', 0)
#         fat_saturated = api_data.get('fat_saturated_g', 0)
#         protein = api_data.get('protein_g', 0)
#         sodium = api_data.get('sodium_mg', 0)
#         potassium = api_data.get('potassium_mg', 0)
#         cholesterol = api_data.get('cholesterol_mg', 0)
#         carbohydrates = api_data.get('carbohydrates_total_g', 0)
#         fiber = api_data.get('fiber_g', 0)
#         sugar = api_data.get('sugar_g', 0)
        
#         # Check if a user ID is available
#         if user_id is not None:
#             nutrition_data = NutritionEntry(
#                 user_id=user_id,
#                 date=date,
#                 name=name,
#                 calorie=calorie,
#                 serving_size=serving_size,
#                 fat_total=fat_total,
#                 fat_saturated=fat_saturated,
#                 protein=protein,
#                 sodium=sodium,
#                 potassium=potassium,
#                 cholesterol=cholesterol,
#                 carbohydrates=carbohydrates,
#                 fiber=fiber,
#                 sugar=sugar
#             )
#             db.session.add(nutrition_data)
#             db.session.commit()
#             return 'Data stored successfully!'
#         else:
#             return 'User not authenticated. Please log in.'
#     else:
#         print(f"Failed to retrieve data from the API. Status code: {response.status_code}")

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')

# @app.route('/nutrition', methods=['GET', 'POST'])
# def nutrition():
#     if request.method == 'POST':
#         print("Hi")
#         # This block of code handles the POST request (form submission)

#         # Retrieve data from the form submission and user ID from the session
#         user_id = session.get('user_id')
#         date = datetime.now().date()
#         name = request.form['food']  # Retrieve the food item entered by the user

#         # Make a request to the API to retrieve nutrition data
#         api_url = f'https://api.api-ninjas.com/v1/nutrition?query={name}'
#         api_key = 'Jlh7a0UtRAQh9kONpuEYHA==1ku9R1AoxhprEdHG'  # Replace with your actual API key

#         try:
#             response = requests.get(api_url, headers={'X-Api-Key': api_key})

#             if response.status_code == 200:
#                 api_data = response.json()
#                 print(f"Received API data: {api_data}")
#                 # Extract the relevant nutrition information from the API response
#                 for item in api_data:
#                     calorie = item.get('calories', 0)
#                     serving_size = item.get('serving_size_g', 0)
#                     fat_total = item.get('fat_total_g', 0)
#                     fat_saturated = item.get('fat_saturated_g', 0)
#                     protein = item.get('protein_g', 0)
#                     sodium = item.get('sodium_mg', 0)
#                     potassium = item.get('potassium_mg', 0)
#                     cholesterol = item.get('cholesterol_mg', 0)
#                     carbohydrates = item.get('carbohydrates_total_g', 0)
#                     fiber = item.get('fiber_g', 0)
#                     sugar = item.get('sugar_g', 0)

#                 # Check if a user ID is available
#                 if user_id is not None:
#                     nutrition_data = NutritionEntry(
#                         user_id=user_id,
#                         date=date,
#                         name=name,
#                         calories=calorie,
#                         serving_size_g=serving_size,
#                         fat_total_g=fat_total,
#                         fat_saturated_g=fat_saturated,
#                         protein_g=protein,
#                         sodium_mg=sodium,
#                         potassium_mg=potassium,
#                         cholesterol_mg=cholesterol,
#                         carbohydrates_total_g=carbohydrates,
#                         fiber_g=fiber,
#                         sugar_g=sugar
#                     )
#                     db.session.add(nutrition_data)
#                     db.session.commit()
#                     return 'Data stored successfully!'
                    

#                 else:
#                     return 'User not authenticated. Please log in.'
#             else:
#                 print(f"Failed to retrieve data from the API. Status code: {response.status_code}")
#                 return 'Failed to retrieve data from the API.'
#         except Exception as e:
#             # Handle exceptions and log the error
#             print(f"An error occurred: {str(e)}")
#             return 'An error occurred while processing your request.'

#     else:
#         # This block of code handles the GET request (displaying the nutrition page)
#         # Add your admin dashboard logic here
#         return render_template('nutrition.html')


@app.route('/workout_log')
def workout_log():
    return render_template('workout_log.html')


@app.route('/add_workout', methods=['POST'])
def add_workout():
    data = request.get_json()

    user_id = session.get('user_id')
    exercise_name = data['exercise_name']
    sets = data['sets']
    reps = data['reps']
    weight = data['weight']
    date_str = data['date']

        # Convert date string to Python date object
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    # print("User ID from session:", user_id)


        # Check if the user is authenticated before attempting to insert a workout
    
    new_workout = WorkoutLog(user_id=user_id, exercise_name=exercise_name, sets=sets, reps=reps, weight=weight, date=date)
    db.session.add(new_workout)
    db.session.commit()

    return jsonify({'message': 'Workout added successfully'})


@app.route('/get_workouts', methods=['GET'])
def get_workouts():
    # Get the user_id from the session
    user_id = session.get('user_id')

    # Filter workouts based on user_id
    workouts = WorkoutLog.query.filter_by(user_id=user_id).all()

    # Return the filtered workouts
    workout_list = [{'id': workout.id,
                     'exercise_name': workout.exercise_name,
                     'sets': workout.sets,
                     'reps': workout.reps,
                     'weight': workout.weight,
                     'date': workout.date.strftime('%Y-%m-%d')} for workout in workouts]
    return jsonify({'workouts': workout_list})

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
        security_question = request.form['securityQuestion']
        security_answer = request.form['answer']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error_message = 'Username already exists. Please choose another username.'
            return render_template('register.html', error=error_message)
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, name=name, email=email, password=hashed_password, age=age, weight=weight, height=height, fitness_goal=selected_goal, focus_area=selected_area, security_question=security_question, security_answer=security_answer)
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
        # Inside your login route
        session['user_id'] = user.id  # Assuming user is the user object retrieved from the database


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

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        username = request.form['username']
        security_answer = request.form['security_answer']
        new_password = request.form['new_password']  # Input for the new password

        # Replace the following logic with your actual user data retrieval
        user = User.query.filter_by(username=username).first()

        if user and user.security_answer == security_answer:
            # Update the user's password in the database
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            
            # Commit the changes to the database
            db.session.commit()

            flash('Password successfully reset.')
            return redirect(url_for('login'))
        else:
            
            error_message = 'Invalid username or security answer. Please try again.'
            return render_template('forgotPassword.html', error=error_message)

    return render_template('forgotPassword.html')

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

# @app.route('/store_workout_log', methods=['POST'])
# def store_workout_log():
#     if 'user_id' in session:
#         user_id = session['user_id']
#         user = User.query.filter_by(id=user_id).first()
#         if user:
#             # exercise_name = request.form['exercise_name']
#             # sets = int(request.form['sets'])
#             # reps = int(request.form['reps'])
#             # weight = request.form['weight']
#             # date = datetime.now().date()
            
#             exercise_name = request.form.get('exercise-name')
#             sets = request.form.get('sets')
#             reps = request.form.get('reps')
#             weight = request.form.get('weight')
#             date = request.form.get('workout-date')
            
#             workout_log = WorkoutLog(
                
#                 user_id=user_id,
#                 exercise_name=exercise_name,
#                 sets=sets,
#                 reps=reps,
#                 weight=weight,
#                 date=date
#             )

#             db.session.add(workout_log)
#             db.session.commit()

#             flash("Workout log entry added successfully.", "success")
#             return redirect(url_for('workout_log'))
#         else:
#             flash("User not found.", "danger")
#     else:
#         flash("You must be logged in to add workout log entries.", "warning")
#         return redirect(url_for('login'))

# # Add this route to display the workout log page
# @app.route('/workout_log')
# def workout_log():
#     if 'user_id' in session:
#         user_id = session['user_id']
#         user = User.query.filter_by(id=user_id).first()
#         if user:
#             # Retrieve workout log entries for the logged-in user
#             workout_logs = WorkoutLog.query.filter_by(user_id=user_id).order_by(WorkoutLog.date).all()
#             return render_template('workout_log.html', workout_logs=workout_logs)
#         else:
#             flash("User not found.", "danger")
#     else:
#         flash("You must be logged in to view the workout log.", "warning")
#         return redirect(url_for('login'))
# workout_data = []
# @app.route('/store_workout', methods=['POST'])
# def store_workout():
#     data = request.get_json()
#     workout_data.append(data)
#     return jsonify(success=True)


# @app.route('/get_workouts')
# def get_workouts():
#     return jsonify(workouts=workout_data)

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
        # Calculate the length of exercises for each day
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        exercise_lengths = {}
        for day in days_order:
            exercise_lengths[day] = len([exercise for exercise in workout_plan if exercise.day == day])
        return render_template('beginner_plan.html', workout_plan=workout_plan, exercise_lengths=exercise_lengths)
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

@app.route('/bmi')
def bmi():
    return render_template('bmi.html')

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
from datetime import datetime

@app.route('/add_weight', methods=['POST', 'GET'])
def add_weight():
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            if user:
                weight = float(request.form.get('weight'))
                date = datetime.now().date()
                weight_entry = WeightEntry(user_id=user_id, date=date, weight=weight)
                db.session.add(weight_entry)
                db.session.commit()
                flash("Weight entry added successfully.", "success")
                return redirect(url_for('weight_chart'))
            else:
                flash("User not found.", "danger")
        else:
            flash("You must be logged in to add weight entries.", "warning")
    elif request.method == 'GET':
        return render_template('add_weight.html')


@app.route('/weight_chart')
def weight_chart():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        if user:
            # Retrieve weight entries for the logged-in user
            weight_entries = WeightEntry.query.filter_by(user_id=user_id).order_by(WeightEntry.date).all()
            # Extract dates and weights for the chart
            dates = [entry.date.strftime('%Y-%m-%d') for entry in weight_entries]
            weights = [entry.weight for entry in weight_entries]
            return render_template('weight_chart.html', dates=dates, weights=weights)
        else:
            flash("User not found.", "danger")
    else:
        flash("You must be logged in to view the weight chart.", "warning")
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

# Create the database and tables before running the app
with app.app_context():
    db.create_all()


if __name__ == '__main__':
 
    app.run(debug=True)
