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

        df, sorted_counties, sorted_states = get_df_for_county_scoring(
            db,
            focus_cases=focus_cases,
            focus_deaths=focus_deaths,
            focus_recoveries=focus_recoveries,
            max_date=str(form.max_date.data),
            min_date=str(form.min_date.data),
            normalize=True
        )

        fips = pandas.read_csv(os.path.join(application_directory, 'static/fips_choropleth.csv'))
        df = pandas.merge(left=df, right=fips, on=['county', 'state'], how='outer')
        df['score'] = df['score'].fillna('Insufficient Data')
        cols_to_delete = []
        for column in df.columns:
            if column.startswith('level_'):
                cols_to_delete.append(column)
        df.drop(columns=cols_to_delete, inplace=True)
        df.dropna(inplace=True)

        df.fips = df.fips.apply(lambda x: int(x))
        df.rename({'score': 'score_value', 'county': 'area_name'}, inplace=True, axis=1, errors='raise')

        def rounder(x):
            try:
                return round(float(x), 2)
            except:
                return x
        df.score_value = df.score_value.apply(rounder)
        chart_data = df.to_dict(orient='records')
        chart_data = json.dumps(chart_data, indent=2)
        return render_template(
            'regional_scoring/palette.html',
            form=form,
            chart_data=chart_data,
            sorted_counties=sorted_counties,
            sorted_states=sorted_states
        )

    return render_template(
        'regional_scoring/palette.html',
        form=form,
        chart_data=''
    )
