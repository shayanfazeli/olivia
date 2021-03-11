__author__ = ["Shayan Fazeli"]
__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

from typing import Dict
import os
from app.libraries.queries import get_data_for_query
from app import create_app, db, application_directory
from app.libraries.database_manipulation import populate_database_with_glance, update_dynamic_tables, update_tweet_table_1_from_local_csv, update_police_shooting_per_month_table, kff_vaccine_data

from app.entities import Election, GoogleMobility, Cases
from flask import redirect, send_from_directory

application = create_app()


@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application_directory, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@application.shell_context_processor
def make_shell_context():
    """
    The :func:`make_shell_context` build the flask shell context given the current entities.
    It can be called by running `flask shell` in the application root directory.
    Returns
    ----------
    The output of this method is a `Dict` type including the entities and methods to be used in shell
    """
    return {
        'db': db,
        'Election': Election,
        'GoogleMobility': GoogleMobility,
        'Cases': Cases,
        'populate_database_with_glance': populate_database_with_glance,
        'update_dynamic_tables': update_dynamic_tables,
        'get_data_for_query': get_data_for_query,
        'update_tweet_table_1_from_local_csv': update_tweet_table_1_from_local_csv,
        'update_police_shooting_per_month_table': update_police_shooting_per_month_table,
        'kff_vaccine_data': kff_vaccine_data}


if __name__ == "__main__":
    application.run()
