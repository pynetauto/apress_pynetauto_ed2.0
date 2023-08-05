# ex3_23.py
total = 0.0
with open ('C://Python312//ch03//2020_router_purchase.csv', 'r') as f:
    headers = next (f)
    for line in f:
        line = line.strip ()
        devices = line.split (',')
        devices[4] = devices[4] .strip ('$')
        devices[4] = float (devices[4])
        devices[3] = int (devices[3])
        total += devices[3] * devices[4]

print('Total cost: $', total)