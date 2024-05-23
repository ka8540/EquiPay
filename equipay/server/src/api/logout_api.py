from flask import jsonify, make_response, request
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import only the necessary functions from utilities and logout db module
try:
    from src.utilities.swen_344_db_utils import exec_commit
    from src.db.logout import user_logout  # Assuming user_logout function handles the logout process
except ImportError:
    from utilities.swen_344_db_utils import exec_commit
    from db.logout import user_logout

class LogoutAPI(Resource):
    """
    API endpoint for user logout.
    """
    
    @jwt_required()
    def post(self):
        print("Raw Request Data:", request.data)
        parser = reqparse.RequestParser()
        parser.add_argument('session_key', type=str, required=True, location='json')
        args = parser.parse_args()
        print(args, 'session_key on api')

        # Get current user's identity from the JWT token
        current_user = get_jwt_identity()
        print(f'Current user: {current_user}')

        # Check user credentials
        response, status_code = user_logout(args)

        return make_response(jsonify(response), status_code)
