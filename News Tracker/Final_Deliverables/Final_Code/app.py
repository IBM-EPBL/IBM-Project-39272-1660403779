from flask import Flask, render_template, request,session,redirect,flash
from flask_session import Session
import ibm_db, json, requests

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
con = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;UID=frc91862;PWD=tVE4xOjs6QYRzQNC","","")

url = "https://bing-news-search1.p.rapidapi.com/news/search"
headers = {
    "X-BingApis-SDK": "true",
    "X-RapidAPI-Key": "2aa0169638msh69714997ed3b565p1cd48djsn73ea6e4776cf",
    "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
}
querystring = {"q":"","freshness":"Day","textFormat":"Raw","safeSearch":"Off"}
data = requests.request("GET", url, headers=headers, params=querystring)
data = data.json()


@app.route('/',methods=['GET','POST'])
def Home():
    if not session.get("name"):
        return render_template("Home.html")
    usernews = []
    sql = "select search from users where username = ?"
    stmt = ibm_db.prepare(con,sql)
    ibm_db.bind_param(stmt,1,session.get("name"))
    ibm_db.execute(stmt)
    string = ibm_db.fetch_assoc(stmt)
    
    if string["SEARCH"] != None:
        for sest in string["SEARCH"].split("/"):
            queryst = {"q":sest,"freshness":"Day","textFormat":"Raw","safeSearch":"Off"}
            news = requests.request("GET", url, headers=headers, params=queryst)
            news = news.json()
            usernews.append(news)
    usernews.append(data)
    return render_template("Welcome.html",value=usernews)

@app.route('/login', methods=['GET','POST'])
def Login():
   
    if request.method == 'POST':
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
        if username == False:
            flash("Password does not match with Username!")
            return redirect("/")
        elif username["USERNAME"] != None:
            session["name"] = username["USERNAME"]
            return redirect("/")
        else:
            flash('Login Failed','error')
            return redirect("/")
    flash('Login Failed','error')
    return redirect("/")

@app.route("/user",methods=['GET','POST'])
def User():

    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if len(name) != 0 and len(password) != 0 and len(email) != 0:
            sql = "Select * from Users where username = ? and password = ?"
            stmt = ibm_db.prepare(con,sql)
            ibm_db.bind_param(stmt,1,name)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            array = json.dumps(account)
            username = json.loads(array)
            
            if username == False or username["USERNAME"] == None:
                sql = "insert into users values(?,?,?,?);"
                stmt = ibm_db.prepare(con,sql)
                ibm_db.bind_param(stmt,1,name)
                ibm_db.bind_param(stmt,2,password)
                ibm_db.bind_param(stmt,3,email)
                ibm_db.bind_param(stmt,4,None)
                ibm_db.execute(stmt)
                return render_template("Home.html")
            flash("User Name Exist!")
            return redirect("/userpage")
    flash("Please provide all the credentials to sign up")
    return redirect("/userpage")

@app.route("/userpage")
def Userpage():
    return render_template("CreateUser.html")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/search",methods=['POST'])
def Search():
    usernews = []
    query = request.form["query"]
    username = session.get("name")
    url = "https://bing-news-search1.p.rapidapi.com/news/search"
    headers = {
        "X-BingApis-SDK": "true",
        "X-RapidAPI-Key": "2aa0169638msh69714997ed3b565p1cd48djsn73ea6e4776cf",
        "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
    }
    querystring = {"q":query,"freshness":"Day","textFormat":"Raw","safeSearch":"Off"}
    data = requests.request("GET", url, headers=headers, params=querystring)
    data = data.json()
    sql = "select search from users where username = ?"
    stmt = ibm_db.prepare(con,sql)
    ibm_db.bind_param(stmt,1,username)
    ibm_db.execute(stmt)
    string = ibm_db.fetch_assoc(stmt)
    if query == "":
        usernews.append(data)
        return render_template("Welcome.html",value=usernews)
    if string["SEARCH"] == None:
        sql = "update users set search = ? where username = ?"
        stmt = ibm_db.prepare(con,sql)
        ibm_db.bind_param(stmt,1,query)
        ibm_db.bind_param(stmt,2,session.get("name"))
        ibm_db.execute(stmt)
        usernews.append(data)
        return render_template("Welcome.html",value=usernews)
    if not string["SEARCH"].__contains__(query):
        query += "/"+string["SEARCH"]
        sql = "update users set search = ? where username = ?"
        stmt = ibm_db.prepare(con,sql)
        ibm_db.bind_param(stmt,1,query)
        ibm_db.bind_param(stmt,2,session.get("name"))
        ibm_db.execute(stmt)
    usernews.append(data)
    return render_template("Welcome.html",value=usernews)

if __name__ == "__main__":
    app.run(debug=True)