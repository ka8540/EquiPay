from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import boto3
from botocore.exceptions import NoCredentialsError
import werkzeug
from utilities.swen_344_db_utils import exec_commit
from model.user import get_username  
from db.user_details import update_user_image_url

class UploadAPI(Resource):
    def __init__(self, **kwargs):
        self.s3 = boto3.client('s3')
        self.s3_bucket = kwargs['s3_bucket']

    @jwt_required()  # Require JWT token for this endpoint
    def post(self):
        print("Headers:", request.headers)  # Log headers to check what's received
        print("Files:", request.files)  # Log files directly to check the presence
        # JWT identity and session key from headers
        jwt_user = get_jwt_identity()
        session_key = request.headers.get('Session-Key')
        print("session-key inside the post request:",session_key)
        if not session_key:
            return make_response(jsonify({"error": "Session key is required"}), 400)

        # Validate session key and get username
        username = get_username(session_key)
        if not username:
            return make_response(jsonify({"error": "Invalid session key or token mismatch"}), 401)

        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True, help="File is required")
        args = parser.parse_args()
        file = args['file']
        print(file)

        if file:
            file_name = file.filename
            content_type = file.content_type
            try:
                # Upload the file without specifying ACL
                self.s3.upload_fileobj(
                    file,
                    self.s3_bucket,
                    file_name,
                    ExtraArgs={'ContentType': content_type}
                )
                image_url = f"https://{self.s3_bucket}.s3.amazonaws.com/{file_name}"

                # Assuming you have a function to update the user's image URL in the database
                response = update_user_image_url(username, image_url)
                return make_response(jsonify({"url": image_url, "db": response}), 200)
            except NoCredentialsError as e:
                return make_response(jsonify({"error": "Credentials not available"}), 403)
            except Exception as e:
                return make_response(jsonify({"error": str(e)}), 500)
        else:
            return make_response(jsonify({"error": "No file part"}), 400)