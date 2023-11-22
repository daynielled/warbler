from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class ProfileUpdateForm(FlaskForm):
    """Form for updating user profile."""

    bio = TextAreaField('Bio', validators=[Length(max=160)])  # Adjust the maximum length as needed
    location = StringField('Location', validators=[Length(max=100)])  # Adjust the maximum length as needed
    header_image_url = StringField('Header Image URL', validators=[DataRequired(), Length(max=255)])  # Adjust the maximum length as needed