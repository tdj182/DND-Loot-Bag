from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import Required, Email, Length


class SearchForm(FlaskForm):
    """Form for adding/editing messages."""

    search = StringField('Search Item', validators=[Required()])


class UserForm(FlaskForm):
    """Form for adding users"""

    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LootbagForm(FlaskForm):
    """Form for a new loot bag"""
    name = StringField('Name', validators=[Required()])
    password = PasswordField('Password')
    is_shareable = BooleanField('Is Shareable?',  validators=[Required()])


class ItemForm(FlaskForm):
    """Form for custom Item"""
    item_name = StringField('Name')
    rarity = StringField('Rarity')
    requires_attunement = StringField('Requires Attunement')
    text = StringField('Text')
    type = StringField('Type')


class LootbagLoginForm(FlaskForm):
    """Form for adding users"""

    password = PasswordField('Password')
