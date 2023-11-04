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
        {'content': 'priority 1', 'link': 'https://drive.google.com/file/d/1WuZXPkpVmTVO5cEsfjEpqHT9Ihy1tw45/view?usp=drive_link'},
        {'content': 'priority 2', 'link': 'https://drive.google.com/file/d/1vLTpeHZB1j-V4vC08_kLpm8gHtp_tMAr/view?usp=drive_link'},
        {'content': 'priority 3', 'link': 'https://drive.google.com/file/d/1IpbsFPWONYNeHSmkYMg1zERY4nYGjK0x/view?usp=drive_link'}
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





if __name__ == '__main__':
    app.run(debug=True)
