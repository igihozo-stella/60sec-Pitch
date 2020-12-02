from flask_wtf import FlaskForm
from wtforms.validators import Required, Email, Length, EqualTo
from wtforms import StringField, TextAreaField, SubmitField, PasswordField


class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[Required()])
    password = PasswordField('Password', validators = [Required()])
    submit  = SubmitField("login")


class BioForm(FlaskForm):
    bio= TextAreaField("Edit your bio here...", validators=[Required(),Length(max=200)])
    submit = SubmitField("post")


class PostForm(FlaskForm):
    title = StringField("", validators=[Required()])
    content = TextAreaField("", validators=[Required()])
    submit = SubmitField("post")