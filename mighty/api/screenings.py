from .. import model

from flask_restplus import Namespace, Resource, reqparse, fields

ns = Namespace(name='screenings',
               description='Operations related to screenings')

parser = ns.parser()
parser.add_argument('patient_id',
                    type=str,
                    required=True,
                    help='Unique patient identifier')

screening_observation = ns.model('Observation', {
    'name': fields.String(description='Observation name'),
    'value': fields.String(description='Observation value'),
    'unit': fields.String(description='Observation unit'),
})

screening = ns.model('Screening', {
    'title': fields.String(required=True, description='Title'),
    'status': fields.String(required=True, description='Status'),
    'timing': fields.String(description='Timing'),
    'due_date': fields.String(description='Due Date'),
    'most_recent_date': fields.String(description='Most Recent Date'),
    'observations': fields.List(fields.Nested(screening_observation)),
    'rank': fields.Integer(description='Relevance rank'),
    'description': fields.String(description='Description'),
})

@ns.route('/')
class ScreeningChecklist(Resource):
    @ns.response(404, 'Patient not found.')
    @ns.response(201, 'Successfully retrieved ScreeningChecklist.')
    @ns.expect(parser)
    @ns.marshal_with(screening)
    def get(self):
        """
        Returns the screening checklist for the given patient.

        Test the endpoint with this sample patient_id:
        a33d3135-2c7a-43ad-8804-3c2d3f492253
        """

        args = parser.parse_args()
        result = model.get_screening_checklist(patient_id=args['patient_id'])
        if result is None:
            ns.abort(404, 'Patient not found.')
        else:
            return result, 201
