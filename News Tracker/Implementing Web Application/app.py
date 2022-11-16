from flask import Flask, render_template, request
import ibm_db, json
app = Flask(__name__)

@app.route('/')
def Home():
    return render_template("Home.html")

@app.route('/login', methods=['POST'])
def Login():
 
    con = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;UID=frc91862;PWD=tVE4xOjs6QYRzQNC","","")

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        name = request.form['username']
        password = request.form['password']
        sql = "Select * from Users where username = ? and password = ?"
        stmt = ibm_db.prepare(con,sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        array = json.dumps(account)
        username = json.loads(array)
        if username["USERNAME"] != None:
            return render_template("Welcome.html",value=username["USERNAME"])
        else:
            return render_template("CreateUser.html",value="Login Failed")

@app.route("/user",methods=['POST'])
def User():

    con = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;UID=frc91862;PWD=tVE4xOjs6QYRzQNC","","")

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        name = request.form['username']
        password = request.form['password']
        if len(name) != 0 and len(password) != 0:
            sql = "Select * from Users where username = ? and password = ?"
            stmt = ibm_db.prepare(con,sql)
            ibm_db.bind_param(stmt,1,name)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            array = json.dumps(account)
            username = json.loads(array)
            
            if username == False:
                sql = "insert into users values(?,?);"
                stmt = ibm_db.prepare(con,sql)
                ibm_db.bind_param(stmt,1,name)
                ibm_db.bind_param(stmt,2,password)
                ibm_db.execute(stmt)
                return render_template("Home.html")
            return "<h1>User Name Exist</h1>"

    return "<h1>Account creation failed</h1>"

@app.route("/userpage")
def Userpage():
    return render_template("CreateUser.html")

if __name__ == "__main__":
    app.run(debug=True)