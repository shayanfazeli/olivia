from flask import Blueprint, render_template
from app.blueprints.regional_scoring.forms import RegionalScoringForm
from app.libraries.queries import get_df_for_county_scoring
from erlab_coat.meta import label2description
from app import db, application_directory
import json
import os
import pandas
import numpy
import gc
from flask import jsonify, Response

regional_scoring_blueprint = Blueprint("regional_scoring", __name__)


@regional_scoring_blueprint.route('/regional_scoring', methods=['GET', 'POST'])
def regional_scoring():
    form = RegionalScoringForm()

    if form.validate_on_submit():
        def consideration_value(x: str) -> float:
            if x == 'ignore':
                return 0
            elif x == 'low':
                return 0.2
            elif x == 'moderate':
                return 0.5
            elif x == 'high':
                return 0.9
            else:
                raise ValueError

        focus_cases = consideration_value(form.focus_cases.data)
        focus_deaths = consideration_value(form.focus_deaths.data)
        focus_recoveries = consideration_value(form.focus_recoveries.data)
        past_focus_factor = consideration_value(form.past_focus_factor.data)

        df = get_df_for_county_scoring(
            db,
            focus_cases=focus_cases,
            focus_deaths=focus_deaths,
            focus_recoveries=focus_recoveries,
            past_focus_factor=past_focus_factor,
            min_date=str(form.min_date.data),
            normalize=True
        )

        fips = pandas.read_csv(os.path.join(application_directory, 'static/fips.csv'))
        df = pandas.merge(left=df, right=fips, on=['county', 'state'], how='outer').dropna()
        df.fips = df.fips.apply(lambda x: int(x))
        df.rename({'score': 'score_value', 'county': 'area_name'}, inplace=True, axis=1, errors='raise')
        df.drop(columns=['level_2'], inplace=True)
        chart_data = df.to_dict(orient='records')
        chart_data = json.dumps(chart_data, indent=2)
        return render_template(
            'regional_scoring/palette.html',
            form=form,
            chart_data=chart_data
        )

    return render_template(
        'regional_scoring/palette.html',
        form=form,
        chart_data=''
    )
