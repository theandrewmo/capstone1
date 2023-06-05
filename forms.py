from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """ Form for adding users """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])
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

class ReviewForm(FlaskForm):
    """ Form for reviewing a brewery """

    rating = SelectField('Rating', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    photo_url = HiddenField('Photo URL')
    photo_file = FileField('Photo', render_kw={"onchange": "uploadImage(event)",'accept': 'image/*'})

class ForgotPasswordForm(FlaskForm):
    """ Form for fixing a forgotten password"""

    email = StringField('Email', validators=[DataRequired(), Email()])

class NewPasswordForm(FlaskForm):
    """ Form for adding new password"""

    new_password = PasswordField('New Password', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[Length(min=6), DataRequired()])


    