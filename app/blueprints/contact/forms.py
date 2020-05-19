from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import NumberRange, DataRequired, Email
import email_validator
import operator
from erlab_coat.meta import label2description


class SendFindingForm(FlaskForm):
    email = TextAreaField("Your Email", validators=[DataRequired(), Email()])
    finding_title = TextAreaField("Finding Title", validators=[DataRequired()])
    explanation = TextAreaField("Explanation", validators=[DataRequired()])
    reproduce_instructions = TextAreaField("How to Reproduce Your Results", validators=[DataRequired()])
    submit = SubmitField("Submit")