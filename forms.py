from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """ Form for adding users """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=([Length(min=6)]))
    city = StringField('City')
    state = SelectField('State')
    postal_code = StringField('Postal Code')
    fav_type = SelectField('Favorite Type')
                           
class LoginForm(FlaskForm):
    """ Form for logging in """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class SearchForm(FlaskForm):
    """ Form for searching breweries """

    term = StringField('Search Term')

class SearchTypeForm(FlaskForm):
    """ Form for choosing search type """

    search_type = SelectField('Search Type')