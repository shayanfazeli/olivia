from flask import Blueprint, render_template
from app.blueprints.regional_comparisons.forms import RegionalComparisonForm
from app.libraries.queries import get_df_of_all_features_for_two_region_groups, process_for_d3_json, process_for_d3_json_ultrafast
from erlab_coat.meta import label2description
from app import db, application_directory
import json

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

        df = df.loc[:, ['type', var]]

        chart_data = df.to_dict(orient='records')
        chart_data = json.dumps(chart_data, indent=2)

        return render_template(
            'regional_group_differences/palette.html',
            form=form,
            feature=var,
            feature_description=label2description[var],
            comparison_data=chart_data,
            bin_count=bin_count
        )

    return render_template(
        'regional_group_differences/palette.html',
        form=form,
        feature='',
        feature_description='',
        var='',
        comparison_data='',
        bin_count=50
    )

