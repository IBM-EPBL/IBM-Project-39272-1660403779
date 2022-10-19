from flask import Flask, render_template, request
import psycopg2
app = Flask(__name__)

@app.route('/')
def Home():
    return render_template("Home.html")

@app.route('/login', methods=['POST'])
def Login():
    database = psycopg2.connect(
        password = "Sri@1702",
        user = "postgres",
        port = "5432",
        database = "Sri_17"
    )
    cursor = database.cursor()

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        name = request.form['username']
        password = request.form['password']
        cursor.execute("Select * from Users where username = '%s' and password = '%s'" %(name,password))
        account = cursor.fetchone()
        if account:
            return render_template("Welcome.html",value=account[0])
        else:
            return render_template("CreateUser.html",value="Login Failed")

@app.route("/user",methods=['POST'])
def User():
    database = psycopg2.connect(
        password = "Sri@1702",
        user = "postgres",
        port = "5432",
        database = "Sri_17"
    )
    cursor = database.cursor()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        name = request.form['username']
        password = request.form['password']
        if len(name) != 0 and len(password) != 0:
            cursor.execute("Select username from Users where username = '%s' and password = '%s'" %(name,password))
            account = cursor.fetchone()
            if account == '':
                cursor.execute("insert into Users values('%s','%s')" %(name, password))
                database.commit()
                database.close()
                return render_template("Home.html")
            return "<h1>User Name Exist</h1>"
    return "<h1>Account creation failed</h1>"

@app.route("/userpage")
def Userpage():
    return render_template("CreateUser.html")

if __name__ == "__main__":
    app.run(debug=True)