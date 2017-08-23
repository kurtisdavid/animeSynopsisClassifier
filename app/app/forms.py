from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    anime_link = StringField('openid', validators=[DataRequired()])