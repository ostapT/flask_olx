import os

from dotenv import load_dotenv
from flask import Flask, request, redirect, render_template, url_for
from flask_login import login_user, LoginManager, login_required
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from forms import LoginForm, RegistrationForm
from models import User, db
from olx_scraper import parse_urls, process_ads


load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
            else:
                return render_template(
                    "login.html",
                    error="Invalid username or password",
                    form=form
                )
            return redirect(url_for("update_ads"))
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            request.form["password"]
        )
        hashed_password_str = hashed_password.decode('utf-8')
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            return render_template(
                "register.html",
                error="That username already exists.",
            )
        new = User(username=form.username.data, password=hashed_password_str)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/update_ads", methods=["GET", "POST"])
@login_required
def update_ads():
    if request.method == "POST":
        links = parse_urls()
        ads_data = process_ads(links)
        return render_template("ads.html", ads_data=ads_data)
    elif request.method == "GET":
        return render_template("base.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
