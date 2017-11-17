from flask import Blueprint
from flask_restplus import Api
from .immunizations import ns as immunizations_namespace

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(
    app=blueprint,
    title='Mighty Engine API',
    version='1.0',
    description='A RESTful API for the Mighty Engine',
)

api.add_namespace(immunizations_namespace)
