from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from datetime import date


class TutorialBoardForm(FlaskForm):
    choice = SelectField('Please select a tutorial to continue', default='spatiotemporal_trends_and_variables', choices=[
        ('spatiotemporal_trends_and_variables', 'Spatio-temporal Trends and Variables'),
        ('region_group_comparison', 'Region-Group Comparison'),
        ('region_scoring', 'Region Scoring'),
        ('hate_speech_monitor', 'Hate Speech Monitor')
    ], validators=[])

    submit = SubmitField('View')
