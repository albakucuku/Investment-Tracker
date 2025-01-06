import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize the portfolio as an empty pandas DataFrame with specific column types
# https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/
def initializePortfolio():

    return pd.DataFrame({
        "Asset": pd.Series(dtype="str"),     # https://www.geeksforgeeks.org/python-pandas-series/        
        "Purchase Price": pd.Series(dtype="float"),  
        "Quantity": pd.Series(dtype="float"),        
        "Current Price": pd.Series(dtype="float"),   
        "Last Updated": pd.Series(dtype="str")      # time stamp to keep track 
    })

# Function to add a new asset to the portfolio
def addAsset(portfolio):
 
    assetName = input("Enter the asset name: ")
    purchasePrice = float(input(f"Enter the purchase price of {assetName}: "))
    quantity = float(input(f"Enter the quantity of {assetName} owned: "))
    currentPrice = float(input(f"Enter the current price of {assetName}: "))
    # Generate a timestamp for when the asset is added
    lastUpdated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # source used here is stack overflow 
    
    # Create a DataFrame for the new asset
    newAsset = pd.DataFrame([{
        "Asset": assetName,
        "Purchase Price": purchasePrice,
        "Quantity": quantity,
        "Current Price": currentPrice,
        "Last Updated": lastUpdated
    }])
    
    # Combine the new asset with the existing portfolio
    # concat() -> https://www.geeksforgeeks.org/pandas-concat-function-in-python/
    portfolio = pd.concat([portfolio, newAsset], ignore_index=True)
    print(f"Asset {assetName} added successfully!")
    return portfolio

# Function to display the current portfolio
def viewPortfolio(portfolio):
    if portfolio.empty:
        print("Your portfolio is empty.")
    else:
        print("\nCurrent Portfolio:")
        print(portfolio.to_string()) # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_string.html
        # ^^ i had an issue with this function truncating my columns so i used to_string() to solve this problem
        
# Function to update the price of an existing asset
def updatePrice(portfolio):

    assetName = input("Enter the asset name to update: ")
    if assetName in portfolio["Asset"].values:
        new_price = float(input(f"Enter the new price for {assetName}: "))
        # Update the price and timestamp for the specified asset
        # .loc method -> https://www.geeksforgeeks.org/python-pandas-dataframe-loc/
        portfolio.loc[portfolio["Asset"] == assetName, "Current Price"] = new_price
        portfolio.loc[portfolio["Asset"] == assetName, "Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Price for {assetName} updated to {new_price}!")
    else:
        print(f"Asset {assetName} not found in your portfolio.")
    return portfolio

# Function to calculate and display portfolio metrics
def calculateMetrics(portfolio):
    """
    I wanted to calculate and display important portfolio metrics.
    - Current value of each asset (quantity * current price)
    - Performance percentage for each asset
    - Total portfolio value
    - Overall percentage change in portfolio value
    """
    if portfolio.empty:
        print("Your portfolio is empty. Add assets to calculate metrics.")
        return
    
    # Calculate additional columns for performance metrics
    # https://www.codingfinance.com/post/2018-04-03-calc-returns-py/
    portfolio["Current Value"] = portfolio["Quantity"] * portfolio["Current Price"] 
    portfolio["Performance (%)"] = ((portfolio["Current Price"] - portfolio["Purchase Price"]) / portfolio["Purchase Price"]) * 100
    
    print("\nAsset Performance:")
    print(portfolio[["Asset", "Current Value", "Performance (%)"]])
    
    # Aggregate portfolio metrics
    total_value = portfolio["Current Value"].sum()
    overall_change = (portfolio["Current Value"].sum() - (portfolio["Purchase Price"] * portfolio["Quantity"]).sum()) / (portfolio["Purchase Price"] * portfolio["Quantity"]).sum() * 100 # https://absentdata.com/pandas/3-ways-to-calculate-percent-change-in-python/
    
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")
    print(f"Overall Portfolio Percentage Change: {overall_change:.2f}%")

# Function to visualize portfolio performance
def visualizePortfolio(portfolio):
    """
    uses a bar chart to visualize the performance of the portfolio.
    each bar represents the performance percentage of an asset.
    """
    if portfolio.empty:
        print("Your portfolio is empty. Add assets to visualize performance.")
        return
    
    # Ensure performance percentage is calculated before plotting
    portfolio["Performance (%)"] = ((portfolio["Current Price"] - portfolio["Purchase Price"]) / portfolio["Purchase Price"]) * 100
    portfolio.plot.bar(x="Asset", y="Performance (%)", legend=False, color="skyblue")
    plt.title("Portfolio Performance")
    plt.ylabel("Performance (%)")
    plt.xlabel("Asset")
    plt.show()

# Function to save the portfolio to a CSV file
def savePortfolio(portfolio):
    # Saves the portfolio to CSV file 'portfolio.csv'.
    portfolio.to_csv("portfolio.csv", index=False)
    print("Portfolio saved to portfolio.csv.")

# Function to load a portfolio from a CSV file
def loadPortfolio():
    """
    This will load portfolio data from a CSV file named 'portfolio.csv'.
    If the file isn't found it initializes an empty portfolio.
    """
    try:
        portfolio = pd.read_csv("portfolio.csv")
        print("Portfolio loaded from portfolio.csv.")
    except FileNotFoundError:
        print("No portfolio.csv file found. Starting with an empty portfolio.")
        portfolio = initializePortfolio()
    return portfolio

# main program
def main():

    print("Welcome to the Investment Portfolio Tracker!")
    portfolio = initializePortfolio()
    
    while True:
        # display menu options
        print("\nMenu:")
        print("1. Add a new asset")
        print("2. View portfolio")
        print("3. Update asset price")
        print("4. Calculate portfolio metrics")
        print("5. Visualize portfolio performance")
        print("6. Save portfolio")
        print("7. Load portfolio")
        print("8. Exit")
        
        # get user input for menu selection
        choice = input("Choose an option (1-8): ")
        
        if choice == "1":
            portfolio = addAsset(portfolio)
        elif choice == "2":
            viewPortfolio(portfolio)
        elif choice == "3":
            portfolio = updatePrice(portfolio)
        elif choice == "4":
            calculateMetrics(portfolio)
        elif choice == "5":
            visualizePortfolio(portfolio)
        elif choice == "6":
            savePortfolio(portfolio)
        elif choice == "7":
            portfolio = loadPortfolio()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a valid option (1-8).")

if __name__ == "__main__":
    main()