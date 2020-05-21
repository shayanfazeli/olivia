__author__ = ["Shayan Fazeli"]
__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

from typing import Dict
import os
from app.libraries.queries import get_data_for_query
from app import create_app, db, application_directory
from app.libraries.database_manipulation import populate_database_with_glance
from app.entities import Election
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
    return {'db': db, 'Election': Election, 'populate_database_with_glance': populate_database_with_glance,
            'get_data_for_query': get_data_for_query}


if __name__ == "__main__":
    app.run()
