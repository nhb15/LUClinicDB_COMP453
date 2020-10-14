from flask import Flask, render_template, url_for, flash, redirect, request
from .forms import RegistrationForm, LoginForm, MedicationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
@app.route("/home")
def home():
    return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/profile")
def profile():
    return render_template('profile.html', title='Profile')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# To be removed to post login
@app.route("/addMedication", methods=['GET', 'POST'])
def addMedication():
    form = MedicationForm()
    if form.validate_on_submit():
        flash(f'Medicine {form.med.data} added!', 'success')
        return redirect(url_for('home'))
    return render_template('addMedication.html', title='Add a Medication', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # To add logic based on login type
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Welcome to', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
