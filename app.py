#Flask Backend
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Initialize portfolio (for demonstration purposes, it's a CSV)
def load_portfolio():
    try:
        return pd.read_csv('portfolio.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=["Asset", "Purchase Price", "Quantity", "Current Price", "Last Updated"])

# Save portfolio to CSV
def save_portfolio(portfolio):
    portfolio.to_csv('portfolio.csv', index=False)

# Home route to display portfolio
@app.route('/')
def home():
    portfolio = load_portfolio()
    return render_template('index.html', portfolio=portfolio)

# Route to add new asset
@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        # Retrieve form data
        asset_name = request.form['asset_name']
        purchase_price = float(request.form['purchase_price'])
        quantity = float(request.form['quantity'])
        current_price = float(request.form['current_price'])
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a new asset entry
        portfolio = load_portfolio()
        new_asset = pd.DataFrame([{
            "Asset": asset_name,
            "Purchase Price": purchase_price,
            "Quantity": quantity,
            "Current Price": current_price,
            "Last Updated": last_updated
        }])

        # Add new asset to portfolio and save
        portfolio = pd.concat([portfolio, new_asset], ignore_index=True)
        save_portfolio(portfolio)

        return redirect(url_for('home'))

    return render_template('add_asset.html')

# Calculate and display portfolio metrics
@app.route('/metrics')
def metrics():
    portfolio = load_portfolio()
    if portfolio.empty:
        return "Portfolio is empty. Please add assets first."

    portfolio["Current Value"] = portfolio["Quantity"] * portfolio["Current Price"]
    portfolio["Performance (%)"] = ((portfolio["Current Price"] - portfolio["Purchase Price"]) / portfolio["Purchase Price"]) * 100

    total_value = portfolio["Current Value"].sum()
    overall_change = (portfolio["Current Value"].sum() - (portfolio["Purchase Price"] * portfolio["Quantity"]).sum()) / (portfolio["Purchase Price"] * portfolio["Quantity"]).sum() * 100

    return render_template('metrics.html', portfolio=portfolio, total_value=total_value, overall_change=overall_change)

if __name__ == '__main__':
    app.run(debug=True)
