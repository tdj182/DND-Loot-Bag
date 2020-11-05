from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import required, Email, Length


class SearchForm(FlaskForm):
    """Form for adding/editing messages."""

    search = StringField('Search Item', validators=[required()])