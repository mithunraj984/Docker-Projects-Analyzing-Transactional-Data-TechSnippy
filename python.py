import pandas as pd
import numpy as np
from pymongo import MongoClient
from forex_python.converter import CurrencyRates

# Function to download transactional data from Amazon S3 Bucket (Assuming you have your own implementation)
def download_data_from_s3():
    # Replace this function with your own implementation to download data from S3
    # Example: Use boto3 or another library for Amazon S3 interactions
    # Return a pandas DataFrame with the transactional data
    pass

# Function to convert currencies into SGD
def convert_currencies_to_sgd(data_frame):
    # Assuming data_frame has a 'Currency' column representing the currency of each transaction
    # Use forex-python to convert currencies to SGD
    c = CurrencyRates()
    sgd_exchange_rate = c.get_rate('SGD', 'USD')  # Replace 'USD' with your preferred base currency
    data_frame['Amount_SGD'] = data_frame['Amount'] * sgd_exchange_rate
    return data_frame

# Function to analyze data
def analyze_data(data_frame):
    # Example analysis: Calculate total transaction amount and count per currency
    result = data_frame.groupby('Currency').agg({'Amount': 'sum', 'Transaction_ID': 'count'}).reset_index()
    return result

# Function to store analyzed data into MongoDB
def store_data_in_mongodb(data_frame):
    # Replace 'your_mongodb_connection_string' with your actual MongoDB connection string
    client = MongoClient('your_mongodb_connection_string')
    db = client['your_database_name']
    collection = db['your_collection_name']
    
    # Convert the DataFrame to dictionary and insert into MongoDB
    data_dict = data_frame.to_dict(orient='records')
    collection.insert_many(data_dict)

# Main function
def main():
    # Download data from S3
    transaction_data = download_data_from_s3()

    # Convert currencies to SGD
    transaction_data_sgd = convert_currencies_to_sgd(transaction_data)

    # Analyze data
    analysis_result = analyze_data(transaction_data_sgd)

    # Store analyzed data in MongoDB
    store_data_in_mongodb(analysis_result)

if __name__ == "__main__":
    main()
