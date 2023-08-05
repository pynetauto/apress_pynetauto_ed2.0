# ex3_24.py
import csv
total = 0.0
with open ('C://Python312//ch03//2020_router_purchase.csv') as f:
    rows = csv.reader (f)
    headers = next (rows)
    for row in rows:
        row [4] = row [4].strip ('$')
        row [4] = float(row [4])
        row [3] = int(row [3])
        total += row[3] * row[4]

print('Total cost: $', total)