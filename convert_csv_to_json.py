import csv
import json
import re
import pandas as pd

# Load the CSV file
file_path = 'transactions.csv'
transactions_df = pd.read_csv(file_path)

# Function to handle valid numeric amounts and skip invalid ones
def clean_amount(amount):
    # Remove spaces, Rs., and commas first
    cleaned_amount = amount.replace("Rs.", "").replace(",", "").replace(" ", "")
    
    # Handle negative and positive amounts by ensuring signs are in correct position
    cleaned_amount = cleaned_amount.replace("+-", "-").replace("+", "")
    
    # Try to convert to float, if fails return None to filter out later
    try:
        return float(cleaned_amount)
    except ValueError:
        return None

# Normalize transaction names by removing prefixes like "Money sent to" or "Received from"
def normalize_name(transaction_details):
    return re.sub(r"(Money sent to|Received from) ", "", transaction_details)

# Apply the cleaning function to the Amount column and normalize the transaction names
transactions_df['Cleaned_Amount'] = transactions_df['Amount'].apply(clean_amount)
transactions_df['Normalized_Name'] = transactions_df['Transaction Details'].apply(normalize_name)

# Filter out invalid amounts
valid_transactions_df = transactions_df.dropna(subset=['Cleaned_Amount'])

# Group by the normalized names and aggregate transactions
grouped_data = valid_transactions_df.groupby('Normalized_Name').agg({
    'Date': list,
    'Cleaned_Amount': sum,
    'Amount': list
}).reset_index()

# Prepare the final output structure in the required JSON format
result = []
for _, row in grouped_data.iterrows():
    transactions = [{"Date": date, "Amount": amount} for date, amount in zip(row['Date'], row['Amount'])]
    cumulative_transaction = f"{'+' if row['Cleaned_Amount'] >= 0 else ''}{int(row['Cleaned_Amount'])}"
    
    result.append({
        "Name of Transaction Account": row['Normalized_Name'],
        "Cumulative Transaction": cumulative_transaction,
        "Transactions": transactions
    })

# Write the result to a JSON file
with open('transactions_output.json', 'w') as f:
    json.dump(result, f, indent=4)

print("JSON data has been written to 'transactions_output.json'")
