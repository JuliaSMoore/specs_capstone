from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, TextAreaField, RadioField, ValidationError, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo
from model import User
import controller
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=50), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7, max=50)])
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=99)])
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=50), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7, max=50), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=7, max=50)])
    category = SelectField('Category', choices=[('Writer', 'Writer'), ('Reader', 'Reader')])
    submit = SubmitField('Register')

    def validate_email(self,email):
        if User.query.filter(email == self.email.data).first():
            raise ValidationError('Email has been registered')
        
    def validate_username(self, username):
        if User.query.filter(username == self.username.data).first():
            raise ValidationError('Username has been registered')


class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=50)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=50, max=1000)])
    image_url = StringField('Image')
    submit = SubmitField('Submit')

class CharacterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=50)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=50, max=1000)])
    image_url = StringField('Image')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    text = TextAreaField('Description', validators=[DataRequired(), Length(min=5, max=1000)])
    submit = SubmitField('Submit')

class RatingForm(FlaskForm):
    score = RadioField('Rate this request:', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    submit = SubmitField('Submit')


# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()

class AddTagsForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags.choices = [(tag.name, tag.name) for tag in controller.get_tags()]
    tags = SelectMultipleField('Tags')
    submit = SubmitField('Submit')

class AddCharactersForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.characters.choices = [(character.name, character.name) for character in controller.get_characters_by_created_id(current_user.id)]
    characters = SelectMultipleField('Characters')
    submit = SubmitField('Submit')