from wsgiref.validate import validator
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from App.models import User


class LoginForm(FlaskForm): #creates a login form class inheriting from flask form
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm): #creates a register form class inheriting from flask form
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)]) #make a username - has to be between 4 and 50 characters
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)]) #make a password - has to be between 4 and 50 characters
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username): #Checks if the username is already in use
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already in use. Please choose another one.')

    def validate_email(self, email): #checks if the email is already in use
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already in use. Please choose another one.')

class EditProfileForm(FlaskForm): #creates a edit profile form class inheriting from flask form
    username = StringField('Username', validators=[DataRequired()])
    about_me = StringField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username): #Checks if username is already in use if it is attempting to be changed
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('This username is already in use. Please choose another one')

class ResetPasswordRequestForm(FlaskForm): #creates a reset password request form class inheriting from flask form
    email= StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm): #creates a reset password form class inheriting from flask form
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Request Password Reset')

class UploadForm(FlaskForm): #creates a upload form class inheriting from flask form
    title = StringField('Title', validators=[DataRequired()])
    key = StringField('Key', validators=[DataRequired()])
    bpm = StringField('Bpm', validators=[DataRequired()])
    timeSignature = StringField('Time Signature', validators=[DataRequired()])
    file = FileField('File', validators=[DataRequired()]) #FileRequired(), FileAllowed(files)
    submit=SubmitField('Upload')