import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# Load the training data
training_data = pd.read_csv('/Users/siddhantjain/PycharmProjects/Most Valuable NBA Player/Combined Tests/75_Experience.csv')

# Prepare data for polynomial regression
X_train = training_data[['Experience']]
y_train = training_data['Total_Win_Shares'] / training_data['Total_Players']

# Polynomial Regression on the overall data
poly = PolynomialFeatures(degree=2)
X_poly_train = poly.fit_transform(X_train)
poly_reg = LinearRegression()
poly_reg.fit(X_poly_train, y_train)

# Load player data
player_data = pd.read_csv('/Users/siddhantjain/PycharmProjects/Most Valuable NBA Player/Combined Tests/Advanced_Stats.csv')

# Function to predict player's win shares 5 years down the line
def predict_future_win_shares(player_experience, current_win_shares):
    # Predict the peak based on the polynomial regression model
    peak_prediction = poly_reg.predict(poly.transform([[player_experience]]))[0]

    # Predict the win shares 5 years down the line
    future_experience = player_experience + 5
    future_poly = poly.transform(pd.DataFrame([[future_experience]], columns=['Experience']))
    future_prediction = poly_reg.predict(future_poly)[0]

    # Adjust the prediction based on the player's current win shares
    # Adjustment factor: scale prediction to player's current win shares
    adjusted_future_prediction = (current_win_shares / peak_prediction) * future_prediction

    return adjusted_future_prediction

# Apply the prediction function to all players
player_data['Predicted_WS_5_Years'] = player_data.apply(
    lambda row: predict_future_win_shares(row['Experience'], row['WS']),
    axis=1
)

# Save updated player data with predictions
player_data.to_csv('Advanced_Stats.csv', index=False)
print("Predictions saved to Advanced_Stats.csv")
