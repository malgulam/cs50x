import sys
import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

from cs50 import SQL
import sqlite3

from datetime import datetime

def success(title="Success", message="Success", links=None, method=None, name=None):
    """Render message in a separate html page"""
    return render_template('success.html', title=title, message=message, links=links, method=method)

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def user_exists(username):
    sys.path.append('.')
    conn = None
    try:
        db = 'finance.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = :username", (username,))
        users = list(c.fetchall())
        if len(users) != 1:
            return False
        return True
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)
        return False

def add_new_user(Username, Hash):
    sys.path.append('.')
    conn = None
    try:
        db = 'finance.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''INSERT INTO users(username, hash) VALUES (?,?)''', (Username, Hash))
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)

def create_user_portfolio(Username):
    sys.path.append('.')
    conn = None
    try:
        db = 'finance.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {Username}_portfolio(Symbol VARCHAR(10), Name VARCHAR(200), Shares INTEGER, Price DECIMAL(16,2), Total_Shares_Owned DECIMAL(16,2))''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)

def create_user_history(Username):
    sys.path.append('.')
    conn = None
    try:
        db = 'finance.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {Username}_history(Symbol VARCHAR(10), Name VARCHAR(200), Shares INTEGER, Price DECIMAL(16,2), Purchase_Type VARCHAR(5), date_created DATETIME)''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)

def display_user_portfolio(user_id):
    #determine which user's protfolio we are trying to locate
    sys.path.append('.')
    conn = None
    '''user list contents with index:
    [0] -- id
    [1] -- username
    [2] -- hash
    [3] -- cash
    '''
    try:
        db = 'finance.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''SELECT * FROM users WHERE id = :id''', (user_id,))
        user = list(c.fetchall())
        username = user[0][1]
        cash = user[0][3]
        print("Username: ", username)
        print("Cash: ", cash)
        c.execute(f'SELECT * FROM {username}_portfolio')
        portfolio_contents = list(c.fetchall())
        print('PORTFOLIO CONTENTS: ', portfolio_contents)
        return render_template('portfolio.html', portfolio=portfolio_contents, cash=usd(cash))
    except sqlite3.OperationalError as e:
        print(e)
def find_user_with_this_id(id):
    conn = None
    try:
        db = 'finance.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''SELECT * FROM users WHERE id = :id''', (id,))
        user = list(c.fetchall())
        username = user[0][1]
        conn.close()
        return username
    except sqlite3.OperationalError as e:
        print(e)

def history(Symbol, Name, Shares, Price, Purchase_Type, Date=datetime.utcnow()):
    conn = None
    db = 'finance.db'
    username = session['user_id']
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        date = datetime.utcnow()
        c.execute(
            f'''INSERT INTO George_history(Symbol, Name, Shares, Price, Purchase_Type, date_created) VALUES(?,?,?,?,?,?)''',
            (Symbol, Name, Shares, Price, Purchase_Type, date))
        # c.execute(f'''INSERT INTO {username}_history(Symbol, Name, Shares, Price, Purchase_Type, date_created) VALUES(?,?,?,?,?)''', (Symbol, Name, Shares, Price, Purchase_Type, Date))
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)

def ownStock(Symbol):
    conn = None
    db = 'finance.db'
    username = find_user_with_this_id(int(session['user_id']))
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'''SELECT * FROM {username}_portfolio WHERE Symbol = :symbol AND Shares > 0''', (Symbol,))
        found_symbols = list(c.fetchall())
        if not found_symbols:
            conn.close()
            return False
        conn.close()
        return True
    except sqlite3.OperationalError as e:
        print(e)

