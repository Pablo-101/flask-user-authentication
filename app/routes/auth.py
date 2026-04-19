from flask import render_template, session, request, redirect, url_for, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return render_template("home.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        flash("You already logged in", "info")
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user"] = user.id
            flash("Logged in Successfully!", "success")
            return redirect(url_for("auth.dashboard"))

        flash("Username or Password is Incorrect", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if "user" in session:
        flash("You already logged in", "info")
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username.strip() or not password.strip():
            flash(
                "Username and password cannot be empty or contain only spaces.",
                "danger",
            )
            return redirect(url_for("auth.sign_up"))

        user = User.query.filter_by(username=username).first()

        if user:
            flash("Username already exists!", "danger")
            return redirect(url_for("auth.login"))

        passwordhash = generate_password_hash(password)
        user = User(username=username, password=passwordhash)
        db.session.add(user)
        db.session.commit()
        session["user"] = user.id
        flash("Account has been successfully created", "success")
        return redirect(url_for("auth.dashboard"))

    return render_template("sign_up.html")


@auth_bp.route("/dashboard")
def dashboard():
    if "user" in session:
        user = User.query.get(session["user"])
        return render_template("dashboard.html", username=user.username)
    else:
        flash("Login first", "warning")
        return redirect(url_for("auth.login"))


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    if "user" in session:
        if request.method == "POST":
            session.pop("user", None)
            flash("Logged Out", "success")
            return redirect(url_for("auth.login"))

        return redirect(url_for("auth.dashboard"))

    flash("You already Logged Out", "success")
    return render_template("home.html")


@auth_bp.route("/delete", methods=["GET", "POST"])
def delete():
    if "user" in session:
        user_id = session["user"]
        user = User.query.filter_by(id=user_id).first()
        if request.method == "POST":
            db.session.delete(user)
            db.session.commit()
            session.pop("user", None)
            flash("Account deleted successfully", "success")
            return redirect(url_for("auth.home"))
        else:
            return redirect(url_for("auth.dashboard"))

    else:
        flash("You need to login first", "warning")
        return redirect(url_for("auth.login"))
