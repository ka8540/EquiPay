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
except ImportError:
    from utilities.swen_344_db_utils import exec_sql_file
    from api.login_api import LoginAPI
    from api.signup_api import SignUpApi
    from api.logout_api import LogoutAPI

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)
api = Api(app)

api.add_resource(SignUpApi, '/signUp', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(LoginAPI, '/login', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(LogoutAPI, '/logout')

def setup_database():
    print("Loading db")
    exec_sql_file('data/data.sql')

if __name__ == '__main__':
    print("Starting flask")
    setup_database()
    app.run(debug=True)