def buy_shares(Symbol, Shares, Username):
    #receive all vital information concerning the stock
    results = lookup(symbol=Symbol)
    price = results['price']
    name = results['name']
    total_cost = price * Shares
    conn = None
    db = 'finance.db'
    #determine if user has the stock already
    if not ownStock(Symbol):
        #create new stock entry in database
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            #first deduct the amount from the user's cash
            c.execute('''SELECT * FROM users WHERE username = :username''', (Username,))
            original_cash = list(c.fetchall())[0][3]
            new_cash = int(original_cash - total_cost)
            c.execute('''UPDATE users SET cash = :new_cash WHERE username = :username''', (new_cash, Username))
            conn.commit()
            #append the symbol, name, shares, price, all_shares owned to the db
            all_shares_owned = Shares
            c.execute(f'''INSERT INTO {Username}_portfolio(Symbol, Name, Shares, Price, Total_Shares_Owned) VALUES(?,?,?,?,?)''', (Symbol, name, Shares, price, all_shares_owned))
            conn.commit()
            conn.close()
            history(Symbol, Name=results['name'], Shares=Shares, Price=price, Purchase_Type='Buy')
            return
        except sqlite3.OperationalError as e:
            print(e)
    #if user has the stock!
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        # first deduct the amount from the user's cash
        c.execute('''SELECT * FROM users WHERE username = :username''', (Username,))
        original_cash = list(c.fetchall())[0][3]
        new_cash = int(original_cash - total_cost)
        c.execute('''UPDATE users SET cash = :new_cash WHERE username = :username''', (new_cash, Username))
        conn.commit()
        #append the symbol, name, shares, price, all_shares_owned to db
        all_shares_owned = 0
        #finding out the current shares owned by user
        c.execute(f'''SELECT * FROM {Username}_portfolio WHERE Symbol = :symbol''', (Symbol,))
        # all_shares_owned = int(list(c.fetchall())[0][4]) + Shares
        all_shares_owned = int(list(c.fetchall())[0][4]) + Shares
        print('ALL SHARES OWNED: ', all_shares_owned)
        # c.execute(
        #     f'''INSERT INTO {Username}_portfolio(Symbol, Name, Shares, Price, Total_Shares_Owned) VALUES(?,?,?,?,?)''',
        #     (Symbol, name, Shares, price, all_shares_owned))
        c.execute(f'''UPDATE {Username}_portfolio  SET Total_Shares_Owned = :shares_owned WHERE Symbol = :symbol ''', (all_shares_owned,Symbol))
        conn.commit()
        conn.close()
        history(Symbol, Name=results['name'], Shares=Shares, Price=price, Purchase_Type='Buy')
    except sqlite3.OperationalError as e:
        print(e)
# def buy_shares(Symbol, Shares, Username):
#     #first determine  symbol, name, shares, price, total
#     results = lookup(symbol=Symbol)
#     symbol = results['symbol']
#     price = results['price']
#     name = results['name']
#     total_cost = price * Shares
#     conn = None
#     try:
#         db = 'finance.db'
#         conn = sqlite3.connect(db)
#         c = conn.cursor()
#         #first deduct the new expenses from the user's money
#         c.execute('''SELECT * FROM users where username = :username''', (Username,))
#         original_cash = list(c.fetchall())[0][3]
#         new_cash = int(original_cash - total_cost)
#         c.execute('''UPDATE users SET cash = :cash''', (new_cash,))
#         conn.commit()
#         #secondly append the symbol, name, shares, price, All_shares_owned to the db
#         c.execute(f'''SELECT * FROM {Username}_portfolio WHERE Symbol = :symbol''', (Symbol,))
#         all_findings = list(c.fetchall())
#         all_shares_owned = 0
#         if not all_findings:
#             pass
#         else:
#             for finding in all_findings:
#                 index = all_findings.index(finding)
#                 all_shares_owned += all_findings[index][2]
#         if not all_shares_owned:
#             all_shares_owned += int(Shares)
#
#         print("ALL SHARES: ", all_shares_owned)
#         c.execute(f'''INSERT INTO {Username}_portfolio(Symbol, Name, Shares, Price, Total_Shares_Owned) VALUES(?,?,?,?,?)''', (Symbol, name, Shares, price, all_shares_owned))
#         conn.commit()
#         conn.close()
#     except sqlite3.OperationalError as e:
#         print(e)

