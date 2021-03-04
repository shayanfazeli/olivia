from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date


class HateSpeechMonitorForm(FlaskForm):
    action_choice = SelectField('Action', default='show_trends', choices=[
        ('hate_trends', 'Daily Trends'),
        ('hate_top_tweets', 'Most Hateful Tweets'),
        ('hate_top_tweets_china', 'Most Hateful Tweets Mentioning China'),
        ('hate_place_statistics', 'Place Statistics'),
        ('hate_wordcloud', 'Word Cloud of Hateful Tweets')
    ], validators=[])
    place_filter = TextAreaField('Places of Interest', validators=[])

    min_date = DateField("Start Date", validators=[DataRequired()])
    max_date = DateField("End Date", validators=[DataRequired()])

    submit = SubmitField('Compute Scores')

    def validate(self):
        if not super(HateSpeechMonitorForm, self).validate():
            return False

        def turn_to_date(x: str) -> date:
            tmp = str(x)
            date_parts = [int(e) for e in tmp.split('-')]
            return date(date_parts[0], date_parts[1], date_parts[2])

        start_date = turn_to_date(self.min_date.data)
        end_date = turn_to_date(self.max_date.data)

        date_delta = end_date - start_date

        if date_delta.days < 0:
            msg = "Please check the specified dates again."
            self.start_date.errors.append(msg)
            self.end_date.errors.append(msg)
            return False

        return True
