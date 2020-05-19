from flask import Blueprint, render_template
from app import application_directory
import os
import pandas

tweets_blueprint = Blueprint("tweets", __name__)


@tweets_blueprint.route('/tweets', methods=['GET', 'POST'])
def tweets_of_the_day():
    df = pandas.read_csv(os.path.join(application_directory, 'static/tweets/tweets.csv'))
    return render_template('tweets/covid_tweets.html', df=df)
