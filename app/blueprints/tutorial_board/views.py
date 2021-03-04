from flask import Blueprint, render_template
from app.blueprints.tutorial_board.forms import TutorialBoardForm
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

tutorial_board_blueprint = Blueprint("tutorial_board", __name__)


def get_data_for_choice(choice: str):
    if choice == 'spatiotemporal_trends_and_variables':
        return 'Spatio-Temporal Trends', [
            ('title', 'Spatio-temporal Trends of the COVID-19'),
            ('text', """
                    By clicking on the <b>Spatio-temporal COVID-19 Outbreak Monitor</b> you will get to the following page:
                    """),
            ('image', 'spatiotemporal_trends/1.png'),
            ('text', """
                    The first step in rendering the plots to monitor the spatio-temporal patterns of the COVID-19
                    pandemic and its related variables, is to pick the corresponding variable names for X, Y, and
                    datapoint color and size. This scheme is designed so as to shed light on the inter-variable dynamics
                    as time progresses.
                    """),
            ('image', 'spatiotemporal_trends/2.png'),
            ('text', """
                    The next step is to choose whether you want to see the datapoints with their labels, or just the
                    circles indicating the datapoints. If you want to see the location (e.g. 'CA' or 'Los Angeles_CA'), 
                    please choose so in the "Region Labels" field:
                    """),
            ('image', 'spatiotemporal_trends/3.png'),
            ('text', """
                    OLIVIA platform focuses on US counties. You have two options for the visualization resolutions, which
                    are either to look at each county individually, or to aggregate the information for the counties within a state. <br>
                    If you consider state resolution, the values you see are the county-aggregates on the counties that
                    have COVID-19 related values for the date of focus. 
                    """),
            ('image', 'spatiotemporal_trends/4.png'),
            ('text', """
                            You can write values in the state and county filters shown below. If nothing is inserted,
                            the entire corpus will be considered and processed which might lead to computationally
                            heavy graphs that take too long to load. You can use the filters in combination and
                            choose a set of counties within a set of states, and so on:
                            """),
            ('image', 'spatiotemporal_trends/5.png'),
            ('text', """
                        Finally, you can plot the dynamic graph and by using the slider on the bottom-right, see the patterns through time
                        and at any point. Please note that interpolation has also taken place in preparing the data for the
                        dynamic visualization.
                        """),
            ('image', 'spatiotemporal_trends/6.png'),
            ('text', """
                                Thank you
                                """),
        ]
    elif choice == "region_group_comparison":
        return "Region-Group Comparison", [
            ("title", "Comparing Characteristics of Region-Groups Across Time"),
            ("text", """
            Let's say you have formed a hypothesis that a group of regions during a timespan,
            and another group of regions during the same or another timespan, can be compared to
            reveal important information on the difference and similarities between their characteristics.
            To do so, by clicking on the <b>Region-Group Comparison Platform</b> you will
            be directed to the following platform:
            """),
            ("image", 'region_group_comparison/1.png'),
            ("text", """
                    The first step is to pick a variable to do visual comparison. Also,
                    filtering region is similar to the platform for spatio-temporal trend monitoring, with
                    the difference that you have two instances in this form allowing you to
                    create two custom groups of regions:
                    """),
            ("image", 'region_group_comparison/2.png'),
            ("text", """
                    For many reasons, you might be interested in choosing different time domains
                    for comparing two region groups:
                            """),
            ("image", 'region_group_comparison/3.png'),
            ("text", """
                        The histogram of the chosen variable will be shown with the counts
                        being the number of <county_date> keys that satisfy the chosen criteria. Bin-count
                        has to do with the final plot.
                            """),
            ("image", 'region_group_comparison/4.png'),
            ("image", 'region_group_comparison/6.png'),
            ("text", """
    `               If you choose to generate automatic report, the system will compare the region
    groups in the given time-domain, and show to you the variables that it computes as likely to be different, sorted
    by most different to least. Please note that given the difference in domains and nature of variables, this
    is an estimate and human supervision in the end is required.
                            """),
            ("image", 'region_group_comparison/5.png'),
            ("text", """
                    The automatically generated report looks like this:
                            """),
            ("image", 'region_group_comparison/7.png')
        ]
    elif choice == "hate_speech_monitor":
        return "Hate Speech Monitor", [
            ("title", "Monitoring Hateful Tweets"),
            ("text", """
            This platform is a prototype demonstrating the fact that the information from the social media
            platforms such as twitter can be leveraged. Currently, we have included 10,000 tweets
            in our database obtained recently just to showcase how the information can
            be visualized in the system. The interface is shown below:
            """),
            ('image', "hate_speech_monitor/1.png"),
            ("text", """
                    Using filtering on the places returned by twitter, daily trends such as the number of
                    tweets received that were considered hateful can be shown (such as the figure below):
                    """),
            ('image', "hate_speech_monitor/2.png"),
            ("text", """
                    The platform also allows showing most hateful tweets such as the following outputs:
                    """),
            ('image', "hate_speech_monitor/3.png"),
            ("text", """
                    Different regions within a filter (or all regions if no filter is applied) can be compared. Please note that currently,
                    the number indicates the number of tweets and is not normalized by the amount received from the
                    region. These modification can easily be included.
                    """),
            ('image', "hate_speech_monitor/4.png"),
            ("text", """
                            It is also possible to see the word-cloud of the tweets within the filtered region/timespan group.
                            """),
            ('image', "hate_speech_monitor/5.png"),
        ]
    elif choice == "region_scoring":
        return "Regional Scoring", [
            ("title", "Scoring different regions"),
            ("text", """
            For many applications, it is required to show the scores on the regions. In the following tool,
            you can choose a date range and choose a level of focus on case/death/recovery.
            This computes a score regarding how well a region was doing, given its starting condition in
            the given timespan, in terms of controling the values. This is a demonstration for how region-scores
            can be shown in our platform.
            """),
            ('image', 'region_scoring/1.png'),
            ('image', 'region_scoring/2.png')

        ]
    else:
        raise NotImplementedError


@tutorial_board_blueprint.route('/tutorial_board', methods=['GET', 'POST'])
def tutorial_board():
    form = TutorialBoardForm()

    if form.validate_on_submit():
        choice = form.choice.data
        tutorial_title, tutorial_info_list = get_data_for_choice(choice=choice)
        return render_template(
            'tutorials/palette.html',
            tutorial_title=tutorial_title,
            tutorial_info_list=tutorial_info_list
        )

    return render_template(
        'tutorials/selector.html',
        form=form
    )


