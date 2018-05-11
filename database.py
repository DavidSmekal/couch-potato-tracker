import sqlite3
import json
import requests
import math

conn = sqlite3.connect('database.db')

print("connected to database")

conn.execute('CREATE TABLE IF NOT EXISTS usersStock (stockTicker VARCHAR(10), desired DOUBLE, '
             'currentShare INT, sharePrice DOUBLE, currentMoney INT,'
             'currentPercentage DOUBLE, variation DOUBLE, buySharesRoundDown INT, costToPurchase INT) ;')


def insert_into_database(stock, desired, shares):
    conn.execute("INSERT INTO usersStock (stockTicker, desired, currentShare) VALUES (? , ?, ?);",
                 (stock, desired, shares,))
    conn.commit()
    update_values(0)
    print("inserted successfully")


# this function will update all the values when called
# parameter is the amount of money that is getting added.
# When I call update_values() everywhere else in the program
# where I just want to update the values, I will pass in 0.
def update_values(money):
    # need to get stockTicker, desired and currentShare from the database
    conn = sqlite3.connect('database.db')
    query = "SELECT stockTicker, desired, currentShare FROM usersStock;"
    result = conn.execute(query)
    new_result = result.fetchall()

    for a, b, c in new_result:
        stockTicker = a
        desired = b
        currentShare = c
        # finds the total money in user's profile
        total = current_money_function()

        # todo: I am not able to update the values when adding money of 0
        # if money > 0:
        #     pass
        # if total == 0:

        # if the user is adding money, it will add it to the total
        total += money
        # gets the price of the share
        response = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + stockTicker)
        result = json.loads(response.content.decode('utf-8'))
        sharePrice = result['quoteResponse']['result'][0]['regularMarketPrice']
        print(sharePrice)

        # finds how much money you currently have of the share
        currentMoney = sharePrice * currentShare

        # need to set these values to 0 since the calculations can't be divided by 0
        if total == 0:
            currentPercentage = 0
            variation = 0
            buySharesRoundDown = 0

        else:
            # finds how much percentage your portfolio is at
            currentPercentage = currentMoney / total

            # calculates the variation
            variation = currentPercentage / desired

            # calculates how many shares the user should buy
            # this will be rounded down
            buySharesRoundDown = math.floor(((total * desired) - currentMoney) / sharePrice)

        # how much it will cost to purchase the amount of shares
        costToPurchase = buySharesRoundDown * sharePrice
        conn.execute("UPDATE usersStock SET desired = ?, currentShare = ?, sharePrice = ?, "
                     "currentMoney = ?, currentPercentage = ?, variation = ?,buySharesRoundDown = ?,  "
                     "costToPurchase = ? WHERE stockTicker = ?; ",
                     (desired, currentShare, sharePrice, currentMoney, currentPercentage,
                      variation, buySharesRoundDown, costToPurchase, stockTicker,))
        conn.commit()
    print("Database has been updated")


# this function will only update the desired value.
def update_desired_value(stock, desired, amount):
    conn.execute("UPDATE usersStock SET desired = ?, currentShare = ? WHERE stockTicker = ?", (desired, amount, stock))
    conn.commit()


# this function will return the total money in user's portfolio
def current_money_function():
    sum = conn.execute("SELECT SUM(currentMoney) FROM usersStock")
    conn.commit()
    newsum = sum.fetchone()
    if newsum[0] is None:
        return 0
    else:
        return newsum[0]


# this method will take in a decimal and return a string in percentage form
def decimal_to_percentage(decimal):
    decimal = math.ceil(decimal * 100)
    newString = str(decimal) + "%"
    return newString


# will delete a stock from the database
def delete_stock(stock):
    stock = stock
    conn.execute("DELETE FROM usersStock WHERE stockTicker = ?", (stock,))
    conn.commit()
    update_values(0)
    print("Deleted")


# this function is a backup. This will be used to update the specific values.
# I will have to use this later on!
'''
# this function will update all the values, and do all the math
def update_values(stockTicker, desired, currentShare):
    # finds the total money in user's profile
    total = current_money_function()
    # gets the price of the share
    response = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + stockTicker)
    result = json.loads(response.content.decode('utf-8'))
    sharePrice = result['quoteResponse']['result'][0]['regularMarketPrice']

    # finds how much money you currently have of the share
    currentMoney = sharePrice * currentShare

    # finds how much percentage your portfolio is at
    currentPercentage = currentMoney / total

    # calculates the variation
    variation = currentPercentage / desired

    # calculates how many shares the user should buy
    # this will be rounded down
    buySharesRoundDown = math.floor(((total * desired) - currentMoney)/sharePrice)

    # how much it will cost to purchase the amount of shares
    costToPurchase = buySharesRoundDown * sharePrice
    conn.execute("UPDATE usersStock SET desired = ?, currentShare = ?, sharePrice = ?, "
                 "currentMoney = ?, currentPercentage = ?, variation = ?,buySharesRoundDown = ?,  "
                 "costToPurchase = ? WHERE stockTicker = ?; ",
            (desired, currentShare, sharePrice, currentMoney, currentPercentage,
             variation, buySharesRoundDown, costToPurchase, stockTicker,))
    conn.commit()
'''
