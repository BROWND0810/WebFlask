from flask import Flask 
app = Flask(__name__) 
@app.route("/hello") 
def hello(): 
   return "Hello, Welcome to Bowie State University" 
@app.route("/") 
def index(): 
   return "Homepage of Bowie State University" 
if __name__ == "__main__": 
   app.run(debug=True) 

