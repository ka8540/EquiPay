from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta
import json
from db.forecast import fetch_user_expenses
from db.amoutowed import get_user_id

class ForecastAPI(Resource):
    @jwt_required()
    def get(self):
        jwt_user = get_jwt_identity()
        user_id = get_user_id(jwt_user['username'])
        
        if not user_id:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        expenses = fetch_user_expenses(user_id)
        if not expenses:
            return make_response(jsonify({"message": "No expenses found for the user"}), 201)
        print("Expenses:",expenses)
        df = pd.DataFrame(expenses, columns=['Amount', 'Date'])
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True)
        
        
        df['Timestamp'] = (df['Date'] - df['Date'].min()).dt.total_seconds() / 86400  
        X = df[['Timestamp']]
        y = df['Amount'].astype(float)
        
       
        model = LinearRegression()
        model.fit(X, y)
        
        
        max_date = df['Date'].max()
        future_dates = [max_date + timedelta(days=30 * i) for i in range(1, 7)]
        future_timestamps = [(date - df['Date'].min()).total_seconds() / 86400 for date in future_dates]
        predicted_amounts = model.predict(np.array(future_timestamps).reshape(-1, 1))
        
        
        forecast = {date.strftime("%Y-%m-%d"): float(amount) for date, amount in zip(future_dates, predicted_amounts)}
        return jsonify({"forecast": forecast})


