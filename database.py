import sqlite3
import json
import requests
import math
import errorPopup

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
        stock_ticker = a
        desired = b
        current_share = c
        # finds the total money in user's profile
        total = current_money_function()

        # todo: I am not able to update the values when adding money of 0
        # if money > 0:
        #     pass
        # if total == 0:

        # if the user is adding money, it will add it to the total
        total += money

        response = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + stock_ticker)
        print(response)
        # if stock doesn't exist in website, show popup
        if response.status_code == 404:
            errorPopup.show_error_pop_up(1)
            print("error")
            # need to delete the stock ticker from the database now
            delete_stock(stock_ticker)
            return 0

        result = json.loads(response.content.decode('utf-8'))
        share_price = result['quoteResponse']['result'][0]['regularMarketPrice']

        # finds how much money you currently have of the share
        current_money = share_price * current_share

        # need to set these values to 0 since the calculations can't be divided by 0
        if total == 0:
            current_percentage = 0
            variation = 0
            buy_shares_round_down = 0

        else:
            # finds how much percentage your portfolio is at
            current_percentage = current_money / total

            # calculates the variation
            variation = current_percentage / desired

            # calculates how many shares the user should buy
            # this will be rounded down
            buy_shares_round_down = math.floor(((total * desired) - current_money) / share_price)

        # how much it will cost to purchase the amount of shares
        cost_to_purchase = buy_shares_round_down * share_price

        conn.execute("UPDATE usersStock SET desired = ?, currentShare = ?, sharePrice = ?, "
                     "currentMoney = ?, currentPercentage = ?, variation = ?,buySharesRoundDown = ?,  "
                     "costToPurchase = ? WHERE stockTicker = ?; ",
                     (desired, current_share, share_price, current_money, current_percentage,
                      variation, buy_shares_round_down, cost_to_purchase, stock_ticker,))
        conn.commit()
    print("Database has been updated")


# this function will only update the desired value.
def update_desired_value(stock, desired, amount):
    conn.execute("UPDATE usersStock SET desired = ?, currentShare = ? WHERE stockTicker = ?", (desired, amount, stock))
    conn.commit()


# this function will return the total money in user's portfolio
def current_money_function():
    current_sum = conn.execute("SELECT SUM(currentMoney) FROM usersStock")
    conn.commit()
    new_sum = current_sum.fetchone()
    if new_sum[0] is None:
        return 0
    else:
        return new_sum[0]


# this method will take in a decimal and return a string in percentage form
def decimal_to_percentage(decimal):
    decimal = math.ceil(decimal * 100)
    new_string = str(decimal) + "%"
    return new_string


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
