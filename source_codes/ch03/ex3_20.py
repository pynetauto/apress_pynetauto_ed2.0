# ex3_20.py
import csv

with open ('C://Python312//ch03//2020_router_purchase.csv', 'w', newline='' ) as csvfile:
    filewriter = csv.writer (csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    filewriter.writerow (['Site', 'Router_Type', 'IOS_Image', 'No_of_routers', 'Unit_price($)', 'Purchase_Date'])
    filewriter.writerow(['NYNY', 'ISR4351/K9', 'isr4300-universalk9.16.09.05.SPA.bin', 4, '$ 9100.00', '1-Mar-20'])
    filewriter.writerow(['LACA', 'ISR4331/K9', 'isr4300-universalk9.16.09.05.SPA.bin', 2, '$ 5162.00', '1-Mar- 20'])
    filewriter.writerow(['LDUK', 'ISR4321/K9', 'isr4300-universalk9.16.09.05.SPA.bin', 1, '$ 2370.00', '3-Apr- 20'])
    filewriter.writerow(['HKCN', 'ISR4331/K9', 'isr4300-universalk9.16.09.05.SPA.bin', 2, '$ 5162.00', '17-Apr-20'])
    filewriter.writerow(['TKJP', 'ISR4351/K9', 'isr4300-universalk9.16.09.05.SPA.bin', 1, '$ 9100.00', '15-May-20'])
    filewriter.writerow(['MHGM', 'ISR4331/K9', 'isr4300-universalk9.16.09.05.SPA.bin', 2, '$ 5162.00', '30-Jun-20'])