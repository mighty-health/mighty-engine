from .. import model
from flask import request
from flask_restplus import Namespace, Resource, reqparse, fields
import sys
import traceback

ns = Namespace(name='immunizations',
               description='Operations related to immunizations')

parser = ns.parser()
parser.add_argument('patient_id',
                    type=str,
                    required=True,
                    help='Unique patient identifier')

immunization = ns.model('Immunization', {
    'title': fields.String(required=True, description='Title'),
    'subtitle': fields.String(description='Subtitle'),
    'timing': fields.String(required=True, description='Timing'),
    'due_date': fields.String(required=True, description='Due Date'),
    'prior_dates': fields.List(fields.String(), description='Prior Date'),
    'status': fields.String(required=True, description='Status'),
    'classification': fields.String(description='Classification'),
    'rank': fields.Integer(description='Relevance rank'),
    'description': fields.String(description='Description'),
})

@ns.route('/')
class ImmunizationChecklist(Resource):
    @ns.response(404, 'Patient not found.')
    @ns.response(201, 'Successfully retrieved ImmunizationChecklist.')
    @ns.expect(parser)
    @ns.marshal_with(immunization)
    def get(self):
        """
        Returns immunization checklist for given patient

        Test the endpoint with this sample patient_id:
        a33d3135-2c7a-43ad-8804-3c2d3f492253
        """
        # print("Test *******************")
        # try:
        #
        #     # print(args['patient_id'])
        # except:
        #     print("Unexpected error: ", sys.exc_info()[0])
        #     print(traceback.format_exc())
        #     raise
        args = parser.parse_args()
        result = model.get_immunization_checklist(patient_id=args['patient_id'])
        if result is None:
            # return None, 404
            ns.abort(404, 'Patient not found.')
        else:
            return result, 201
