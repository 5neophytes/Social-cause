import re
import pandas as pd
from ingest_pdf import extract_pdf

extracted_text = extract_pdf(filepath="C:/Users/satvi/Social-cause/dummy.pdf")

dates = []
transaction_details = []
amounts = []
times = []

date_pattern = r'\d{1,2} (Sep|Aug)'  # Matches dates like '24 Sep' or '1 Aug'

lines = extracted_text.split('\n')



for i, line in enumerate(lines):
    print(i, line)
    if re.search(date_pattern, line):
        dates.append(line.strip())  # Add the date
        times.append(lines[i + 1].strip())
        transaction_details.append(lines[i + 2].strip())
        amounts.append(lines[i + 4].strip())

print(len(dates))
print(len(transaction_details))
print(len(amounts))

df_transactions = pd.DataFrame({
    'Date': dates,
    'Time': times,
    'Transaction Details': transaction_details,
    'Amount': amounts
})


print(df_transactions.head())

df_transactions.to_csv('transactions.csv', index=False)