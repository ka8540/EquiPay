from flask import Flask
from flask_restful import Api
from flask_cors import CORS

try:
    # Import only necessary functions and classes
    from src.utilities.swen_344_db_utils import exec_sql_file
    from src.api.login_api import LoginAPI
    from src.api.signup_api import SignUpApi
    from src.api.user_detail_api import UserDetail
    from src.api.logout_api import LogoutAPI
    from src.api.categories_api import ProductCategories, CategoryById, CategorySearch
    from src.api.products_api import Products, ProductById, ProductSearch
    from src.api.retailer_api import Retailers, RetailerById
    from src.api.prices_api import Prices, PricesByProduct
    from src.api.cart_api import CartAPI, CartAPIById
    from src.api.user_favorites_api import UserFavorites, UserFavoritesById
    from src.api.price_conversion_api import Canadian,Indian

    from src.model.amazon import insert_data_from_excel  # Assuming this is the correct function name for handling data insertions from the model
    from src.model.bestbut import insert_data_from_excel_bestbuy
except ImportError:
    # For relative imports within a package structure
    from utilities.swen_344_db_utils import exec_sql_file
    from api.login_api import LoginAPI
    from api.signup_api import SignUpApi
    from api.user_detail_api import UserDetail
    from api.logout_api import LogoutAPI
    from api.categories_api import ProductCategories, CategoryById, CategorySearch
    from api.products_api import Products, ProductById, ProductSearch
    from api.retailer_api import Retailers, RetailerById
    from api.prices_api import Prices, PricesByProduct
    from api.user_favorites_api import UserFavorites, UserFavoritesById
    from api.cart_api import CartAPI, CartAPIById
    from api.price_conversion_api import Canadian,Indian
    from model.amazon import insert_data_from_excel
    from model.bestbut import insert_data_from_excel_bestbuy
    
app = Flask(__name__)  # create Flask instance
CORS(app)  # Enable CORS on Flask server to work with Nodejs pages
api = Api(app)  # api router

api.add_resource(SignUpApi, '/signUp')
api.add_resource(LoginAPI, '/login')
api.add_resource(UserDetail, '/userdetail')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(ProductCategories, '/categories')
api.add_resource(CategoryById, '/categories/<int:category_id>')
api.add_resource(CategorySearch, '/categories/search')
api.add_resource(Products, '/products')
api.add_resource(ProductById, '/products/<int:product_id>')
api.add_resource(ProductSearch, '/products/search')
api.add_resource(Retailers, '/retailers')
api.add_resource(RetailerById, '/retailers/<int:retailer_id>')
api.add_resource(PricesByProduct, '/prices/products/<int:product_id>')
api.add_resource(Prices, '/prices')
api.add_resource(UserFavorites, '/user_favorites')
api.add_resource(UserFavoritesById, '/user_favorites/<int:product_id>')
api.add_resource(CartAPI, '/cart')
api.add_resource(CartAPIById, '/cart/<int:product_id>')
api.add_resource(Canadian, '/cad_price')
api.add_resource(Indian, '/inr_price')



def setup_database():
    print("Loading db")
    # exec_sql_file('data/UserDetail.sql')
    exec_sql_file('data/data.sql')
    insert_data_from_excel()
    insert_data_from_excel_bestbuy()


if __name__ == '__main__':
    print("Starting flask")
    setup_database()  # Set up the database and insert data from Excel
    app.run(debug=True)  # starts Flask
