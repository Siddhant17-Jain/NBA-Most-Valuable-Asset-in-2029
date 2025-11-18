import pandas as pd
import numpy as np

# Load player data
test_data = pd.read_csv('Advanced_Stats.csv')

# Define the polynomial equations based on the given coefficients
def ws_equation1(x):
    return (12.6 +
            -0.36 * x +
            9.38E-03 * x**2 +
            -1.44E-04 * x**3 +
            1.3E-06 * x**4 +
            -7.31E-09 * x**5 +
            2.61E-11 * x**6 +
            -5.95E-14 * x**7 +
            8.36E-17 * x**8 +
            -6.61E-20 * x**9 +
            2.24E-23 * x**10)

def ws_equation2(x):
    return (14.1 +
            -0.469 * x +
            0.0118 * x**2 +
            -1.7E-04 * x**3 +
            1.44E-06 * x**4 +
            -7.63E-09 * x**5 +
            2.58E-11 * x**6 +
            -5.57E-14 * x**7 +
            7.44E-17 * x**8 +
            -5.58E-20 * x**9 +
            1.8E-23 * x**10)

def ws_equation3(x):
    return (33.6 +
            -1.28 * x +
            0.026 * x**2 +
            -2.95E-04 * x**3 +
            2.03E-06 * x**4 +
            -8.89E-09 * x**5 +
            2.54E-11 * x**6 +
            -4.69E-14 * x**7 +
            5.42E-17 * x**8 +
            -3.56E-20 * x**9 +
            1.01E-23 * x**10)

# Extract relevant features
age = test_data['Age']
experience = test_data['Experience']
current_ws = test_data['WS']

# Calculate predictions using the three equations
predicted_ws_eq1 = ws_equation1(age)
predicted_ws_eq2 = ws_equation2(experience)
predicted_ws_eq3 = ws_equation3(age + experience)

# Average the predictions from the three equations
average_predicted_ws = (predicted_ws_eq1 + predicted_ws_eq2 + predicted_ws_eq3) / 3

# Adjust predictions based on current WS and age
adjustment_factor = 0.5
predicted_ws_per_season = (average_predicted_ws * (1 - adjustment_factor) +
                           current_ws * adjustment_factor)

# Ensure predictions are realistic (optional: apply a cap or limit to predictions)
predicted_ws_per_season = np.clip(predicted_ws_per_season, a_min=0, a_max=None)  # Avoid negative predictions

# Store predictions in the dataframe
test_data['Predicted_WS_per_Season_in_5_Years'] = predicted_ws_per_season

# Save the results back into Advanced_Stats.csv
test_data.to_csv('Advanced_Stats.csv', index=False)

print("Predictions for WS per season 5 years into the future saved to Advanced_Stats.csv")
