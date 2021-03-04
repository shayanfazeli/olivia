from flask import Blueprint, render_template
from app.blueprints.hate_speech_monitor.forms import HateSpeechMonitorForm
from app.libraries.queries import get_tweets_df_from_table1
from erlab_coat.meta import label2description
from app import db, application_directory
import json
import os
import pandas
import plotly
import plotly.express as px
import numpy
import gc
from flask import jsonify, Response
from app.libraries.plotly_wordcloud import plotly_wordcloud

hate_speech_monitor_blueprint = Blueprint("hate_speech_monitor", __name__)


def get_hate_speech_monitor_data(mode, start_date, end_date, place_filter):
    graphJSON = {}
    layout = {}
    info_list = []
    # df = pandas.read_csv(os.path.join(application_directory, 'static/sample_hate_monitor.csv'), lineterminator='\n')
    # df.date = df.date.apply(lambda x: x.split(' ')[0])
    #
    # df = df[df.date >= str(start_date)]
    # df = df[df.date <= str(end_date)]

    df = get_tweets_df_from_table1(
        db=db,
        place_names=place_filter,
        min_date=str(start_date),
        max_date=str(end_date)
    )

    if mode.startswith('hate_'):
        df = df[df.hate_prob > 0.5]
    else:
        raise NotImplementedError

    def is_in_filter(x, place_filter):
        x = x.lower()
        if len(place_filter) == 0:
            return True
        else:
            for p in place_filter:
                if x in p:
                    return True
            return False

    # - filtering places
    #df = df[df.place_name.apply(lambda x: is_in_filter(x, place_filter=place_filter))]

    if mode == 'hate_wordcloud':
        text = " ".join(df.text.tolist())
        figure = plotly_wordcloud(text)
        figure.update_layout(template='plotly_white')
        graphJSON = json.dumps(figure.data, cls=plotly.utils.PlotlyJSONEncoder)
        layout = json.dumps(
            figure.layout, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON, layout, info_list
    elif mode in ['hate_top_tweets_china', 'hate_top_tweets']:
        df = df.sort_values(by=['hate_prob'], ascending=False)
        if mode == 'hate_top_tweets_china':
            df = df[df.text.apply(lambda x: 'china' in x.lower() or 'chinese' in x.lower())]
        info_list = []
        for i in range(min(10, df.shape[0])):
            info_list.append(
                {x: dict(df.iloc[i])[x] for x in ['text', 'date', 'place_name']}
            )
        return graphJSON, layout, info_list
    elif mode == 'hate_place_statistics':
        df = df.groupby('place_name').count().sort_values(by='text', ascending=False).reset_index()
        df = df.loc[:, ['place_name', 'text']]

        if len(place_filter) == 0:
            df = df.iloc[:10]

        df.rename({'text': 'count'}, inplace=True, axis=1)
        fig = px.bar(df, x='place_name', y='count', color='count')
        fig.update_layout(yaxis_title='Count', xaxis_title='Place', template='plotly_white')
        fig.layout.font.size = 15
        graphJSON = json.dumps(fig.data, cls=plotly.utils.PlotlyJSONEncoder)
        layout = json.dumps(
            fig.layout, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON, layout, info_list
    elif mode == 'hate_trends':
        df.date = df.date.apply(lambda x: str(x).split(' ')[0])
        df = df.groupby(['place_name', 'date']).count().reset_index()
        df = df.loc[:, ['place_name', 'date', 'text']]

        df.rename({'text': 'count'}, inplace=True, axis=1)

        fig = px.scatter(df, x='date', y='count', color='place_name')
        for i in range(len(fig.data)):
            fig.data[i].update(mode='lines+markers')
        fig.update_layout(template='plotly_white', xaxis_title='Date', yaxis_title='Tweet Count',
                          legend_title="Place")
        graphJSON = json.dumps(fig.data, cls=plotly.utils.PlotlyJSONEncoder)
        layout = json.dumps(
            fig.layout, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON, layout, info_list
    else:
        raise NotImplementedError


@hate_speech_monitor_blueprint.route('/hate_speech_monitor', methods=['GET', 'POST'])
def hate_speech_monitor():
    form = HateSpeechMonitorForm()
    mode = 'reset'
    graphJSON = {}
    layout = {}
    info_list = []

    if form.validate_on_submit():
        mode = form.action_choice.data
        start_date = form.min_date.data
        end_date = form.max_date.data
        place_filter = [e.strip().lower() for e in form.place_filter.data.split(',') if not e == '']

        graphJSON, layout, info_list = get_hate_speech_monitor_data(mode, start_date, end_date, place_filter)

        return render_template(
            'hate_speech_monitor/palette.html',
            form=form, data=graphJSON, layout=layout, mode=mode, info_list=info_list
        )

    return render_template(
        'hate_speech_monitor/palette.html',
        form=form, data={}, layout={}, mode=mode
    )


@hate_speech_monitor_blueprint.route('/most_hateful_tweets', methods=['GET', 'POST'])
def most_hateful_tweets():
    df = pandas.read_csv(os.path.join(application_directory, 'static/sample_hate_monitor.csv'))

    return render_template('hate_speech_monitor/top_tweets.html', df=df)
