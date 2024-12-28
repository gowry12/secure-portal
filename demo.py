from flask import Flask,render_template,jsonify,request
app=Flask(__name__)
#/ means home routing
@app.route('/')
def index():
    return "<h1>Hello hi</h1>"
#route means that after every slash new given. what is the name want be in the url

@app.route('/a')
def index1():
    return render_template("google.html")
@app.route('/about/<uname>')
def about(uname):
#i am giving a var name and call that in about.html
    return render_template("about.html",myname=uname)
#to print json 
@app.route('/api')
def json1():
    data={
        "name":"myname",
        "age":20
    }
    return jsonify(data),400  
@app.route('/api')
def about():
    data= request.args.get('api_key')
    return "<h1>done api</h1>",200
  
#we are giving debbug because after single modification we have to run the code, bcoz server doesn't know that new we given.instead pf every single run we can use debug
app.run(debug=True)
