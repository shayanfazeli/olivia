from flask import Blueprint, render_template
from app.blueprints.regional_comparisons.forms import RegionalComparisonForm
from app.libraries.queries import get_df_of_all_features_for_two_region_groups, process_for_d3_json, \
    process_for_d3_json_ultrafast
from erlab_coat.meta import label2description
from app import db, application_directory
import json
import pandas
import numpy
import gc
from flask import jsonify, Response

regional_comparisons_blueprint = Blueprint("regional_comparisons", __name__)


@regional_comparisons_blueprint.route('/regional_comparisons', methods=['GET', 'POST'])
def regional_comparisons():
    form = RegionalComparisonForm()

    if form.validate_on_submit():
        var = form.var.data
        county_filter1_data = form.county_filter1.data
        state_filter1_data = form.state_filter1.data
        start_date1 = form.start_date1.data
        end_date1 = form.end_date1.data

        county_filter2_data = form.county_filter2.data
        state_filter2_data = form.state_filter2.data
        start_date2 = form.start_date2.data
        end_date2 = form.end_date2.data

        bin_count = int(form.bin_count.data)

        df = get_df_of_all_features_for_two_region_groups(
            db,
            var,
            county_filter1_data,
            state_filter1_data,
            start_date1,
            end_date1,
            county_filter2_data,
            state_filter2_data,
            start_date2,
            end_date2
        )

        if form.prepare_json.data == 'yes':
            statistics_json = []
            for var in label2description.keys():
                skip_flag = False
                for skip_name in ['physical_activity', 'alcohol', 'life_expectancy', 'diabetes']:
                    if var.startswith(skip_name):
                        skip_flag = True
                if skip_flag:
                    continue
                try:
                    df = get_df_of_all_features_for_two_region_groups(
                        db,
                        var,
                        county_filter1_data,
                        state_filter1_data,
                        start_date1,
                        end_date1,
                        county_filter2_data,
                        state_filter2_data,
                        start_date2,
                        end_date2
                    )

                    tmp_element = {'feature': label2description[var],
                                   'group1': {
                                       'mean': df.loc[df.type == 'region_group1', var].mean(),
                                       'median': df.loc[df.type == 'region_group1', var].median(),
                                       'min': df.loc[df.type == 'region_group1', var].min(),
                                       'max': df.loc[df.type == 'region_group1', var].max(),
                                       'std': df.loc[df.type == 'region_group1', var].std()},
                                   'group2': {
                                       'mean': df.loc[df.type == 'region_group2', var].mean(),
                                       'median': df.loc[df.type == 'region_group2', var].median(),
                                       'min': df.loc[df.type == 'region_group2', var].min(),
                                       'max': df.loc[df.type == 'region_group2', var].max(),
                                       'std': df.loc[df.type == 'region_group2', var].std()}
                                   }
                    tmp_element['distance'] = abs(
                        (tmp_element['group1']['mean'] - tmp_element['group2']['mean']) / (
                                tmp_element['group1']['std'] + tmp_element['group2']['std']))
                    if not numpy.isnan(tmp_element['distance']):
                        statistics_json.append(tmp_element)
                        del tmp_element
                        gc.collect()
                except Exception as e:
                    continue

            statistics_json = sorted(statistics_json, key=lambda x: x['distance'], reverse=True)
            return render_template('results/group_comparison_statistics.html', results=statistics_json)
        else:
            statistics_json = []

        df = df.loc[:, ['type', var]]

        chart_data = df.to_dict(orient='records')
        chart_data = json.dumps(chart_data, indent=2)

        return render_template(
            'regional_group_differences/palette.html',
            form=form,
            feature=var,
            feature_description=label2description[var],
            comparison_data=chart_data,
            bin_count=bin_count,
            statistics_json=statistics_json
        )

    return render_template(
        'regional_group_differences/palette.html',
        form=form,
        feature='',
        feature_description='',
        var='',
        comparison_data='',
        bin_count=50,
        statistics_json=[]
    )
