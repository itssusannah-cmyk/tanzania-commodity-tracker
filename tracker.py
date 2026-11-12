import csv

print("--- Tanzanian Local Market Commodity Tracker (Pure Python) ---")

# 1. Load data using Python's built-in csv module
data = []
with open('commodities.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Clean text and convert price to an integer
        row['Region'] = row['Region'].strip()
        row['Commodity'] = row['Commodity'].strip()
        row['Price_TZS'] = int(row['Price_TZS'])
        data.append(row)

print("\nRaw Data Preview (First 5 rows):")
for row in data[:5]:
    print(row)

# 2. Data Analysis: Calculate average price per commodity across regions
commodity_totals = {}
commodity_counts = {}

for row in data:
    comm = row['Commodity']
    price = row['Price_TZS']
    
    commodity_totals[comm] = commodity_totals.get(comm, 0) + price
    commodity_counts[comm] = commodity_counts.get(comm, 0) + 1

print("\n--- Average Prices Across Regions (TZS) ---")
for comm, total in commodity_totals.items():
    avg_price = total / commodity_counts[comm]
    print(f"{comm}: {avg_price:,.2f} TZS")

print("\nSuccess! Your script processed the data locally without any external dependencies.")