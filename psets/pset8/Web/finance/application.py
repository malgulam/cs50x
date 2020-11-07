import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, user_exists, add_new_user, success, create_user_portfolio, \
    display_user_portfolio, buy_shares, find_user_with_this_id, sell_stock, create_user_history, render_history, \
    _change_username, _change_password, _delete_account, checkOldPassword

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

#If you can find a wrap around, no problem but I want to do it with the user id
@app.route("/")
@login_required
def index():
    # return apology("TODO")
    # print(session)
    return redirect(f'/portfolio/{session["user_id"]}')

@app.route('/portfolio/<int:id>')
@login_required
def portfolio(id):
    """Show portfolio of stocks"""
    return display_user_portfolio(id)
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # return apology("TODO")
    if request.method == 'GET':
        return render_template('buy_stock.html')
    else:
        symbol = request.form['symbol']
        if not lookup(symbol):
            return apology('Symbol does not exist!', 403)
        shares = int(request.form['shares'])
        username = find_user_with_this_id(session['user_id'])
        buy_shares(Symbol=symbol, Shares=shares, Username=username)
        return redirect(f'/portfolio/{session["user_id"]}')
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # return apology("TODO")
    return render_history()

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        # print('rows: ', rows)
        # Ensure username exists and password is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #     return apology("invalid username and/or password", 403)
        #check if user already exists
        if len(rows) < 1:
            return apology("User does not exists!", 403)
        if user_exists(rows[0]['username']):
            #check if password_hash is equal to the password user typed in
            if not check_password_hash(rows[0]['hash'], request.form['password']):
                #return this error message if password is wrong
                return apology("invalid password", 403)
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            # Redirect user to home page
            return redirect(f"/portfolio/{rows[0]['id']}")
        return apology("Username does not exist!", 403)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # return apology("TODO")
    return render_template('quote.html')

@app.route("/lookup_results", methods=['GET', 'POST'])
def lookup_results():
    symbol = request.form['symbol']
    results = lookup(symbol)
    if not results:
        return f"No stock found with the symbol {symbol}"
    return render_template("lookup_results.html", results=results)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # return apology("TODO")
    return render_template("register.html")

@app.route("/register_authentification", methods=['POST', 'GET'])
def register_authentification():
    if request.method == 'GET':
        return apology("Wrong request method type!")
    else:
        username = request.form["username"]
        password = request.form["password"]
        if not user_exists(username):
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            add_new_user(Username=username, Hash=hashed_password)
            create_user_portfolio(Username=username)
            create_user_history(Username=username)
            return success(message="Successfully created account!", links="login", method='POST', name='Login')
        return "<h1>User already exists</h1>"

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # return apology("TODO")
    if request.method == 'GET':
        return render_template('sell_stock.html')
    else:
        symbol = request.form['symbol']
        shares = int(request.form['shares'])
        return sell_stock(Symbol=symbol, Shares=shares, id=session['user_id'])

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    return render_template('settings.html')

@app.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    if request.method == 'GET':
        return render_template('change_username.html')
    else:
        old_username = request.form['OUsername']
        new_username = request.form['NUsername']
        if not _change_username(Old_Username=old_username, New_Username=new_username):
            return '<h1>There was a problem changing your username.Try again later!</h1>'
        logout()
        return success(title='Changed Username!', message="Successfully changed username!", links='login', method='GET', name='Login')

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')
    else:
        old_password = request.form['OPassword']
        new_password = request.form['NPassword']
        new_hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        old_hashed_password = generate_password_hash(old_password, method='pbkdf2:sha256', salt_length=8)
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=find_user_with_this_id(session['user_id']))
        #validate if old password is correct
        if not check_password_hash(rows[0]['hash'], request.form['OPassword']):
        # if not checkOldPassword(old_hashed_password):
            return '<h1>Old password incorrect!</h1>'
        if not _change_password(Old_Hash=old_hashed_password, New_Hash=new_hashed_password):
            return '<h1>There was problem changing your password.Try again later!</h1>'
        logout()
        return success(title='Changed Password!', message='Successfully changed password!', method='GET',name='Login')
#todo: logout user after performing changes and deletes
@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'GET':
        return render_template('delete_account.html')
    else:
        username = request.form['Username']
        password = request.form['Password']
        password_hash =generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        if not _delete_account(Username=username, Password=password_hash):
            return '<h1>There was a problem deleting your account!</h1>'
        logout()
        return success(title='Successfully Deleted!', message='Successfully deleted your account', links='register', method='GET', name='Register')
        #todo : logout
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run()