from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

try:
    from utilities.swen_344_db_utils import exec_sql_file
    from api.login_api import LoginAPI
    from api.signup_api import SignUpApi
    from api.logout_api import LogoutAPI
    from api.userlist_api import ListUsersApi
    from api.account_api import AccountApi
    from api.password_api import PasswordApi
    from api.profile_pic_api import UploadAPI
    from api.additional_settings_api import DeleteAccountApi
except ImportError:
    from utilities.swen_344_db_utils import exec_sql_file
    from api.login_api import LoginAPI
    from api.signup_api import SignUpApi
    from api.logout_api import LogoutAPI
    from api.userlist_api import ListUsersApi
    from api.account_api import AccountApi
    from api.password_api import PasswordApi
    from api.profile_pic_api import UploadAPI
    from api.additional_settings_api import DeleteAccountApi
    

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['S3_BUCKET_NAME'] = 'profile-picture-docs'
jwt = JWTManager(app)
api = Api(app)

api.add_resource(SignUpApi, '/signUp', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(LoginAPI, '/login', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(LogoutAPI, '/logout')
api.add_resource(ListUsersApi, '/listUsers', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(AccountApi, '/accountapi', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(PasswordApi, '/passwordapi', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(UploadAPI, '/upload', resource_class_kwargs={'s3_bucket': app.config['S3_BUCKET_NAME']})
api.add_resource(DeleteAccountApi, '/deleteaccount',resource_class_kwargs={'bcrypt': bcrypt})

def setup_database():
    print("Loading db")
    exec_sql_file('data/data.sql')

if __name__ == '__main__':
    print("Starting flask")
    setup_database()
    app.run(debug=True)
