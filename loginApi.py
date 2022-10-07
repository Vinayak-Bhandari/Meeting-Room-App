from flask import Flask,request,render_template
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import  json
# import pandas as pd
# import json
app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(dbname="sql_demo", user="postgres",
                    password="currentele" , host="127.0.0.1")

cursor = conn.cursor()
def execute_query(query):
    cursor=conn.cursor()
    try:
     cursor.execute(query)
     data=cursor.fetchall()
    except:
        data=''
    
    return data
    

@app.route('/login',methods=["GET","POST"])
def login():
    req = request.get_json()
    username = req['username']
    password=req['password']
    # username=request.args.get('username')
    # password=request.args.get('password')
    
    execute_query("rollback")
    query='''select 1 from public.login where username='{}' and password='{}' '''.format(username,password)
    print(query)
    
    data=execute_query(query)
    
    if(len(data)>0):
        return {"message":"login_success","status":True}
    
    else :
        return {"message":"login failure","status":False}
       

@app.route('/register',methods=["GET","POST"])
def register():
    req = request.get_json()
    username = req['username']
    email=req['email']
    password=req['password']
    phone=req['phone']
    # username=request.args.get('username')
    # password=request.args.get('password')
   
    query='''insert into public.login (username , password , phone , email) values ('{0}' , '{1}' , '{2}' , '{3}')'''.format(username,password,phone,email)
    
    print(query)
    
    cursor.execute(query)
    conn.commit()
    return {"message":"Register Successfully","status":True}

    
       
if __name__ == '__main__':
    app.run()