def sell_stock(Symbol, Shares, id):
    db = 'finance.db'
    conn = None
    username  = find_user_with_this_id(id)
    if not ownStock(Symbol):
        return f'<h1>You do not own a stock with symbol: {Symbol}</h1>'
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'''SELECT * FROM {username}_portfolio WHERE Symbol = :symbol''', (Symbol,))
        # total_shares_owned = list(c.fetchall())[0][5]
        total_shares_owned = list(c.fetchall())[0][4]
        print(total_shares_owned)
        #if shares is not less than or equal to toal_amount_shares then throw error
        if not Shares <= total_shares_owned:
            return '<h1>Shares owned do not reacthe target shares to sell</h1>'
        #find out price of stock and sell it the append money to
        results = lookup(Symbol)
        price = results['price']
        c.execute(f'''UPDATE users SET cash = cash + :new_cash WHERE username = :username''', (price, username))
        conn.commit()
        #Updating the stock owned by the person!
        c.execute(f'''UPDATE {username}_portfolio SET Total_Shares_Owned = Total_Shares_Owned - :Shares''', (Shares,))
        conn.commit()
        conn.close()
        history(Symbol, Name=results['name'], Shares=Shares, Price=price, Purchase_Type='Sell')
        return 'Stock sold!'
    except sqlite3.OperationalError as e:
        print(e)
# def sell_stock(Symbol, Shares, id):
#     db = 'finance.db'
#     conn = None
#     username = find_user_with_this_id(id)
#     try:
#         #determine if the user has the stock or not
#         conn = sqlite3.connect(db)
#         c = conn.cursor()
#         c.execute(f'''SELECT * FROM {username}_portfolio WHERE Symbol = :symbol''', (Symbol,))
#         present_symbols = list(c.fetchall())
#         if not present_symbols:
#             return f'<h1>You do not own a stock with symbol: {Symbol}</h1>'
#         total_shares_of_symbol = 0
#         for symbol_share in present_symbols:
#             total_shares_of_symbol += int(symbol_share[2])
#         print("TOTAL SHARES: ", total_shares_of_symbol)
#         if total_shares_of_symbol <= Shares:
#             #todo: actually sell
#             c.execute(f'''UPDATE {username}_portfolio SET Shares = :shares WHERE Symbol = :symbol''', (int(total_shares_of_symbol-Shares), Symbol))
#             conn.commit()
#             print('HERE')
#             #todo: add to history
#         return '<h1>Your current holdings are less than the number of shares you want to sell.</h1>'
#     except sqlite3.OperationalError as e:
#         print (e)


def render_history():
    conn = None
    db = 'finance.db'
    username = find_user_with_this_id(session['user_id'])
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'''SELECT * FROM {username}_history''')
        history = list(c.fetchall())
        conn.close()
        return render_template('history.html', history=history)
    except sqlite3.OperationalError as e:
        print(e)

def _change_username(Old_Username, New_Username):
    conn = None
    db = 'finance.db'
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'''UPDATE users SET username = :new_username WHERE username = :old_username''', (New_Username, Old_Username))
        conn.commit()
        conn.close()
        return True
    except sqlite3.OperationalError as e:
        print(e)
        return False

def checkOldPassword(Old_Hash):
    conn = None
    db = 'finance.db'
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'''SELECT * FROM users WHERE hash = :old_hash''', (Old_Hash,))
        all_found_hashes = list(c.fetchall())
        print('ALL FOUND HASHES: ', all_found_hashes)
        if len(all_found_hashes) < 1:
            return False
        return True
    except sqlite3.OperationalError as e:
        print(e)
        return False

def _change_password(Old_Hash, New_Hash):
    conn = None
    db = 'finance.db'
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        # c.execute(f'''UPDATE users SET hash = ':new_hash' WHERE hash = :old_hash''', (New_Hash, Old_Hash))
        username = find_user_with_this_id(session['user_id'])
        c.execute(f'''UPDATE users SET hash = :new_hash WHERE username = :Username''', (New_Hash, username))
        conn.commit()
        conn.close()
        return True
    except sqlite3.OperationalError as e:
        print(e)
        return False

def _delete_account(Username, Password):
    conn = None
    db = 'finance.db'
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'''DELETE FROM users WHERE username= :Username AND hash = :Password''', (Username, Password))
        conn.commit()
        #delete user portfolio and history
        c.execute(f'''DROP TABLE {Username}_portfolio''')
        conn.commit()
        c.execute(f'''DROP TABLE {Username}_history''')
        conn.commit()
        conn.close()
        return True
    except sqlite3.OperationalError as e:
        print(e)
        return False
