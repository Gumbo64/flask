from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
class registrationform(FlaskForm):
    username = StringField('_Username_', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('_Email_', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Equalto(password)])

    submitfield=SubmitField('Sign up')

class loginform(FlaskForm):
    email = StringField('_Email_', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember?')
    submitfield=SubmitField('Login')