__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credits__ = 'ER Lab - CS@UCLA'

# libraries
import os
from flask import Flask, render_template
from configurations import Configurations
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

application_directory = os.path.abspath(os.path.dirname(__file__))


def create_app(configuration_class: object = Configurations):
    """
    The :func:`create_app` is the most important method in this library. It starts
    by creating the application, preparing the context, initiating the security measures, etc.
    Parameters
    ----------
    configuration_class: `object`, optional (default=Configurations)
        The configuration is set in this method using an object, and the parameters are defined
        in the configuration object stored in `configurations.py`, which is the default value as well.
    Returns
    ----------
    This method returns the application context and the user datastore object
    """
    app = Flask(__name__)
    app.config.from_object(configuration_class)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    mail.init_app(app=app)
    from app.blueprints.regional_visualizations import regional_visualizations_blueprint
    app.register_blueprint(regional_visualizations_blueprint)
    from app.blueprints.regional_comparisons import regional_comparisons_blueprint
    app.register_blueprint(regional_comparisons_blueprint)
    from app.blueprints.regional_scoring import regional_scoring_blueprint
    app.register_blueprint(regional_scoring_blueprint)
    from app.blueprints.contact import contact_blueprint
    app.register_blueprint(contact_blueprint)
    from app.blueprints.tweets import tweets_blueprint
    app.register_blueprint(tweets_blueprint)
    from app.blueprints.main import main_blueprint
    app.register_blueprint(main_blueprint)
    from app.blueprints.results import results_blueprint
    app.register_blueprint(results_blueprint)

    @app.errorhandler(404)
    def error_404(e):
        # note that we set the 404 status explicitly
        return render_template('errors/error.html', error_code=404, error_message="Requested Page Was Not Found"), 404

    @app.errorhandler(500)
    def error_500(e):
        # note that we set the 404 status explicitly
        return render_template('errors/error.html', error_code=500,
                               error_message="Please Check Your Parameters and Try Again"), 500

    @app.errorhandler(502)
    def error_502(e):
        # note that we set the 404 status explicitly
        return render_template('errors/error.html', error_code=502,
                               error_message="Request Timeout"), 502

    @app.errorhandler(504)
    def error_504(e):
        # note that we set the 404 status explicitly
        return render_template('errors/error.html', error_code=500,
                               error_message="Request Timeout"), 504

    return app


from app.entities import Election