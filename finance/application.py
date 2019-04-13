import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=session["user_id"])
    stocks = db.execute("SELECT * FROM portfolio WHERE user=:user", user=user[0]["username"])
    cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])
    stocks_owned = db.execute("SELECT * FROM holdings WHERE user=:user", user=user[0]["username"])

    grand_total = 0

    for dicts in stocks_owned:
        for keys in dicts:
            if keys == "total":
                grand_total = grand_total + dicts[keys]
            if keys == "price" or keys == "total":
                dicts[keys] = usd(dicts[keys])

    grand_total = usd(grand_total + cash[0]["cash"])

    return render_template("index.html", stocks_owned=stocks_owned, cash=usd(cash[0]["cash"]), grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # Open the buy page
    render_template("buy.html")

    # User reached via POST
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("Missing Symbol", 400)

        # Ensure shares were submitted
        if not request.form.get("shares"):
            return apology("Missing Shares", 400)

        # Ensure shares are a positive integer
        try:
            val = int(request.form.get("shares"))
        except ValueError:
            return apology("Enter a positive integer of shares", 400)

        # Ensure shares are positive
        if int(request.form.get("shares")) < 0:
            return apology("Enter a positive integer of shares", 400)

        # Lookup the symbol
        num_shares = float(request.form.get("shares"))
        quote = lookup(request.form.get("symbol"))

        # Check if symbol is valid
        if quote is None:
            return apology("Invalid Symbol", 400)

        price_of_share = quote["price"]

        # Does buyer have enough cash to buy the stock?
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        if float(cash[0]["cash"]) < price_of_share * num_shares:
            return apology("Insufficient Funds", 400)

        # Update cash user has left
        total_left = float(cash[0]["cash"]) - price_of_share * num_shares
        db.execute("UPDATE users SET cash = :total_left WHERE id = :user_id", total_left=total_left, user_id=session["user_id"])

        # Add stock to users portfolio
        # Find user
        username = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Insert stock into portfolio (really transaction history)
        db.execute("INSERT INTO portfolio (user, symbol, name, shares, price, total) VALUES (:user, :symbol, :name, :shares, :price, :total)",
                   user=username[0]["username"], symbol=quote["symbol"], name=quote["name"], shares=num_shares, price=price_of_share, total=num_shares * price_of_share)

        # Insert shares into holdings if stock is not owned
        held = db.execute("INSERT INTO holdings (user, symbol, name, shares_owned, price, total) VALUES (:user, :symbol, :name, :shares, :price, :total)",
                          user=username[0]["username"], symbol=quote["symbol"], name=quote["name"], shares=num_shares, price=price_of_share, total=num_shares * price_of_share)
        if not held:
            held = db.execute("UPDATE holdings SET shares_owned = shares_owned + :shares, price = :price, total = (shares_owned + :shares) * :price WHERE user = :user AND symbol=:symbol",
                              shares=num_shares, user=username[0]["username"], price=price_of_share, symbol=quote["symbol"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Find user and all transactions
    username = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])
    transactions = db.execute("SELECT * FROM portfolio WHERE user = :user", user=username[0]["username"])

    for dicts in transactions:
        for keys in dicts:
            if keys == "price" or keys == "total":
                dicts[keys] = usd(dicts[keys])

    return render_template("history.html", transactions=transactions)


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

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/password", methods=["GET", "POST"])
def password():
    """Change password"""

    # User reached route via POST (submitted a form)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure NEW password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure NEW confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure NEW password and confirmation are the same
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation do not match", 400)

        # Does NEW password pass strength requirements
        pswd = request.form.get("password")
        if pswd.islower():
            return apology("password must contain at least one capital letter")
        elif pswd.isupper():
            return apology("password must contain at least one lower case letter")
        elif pswd.isalpha():
            return apology("password must contain at least one number")
        elif len(pswd) < 6:
            return apology("password must contain at least 6 characters")

        # Encrypt NEW password
        hash = generate_password_hash(request.form.get("password"))

        # Update password
        db.execute("UPDATE users SET hash = :hash WHERE username = :user",
                   user=request.form.get("username"), hash=hash)

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("password.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # Open the quote form page
    render_template("quote.html")

    # User reached route via POST
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("Missing Symbol", 400)

        # Lookup the symbol
        quote = lookup(request.form.get("symbol"))

        # Check if symbol is valid
        if quote is None:
            return apology("Invalid Symbol", 400)

        return render_template("display_quote.html", name=quote["name"], symbol=quote["symbol"], price=usd(quote["price"]))

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (submitted a form)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and confirmation are the same
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation do not match", 400)

        # Does password pass strength requirements
        pswd = request.form.get("password")
        if pswd.islower():
            return apology("password must contain at least one capital letter")
        elif pswd.isupper():
            return apology("password must contain at least one lower case letter")
        elif pswd.isalpha():
            return apology("password must contain at least one number")
        elif len(pswd) < 6:
            return apology("password must contain at least 6 characters")

        # Encrypt password
        hash = generate_password_hash(request.form.get("password"))

        # Insert user into database
        rows = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                          username=request.form.get("username"), hash=hash)
        if not rows:
            return apology("username already exists", 400)

        # Automatically log user in after they register
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Open the sell page
    username = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])
    stocks_owned = db.execute("SELECT * FROM holdings WHERE user=:user", user=username[0]["username"])
    #render_template("sell.html", stocks_owned=stocks_owned)

    # User reached via POST
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("Missing Symbol", 400)

        # Ensure shares were submitted
        if not request.form.get("shares"):
            return apology("Missing Shares", 400)

        # Lookup the symbol
        num_shares = int(request.form.get("shares"))
        quote = lookup(request.form.get("symbol"))

        # Check if symbol is valid
        if quote is None:
            return apology("Invalid Symbol", 400)

        price_of_share = quote["price"]

        # Does user have enough shares to sell?
        shares = db.execute("SELECT shares_owned FROM holdings WHERE user = :user AND symbol = :symbol",
                            user=username[0]["username"], symbol=quote["symbol"])

        # If not return apology
        if shares[0]["shares_owned"] < num_shares:
            return apology("You can not sell mores shares than you own", 400)

        # If user will sell all shares, then delete from holdings
        if shares[0]["shares_owned"] == num_shares:
            shares = db.execute("DELETE FROM holdings WHERE user = :user AND symbol = :symbol",
                                user=username[0]["username"], symbol=quote["symbol"])
        else:
            shares = db.execute("UPDATE holdings SET shares_owned = shares_owned - :num_shares, price = :price, total = (shares_owned - :num_shares) * :price WHERE user = :user AND symbol = :symbol",
                                user=username[0]["username"], symbol=quote["symbol"], num_shares=num_shares, price=price_of_share)

        # Update cash user has left
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        total_left = float(cash[0]["cash"]) + price_of_share * num_shares
        db.execute("UPDATE users SET cash = :total_left WHERE id = :user_id", total_left=total_left, user_id=session["user_id"])

        # Insert sell transaction into portfolio (really transaction history)
        db.execute("INSERT INTO portfolio (user, symbol, name, shares, price, total) VALUES (:user, :symbol, :name, :shares, :price, :total)",
                   user=username[0]["username"], symbol=quote["symbol"], name=quote["name"], shares=-num_shares, price=price_of_share, total=-num_shares * price_of_share)

        return redirect("/")

    else:
        return render_template("sell.html", stocks_owned=stocks_owned)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
