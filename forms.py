from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=8, max=80)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(
            username=username.data
        ).first()
        if existing_username:
            raise ValidationError(
                "That username already exists. Please choose a different one"
            )


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()], render_kw={"placeholder": "Username"},)
    password = PasswordField("Password", validators=[InputRequired()], render_kw={"placeholder": "Password"},)
    submit = SubmitField("Login")
