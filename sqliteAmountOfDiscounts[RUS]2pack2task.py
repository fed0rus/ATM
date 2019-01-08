import sqlite3
database = sqlite3.connect('database.db')
gnome = database.cursor()
clerk = database.cursor()
customer = input()
cashLowerBound = int(input())
amountOfPurchasesLowerBound = int(input())
# Fetching Customer ID
queryCustomer = (customer,)
for atom in gnome.execute('''SELECT id FROM customers WHERE name=?''', queryCustomer):
    customerId = atom[0]
# Fetching customer's balance
queryBalance = (customerId,)
for atom in gnome.execute('''SELECT balance FROM balances WHERE id=?''', queryBalance):
    customerBalance = atom[0]
# No way for cashless
if customerBalance < cashLowerBound:
    print(0)
else:
    # Fetching (customer -> shop) amount of transactions
    numberOfSales = 0
    for shop in gnome.execute('''SELECT id FROM shops'''):
        shopId = shop[0]
        for atom in clerk.execute('''SELECT COUNT(*) FROM transactions WHERE "from"=? AND "to"=?''', (customerId, shopId)):
            amountOfPurchases= atom[0]
        if amountOfPurchases >= amountOfPurchasesLowerBound:
            numberOfSales += 1
    print(numberOfSales)