from flask import Blueprint, render_template
from app.blueprints.regional_visualizations.forms import CoatPlotD3Form
from app.libraries.queries import get_data_for_query, process_for_d3_json
from erlab_coat.meta import label2description
from app import db, application_directory

regional_visualizations_blueprint = Blueprint("regional_visualizations", __name__)


@regional_visualizations_blueprint.route('/regional_visualizations', methods=['GET', 'POST'])
def regional_visualization():
    json_data = ''
    form = CoatPlotD3Form()

    if form.validate_on_submit():
        t_var = 'day_of_the_year'
        x_var = form.x_var.data
        y_var = form.y_var.data
        color_var = form.color_var.data
        size_var = form.size_var.data
        show_labels = form.show_labels.data

        county_filter_data = form.county_filter.data
        state_filter_data = form.state_filter.data

        resolution = form.resolution.data

        df = get_data_for_query(
            db,
            color_var,
            x_var,
            y_var,
            size_var,
            county_filter=county_filter_data,
            state_filter=state_filter_data,
            resolution=resolution,
            interpolate=True
        )

        json_data = process_for_d3_json(df)

        return render_template(
            'regional_visualizations/palette.html',
            form=form,
            json_data=json_data,
            x_var=label2description[x_var],
            y_var=label2description[y_var],
            color_var=label2description[color_var],
            size_var=label2description[size_var],
        )

    return render_template(
        'regional_visualizations/palette.html',
        form=form,
        json_data=json_data
    )

