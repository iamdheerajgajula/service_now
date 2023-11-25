from flask import Flask, render_template, request, redirect, session
import csv


def check_user_credentials(username, password):
    with open('registered.csv', mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            stored_username, stored_password = row
            if username == stored_username and password == stored_password:
                return True
    return False

app = Flask(__name__)
app.secret_key="secret key"
superuser_username_val = 'sumanpg'
superuser_password_val = 'payrent'

# Sample user credentials for demonstration


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # You can retrieve the user's study contents here
    if not session.get('authenticated'):
        return redirect('/')
    study_contents = [
        {'content': 'CAD DUMPS 1', 'link': 'https://drive.google.com/file/d/12Uugn8oIw5ZBv0Ly50KXFxtb_UfGDC-g/view?usp=drive_link'},
        {'content': 'CAD 4', 'link': 'https://drive.google.com/file/d/1-wcR8K2VTAs65fid1zQMBbjmgp3c-fmQ/view?usp=drive_link'},
        {'content': 'CAD 6', 'link': 'https://drive.google.com/file/d/1GZqEZob1SU2bObmtXXsFocd0ODWubnnb/view?usp=drive_link'},
        {'content': 'CAD 6(1)', 'link': 'https://drive.google.com/file/d/1GZqEZob1SU2bObmtXXsFocd0ODWubnnb/view?usp=drive_link'},
        {'content': 'CAD 8', 'link': 'https://drive.google.com/file/d/1ZqB8_LiC5N1VkhU4HItgbjIN_eMDeow4/view?usp=drive_link'},
        {'content': 'CAD ASKED IN EXAM PREV', 'link': 'https://drive.google.com/file/d/1VgxCKqeOkA5IZIYdI9pcd4GQ3h9KD4GN/view?usp=drive_link'},
        {'content': 'CAD IMP', 'link': 'https://drive.google.com/file/d/1HFSZKcHZQcJ3F3m_J97lwcb97OJccdY6/view?usp=drive_link'},
        {'content': 'CAD (1)', 'link': 'https://drive.google.com/file/d/1hQ39jDKL3KCdZQdKn0oYbHapKCVn6-ZA/view?usp=drive_link'},
        {'content': 'CAD MARKED PRACTICE 1', 'link': 'https://drive.google.com/file/d/18X022y99oCb3K6Lyr3uUsP8qX1KjIucu/view?usp=drive_link'},
        {'content': 'CAD (1)', 'link': 'https://drive.google.com/file/d/12XlnXTX_ViPbuvbRFc7kxx5iaOff6XPH/view?usp=drive_link'},


        # Add more study contents as needed
    ]
    return render_template('dashboard.html', study_contents=study_contents)


@app.route('/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')
    if check_user_credentials(username, password):
        session['authenticated'] = True
        return redirect('/dashboard')
        
    else:
        return render_template('login.html', error='Incorrect credentials')
    
@app.route("/add_user", methods=['POST'])
def admin_add_user():
    superuser_username = request.headers.get('X-Superuser-Username')
    superuser_password = request.headers.get('X-Superuser-Password')
    data = request.get_json()
    new_username = data.get('new_username')
    new_password = data.get('new_password')

    if superuser_username == superuser_username_val and superuser_password == superuser_password_val:
        data = request.get_json()
        new_username = data.get('new_username')
        new_password = data.get('new_password')
        with open('registered.csv', mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([new_username, new_password])
        # Add the new user to the database
        return 'User added successfully'
    else:
        return 'Incorrect credentials'
    
@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    return redirect('/')






