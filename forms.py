from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
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


class ItemForm(FlaskForm):
    """Form for custom Item"""
    item_name = StringField('Name')
    rarity = StringField('Rarity')
    requires_attunement = StringField('Requires Attunement')
    text = StringField('Text')
    type = StringField('Type')
