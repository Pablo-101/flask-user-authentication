from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./user_pass.db"
db = SQLAlchemy(app)
app.secret_key = "123"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["user"] = username
            flash("Logged in Successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Username or Password is Incorrect", "danger")
            return redirect(url_for("login"))

    else:
        if "user" in session:
            flash("You already logged in", "info")
            return redirect(url_for("dashboard"))

        return render_template("login.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            session["user"] = username
            flash("Account has been successfully created", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Username already exists!", "danger")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("You already logged in", "info")
            return redirect(url_for("dashboard"))
        return render_template("sign_up.html")


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        username = session["user"]
        return render_template("dashboard.html", username=username)
    else:
        flash("Login first", "warning")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        flash("Logged Out", "success")
        return redirect(url_for("login"))

    else:
        return render_template("home.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
