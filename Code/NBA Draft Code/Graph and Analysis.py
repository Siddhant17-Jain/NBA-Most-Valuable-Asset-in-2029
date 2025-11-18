import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy.optimize import curve_fit
from scipy.stats import linregress

# Load the aggregated data
final_df = pd.read_csv("Totals.csv")

# Dropping rows where WS/Yrs might be NaN or inf
final_df = final_df.dropna(subset=['WS/Yrs'])
final_df = final_df[np.isfinite(final_df['WS/Yrs'])]

# Prepare data for regression
X = final_df[['Pk']]  # Independent variable (draft pick)
y = final_df['WS/Yrs']  # Dependent variable (Win Shares per Year)

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X, y)
y_pred_linear = linear_model.predict(X)

# Linear regression statistics
slope, intercept, r_value, p_value, std_err = linregress(final_df['Pk'], final_df['WS/Yrs'])
linear_r2 = r_value**2
linear_equation = f"y = {slope:.4f}x + {intercept:.4f}"

# Polynomial Regression (2nd degree)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

poly_model = LinearRegression()
poly_model.fit(X_poly, y)
y_pred_poly = poly_model.predict(X_poly)

# Polynomial regression statistics
poly_r2 = poly_model.score(X_poly, y)
poly_coefficients = poly_model.coef_
poly_intercept = poly_model.intercept_
poly_equation = f"y = {poly_coefficients[0]:.4f} + {poly_coefficients[1]:.4f}x + {poly_coefficients[2]:.4f}x^2"

# Logarithmic Curve Fitting
def log_model(x, a, b):
    return a + b * np.log(x)

params, covariance = curve_fit(log_model, final_df['Pk'], final_df['WS/Yrs'])
a, b = params
y_pred_log = log_model(final_df['Pk'], *params)

# Logarithmic regression statistics
residuals = y - y_pred_log
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y - np.mean(y))**2)
log_r2 = 1 - (ss_res / ss_tot)
log_equation = f"y = {a:.4f} + {b:.4f} * log(x)"

# Save results to a CSV file
results = pd.DataFrame({
    'Model': ['Linear Regression', 'Polynomial Regression (2nd degree)', 'Logarithmic Curve Fitting'],
    'R-squared': [linear_r2, poly_r2, log_r2],
    'P-value': [p_value, 'N/A', 'N/A'],  # p-value is only for linear regression
    'Slope': [slope, 'N/A', 'N/A'],
    'Intercept': [intercept, poly_intercept, a],
    'Coefficients': ['N/A', poly_coefficients.tolist(), b],  # Convert list to string for saving
    'Function': [linear_equation, poly_equation, log_equation]
})

results.to_csv('results.csv', index=False)

# Plot the regression results
plt.figure(figsize=(14, 8))
plt.scatter(final_df['Pk'], final_df['WS/Yrs'], color='blue', label='Actual WS/Yrs')

# Linear regression line
plt.plot(final_df['Pk'], y_pred_linear, color='red', label='Linear Regression')

# Polynomial regression line
plt.plot(final_df['Pk'], y_pred_poly, color='orange', label='Polynomial Regression (2nd degree)')

# Logarithmic regression line
plt.plot(final_df['Pk'], y_pred_log, color='green', label='Logarithmic Curve Fitting')

plt.xlabel('Draft Pick')
plt.ylabel('Win Shares per Year (WS/Yrs)')
plt.title('Regression Analysis of WS/Yrs by Draft Pick')
plt.legend()
plt.grid(True)
plt.show()
