from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date
import operator
from app.blueprints.regional_visualizations.forms import fetch_latest_descriptions_for_choices


class RegionalScoringForm(FlaskForm):
    focus_cases = SelectField('Level of Focus on Cases', default='moderate', choices=[
        ('ignore', 'Ignore'),
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
    ])
    focus_deaths = SelectField('Level of Focus on Deaths', default='moderate', choices=[
        ('ignore', 'Ignore'),
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
    ])
    focus_recoveries = SelectField('Level of Focus on Recoveries', default='moderate', choices=[
        ('ignore', 'Ignore'),
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
    ])
    past_focus_factor = SelectField('Considering Historical Data', default='moderate', choices=[
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
    ])

    min_date = DateField("Start Date", validators=[DataRequired()])

    submit = SubmitField('Compute Scores')

    def validate(self):
        if not super(RegionalScoringForm, self).validate():
            return False

        return True
