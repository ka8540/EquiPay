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
    from api.profile_pic_api import UploadAPI, FriendProfilePictureAPI
    from api.additional_settings_api import DeleteAccountApi
    from api.addfriend_api import AddFriendApi
    from api.addfriend_api import FiendList
    from api.split_expense_api import SplitExpenseTwoApi
    from api.total_amount_api import TotalAmountAPIbyID , TotalAmountAPI
    from api.settle_api import DebtsByFriendAPI, DeleteDebtAPI
    from api.create_group_api import UserGroupsAPI, CreateGroupAPI
    from api.profile_pic_api import GroupProfilePictureUpload
    from api.group_api import GroupMembersAPI
    from api.group_api import GroupNameByIdAPI
    from api.profile_pic_api import GroupProfilePictureUpload
    from api.group_expense_api import GroupExpenseAPI
    from api.group_total_expense_api import TotalGroupAmountAPI
    from api.group_total_expense_api import TotalGroupAmountAPIbyID
    from api.group_settle_api import DeleteGroupDebtByIdAPI
    from api.textract_upload_api import UploadAndAnalyzeAPI
    from api.group_expense_list_api import GroupExpensesListAPI
    from api.total_amount_pending import NetAmountOwedAPI
    from api.graph_api import GraphAPI
    from api.activity_api import ActivityAPI
except ImportError:
    from utilities.swen_344_db_utils import exec_sql_file
    from api.login_api import LoginAPI
    from api.signup_api import SignUpApi
    from api.logout_api import LogoutAPI
    from api.userlist_api import ListUsersApi
    from api.account_api import AccountApi
    from api.password_api import PasswordApi
    from api.profile_pic_api import UploadAPI, FriendProfilePictureAPI
    from api.additional_settings_api import DeleteAccountApi
    from api.addfriend_api import AddFriendApi
    from api.addfriend_api import FiendList
    from api.split_expense_api import SplitExpenseTwoApi
    from api.total_amount_api import TotalAmountAPIbyID, TotalAmountAPI
    from api.settle_api import DebtsByFriendAPI, DeleteDebtAPI
    from api.create_group_api import UserGroupsAPI, CreateGroupAPI
    from api.profile_pic_api import GroupProfilePictureUpload
    from api.group_api import GroupMembersAPI
    from api.group_api import GroupNameByIdAPI
    from api.profile_pic_api import GroupProfilePictureUpload
    from api.group_expense_api import GroupExpenseAPI
    from api.group_total_expense_api import TotalGroupAmountAPI
    from api.group_total_expense_api import TotalGroupAmountAPIbyID
    from api.group_settle_api import DeleteGroupDebtByIdAPI
    from api.textract_upload_api import UploadAndAnalyzeAPI
    from api.group_expense_list_api import GroupExpensesListAPI
    from api.total_amount_pending import NetAmountOwedAPI
    from api.graph_api import GraphAPI
    from api.activity_api import ActivityAPI

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
api.add_resource(AddFriendApi, '/addFriend')
api.add_resource(FiendList,'/friends')
api.add_resource(SplitExpenseTwoApi, '/split-expense')
api.add_resource(TotalAmountAPIbyID, '/total-amount/<int:friend_id>')
api.add_resource(TotalAmountAPI, '/total-amount')
api.add_resource(FriendProfilePictureAPI, '/friend-profile-picture/<int:friend_id>')
api.add_resource(DebtsByFriendAPI, '/debts-by-friend/<int:friend_id>')
api.add_resource(DeleteDebtAPI, '/delete-debt')
api.add_resource(UserGroupsAPI,'/user_group')
api.add_resource(CreateGroupAPI, '/create_group')
api.add_resource(GroupProfilePictureUpload, '/group_photo')
api.add_resource(GroupMembersAPI, '/group_members/<int:group_id>')
api.add_resource(GroupNameByIdAPI, '/group_name/<int:group_id>')
api.add_resource(GroupProfilePictureUpload, '/group_photo/<int:group_id>', endpoint='group_photo_upload')
api.add_resource(GroupExpenseAPI, '/group_expense/<int:group_id>')
api.add_resource(TotalGroupAmountAPI, '/group_total/<int:group_id>')
api.add_resource(TotalGroupAmountAPIbyID, '/group_total/<int:group_id>/<int:friend_id>')
api.add_resource(DeleteGroupDebtByIdAPI,'/group_settle/<int:group_id>')
api.add_resource(UploadAndAnalyzeAPI, '/upload-and-analyze')
api.add_resource(GroupExpensesListAPI, '/group_expenselist/<int:group_id>')
api.add_resource(NetAmountOwedAPI, '/net_amount')
api.add_resource(GraphAPI, '/graph_values')
api.add_resource(ActivityAPI, '/activity')

def setup_database():
    print("Loading db")
    exec_sql_file('data/data.sql')

if __name__ == '__main__':
    print("Starting flask")

    setup_database()
    app.run(debug=True)
