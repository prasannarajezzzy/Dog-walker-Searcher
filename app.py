# from distutils.log import debug
from flask import Flask, render_template,request
import getData
import pyrebase
import requests


app = Flask(__name__)



@app.route('/',methods=["POST","GET"])

def index():
    if request.method=='POST':
            print(request.form['searchText'])
            query = str(request.form['searchText'])
            data = getData.companyName(query)
            print("fulll")
            print(data)
            return  render_template("result.html",data = data) 

    return  render_template("index.html") 
    
if __name__ == "__main__":
    app.run(debug=True)