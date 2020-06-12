__author__ = ["Shayan Fazeli"]
__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

from typing import Dict
import os
from app.libraries.queries import get_data_for_query
from app import create_app, db, application_directory
from app.libraries.database_manipulation import populate_database_with_glance, update_dynamic_tables
from app.libraries.queries import get_df_for_county_scoring
from app.entities import Election, GoogleMobility, Cases
from flask import redirect, send_from_directory

app = create_app()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application_directory, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.shell_context_processor
def make_shell_context():
    """
    The :func:`make_shell_context` build the flask shell context given the current entities.
    It can be called by running `flask shell` in the application root directory.
    Returns
    ----------
    The output of this method is a `Dict` type including the entities and methods to be used in shell
    """
    return {'db': db, 'Election': Election, 'GoogleMobility': GoogleMobility, 'Cases': Cases, 'populate_database_with_glance': populate_database_with_glance, 'update_dynamic_tables': update_dynamic_tables,
            'get_data_for_query': get_data_for_query, 'get_df_for_county_scoring': get_df_for_county_scoring}


if __name__ == "__main__":
    app.run()
