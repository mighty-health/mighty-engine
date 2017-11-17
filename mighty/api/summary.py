from .. import model

from flask_restplus import Namespace, Resource, reqparse, fields

ns = Namespace(name='summary',
               description='Operations related to the home page summary')

parser = ns.parser()
parser.add_argument('patient_id',
                    type=str,
                    required=True,
                    help='Unique patient identifier')

reminder = ns.model('Reminder', {
    'title': fields.String(description='Reminder title'),
    'type': fields.String(description='Reminder type'),
    'due_date': fields.String(description='Reminder due date'),
})

summary = ns.model('Summary', {
    'total_immunizations': fields.Integer(description='Total Immunizations'),
    'completed_immunizations': fields.Integer(description='Completed Immunizations'),
    'total_screenings': fields.Integer(description='Total Screenings'),
    'completed_screenings': fields.Integer(description='Completed Screenings'),
    'reminders': fields.List(fields.Nested(reminder)),
})

@ns.route('/')
class Summary(Resource):
    @ns.response(404, 'Patient not found.')
    @ns.response(201, 'Successfully retrieved Summary.')
    @ns.expect(parser)
    @ns.marshal_with(summary)
    def get(self):
        """
        Returns the home page summary for the given patient.

        Test the endpoint with this sample patient_id:
        a33d3135-2c7a-43ad-8804-3c2d3f492253
        """

        args = parser.parse_args()
        result = model.get_summary(patient_id=args['patient_id'])
        if result is None:
            ns.abort(404, 'Patient not found.')
        else:
            return result, 201
