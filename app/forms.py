from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, DateTimeField, \
    PasswordField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
# from app.models import Artist, Venue, User


# class ContactUsForm(FlaskForm):
#     email = StringField('Email Address:', validators=[DataRequired(), Email()])
#     subject = StringField('Email Subject:', validators=[DataRequired()])
#     feedback = TextAreaField('Feedback/Query:', validators=[DataRequired()])
#     submit = SubmitField('Submit')
