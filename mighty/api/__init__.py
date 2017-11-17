from flask import Blueprint
from flask_restplus import Api
from .summary import ns as summary_namespace
from .immunizations import ns as immunizations_namespace
from .screenings import ns as screenings_namespace
from .health_metrics import ns as health_metrics_namespace

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(
    app=blueprint,
    title='Mighty Engine API',
    version='1.0',
    description='A RESTful API for the Mighty Engine',
)
api.add_namespace(summary_namespace)
api.add_namespace(immunizations_namespace)
api.add_namespace(screenings_namespace)
api.add_namespace(health_metrics_namespace)
