from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField,PasswordField,ValidationError
from wtforms.validators import Required, Email, Length, EqualTo
from wtforms.validators import Required

class LoginForm(FlaskForm):

    username = StringField("Username:", validators=[Required()])
    password = PasswordField("Password:", validators=[Required()])
    submit = SubmitField("login")

class EditPostForm(FlaskForm):

    title = StringField("", validators=[Required()])
    content = TextAreaField("", validators=[Required()])
    submit = SubmitField("post")


class SignUpForm(FlaskForm):

    name = StringField("Name:", validators=[Required()])
    username = StringField("Username:", validators=[Required()])
    email = StringField("Email:", validators=[Required(),Email()])
    password = PasswordField('Password', validators = [Required(),EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Password', validators = [Required()])
    submit  = SubmitField("signup")


    def validate_email(self, data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError("Sorry!..There is an account with that email")

    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError("Sorry!.. That username already exists")


class SubscribeForm(FlaskForm):

    email = StringField("Email:", validators=[Required(), Email()])
    submit = SubmitField("subscribe")


    def validate_email(self, data_field):
        if Subscribe.query.filter_by(email = data_field.data).first():
            raise ValidationError("Sorry! That Email has been Subscribed")