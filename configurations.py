__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credits__ = 'ER Lab - CS@UCLA'

# libraries
import os
from dotenv import load_dotenv

# preparing some inner variables
base_directory = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_directory, '.env'))


class Configurations(object):
    """
    The :class:`Configurations` holds the main configuration parameters used in ViSierra. The main
    configurations worth mentioning are the secret key which is used mainly in the authentication blueprint, and
    the database parameters especially where the SQLite database is to be saved.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'visierra_is_secret_Key23'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_directory, 'visierra_database.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql+auroradataapi://olivia:erlab391@olivia-db.cluster-ce8jt52rjpad.us-west-2.rds.amazonaws.com:3306/olivia'

    SQLALCHEMY_DATABASE_URI = 'postgresql://oliviaadmin:erlab391@oliviadbstaging2-cluster.cluster-ro-ce8jt52rjpad.us-west-2.rds.amazonaws.com/olivia'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://oliviaadmin:erlab391@oliviadbstaging2-cluster.cluster-ce8jt52rjpad.us-west-2.rds.amazonaws.com/olivia'

    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     "connect_args": {
    #         "aurora_cluster_arn": "arn:aws:rds:us-west-2:014105426514:cluster:oliviadb",
    #         "secret_arn": "arn:aws:secretsmanager:us-west-2:014105426514:secret:oliviadb"
    #     }
    # }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ['shayan@cs.ucla.edu']
    LANGUAGES = ['en']
