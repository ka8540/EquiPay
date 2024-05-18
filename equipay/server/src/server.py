from flask import Flask
from flask_restful import Api
from flask_cors import CORS

try:
    # Import only necessary functions and classes
    from src.utilities.swen_344_db_utils import exec_sql_file
    from src.api.login_api import LoginAPI
    from src.api.signup_api import SignUpApi
    from src.api.logout_api import LogoutAPI
except ImportError:
    # For relative imports within a package structure
    from utilities.swen_344_db_utils import exec_sql_file
    from api.login_api import LoginAPI
    from api.signup_api import SignUpApi
    from api.logout_api import LogoutAPI
    
app = Flask(__name__)  # create Flask instance
CORS(app)  # Enable CORS on Flask server to work with Nodejs pages
api = Api(app)  # api router

api.add_resource(SignUpApi, '/signUp')
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')



def setup_database():
    print("Loading db")
    exec_sql_file('data/data.sql')


if __name__ == '__main__':
    print("Starting flask")
    setup_database()  # Set up the database and insert data from Excel
    app.run(debug=True)  # starts Flask
