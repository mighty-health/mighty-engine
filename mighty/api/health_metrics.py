from .. import model

from flask_restplus import Namespace, Resource, reqparse, fields

ns = Namespace(name='health_metrics',
               description='Operations related to health metrics')

parser = ns.parser()
parser.add_argument('patient_id',
                    type=str,
                    required=True,
                    help='Unique patient identifier')

metric_reading = ns.model('Reading', {
    'date': fields.String(description='Reading date'),
    'value': fields.String(description='Reading value'),
    'unit': fields.String(description='Reading unit'),
})

health_metric = ns.model('Health Metric', {
    'title': fields.String(required=True, description='Title'),
    'status': fields.String(required=True, description='Status'),
    'category': fields.String(description='Category'),
    'readings': fields.List(fields.Nested(metric_reading)),
    'rank': fields.Integer(description='Relevance rank'),
    'description': fields.String(description='Description'),
})

@ns.route('/')
class HealthMetricList(Resource):
    @ns.response(404, 'Patient not found.')
    @ns.response(201, 'Successfully retrieved HealthMetricList.')
    @ns.expect(parser)
    @ns.marshal_with(health_metric)
    def get(self):
        """
        Returns relevant health metrics for the given patient.

        Test the endpoint with this sample patient_id:
        a33d3135-2c7a-43ad-8804-3c2d3f492253
        """

        args = parser.parse_args()
        result = model.get_health_metrics(patient_id=args['patient_id'])
        if result is None:
            ns.abort(404, 'Patient not found.')
        else:
            return result, 201
