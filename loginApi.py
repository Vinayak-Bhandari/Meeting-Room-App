from flask import Flask,request,render_template,jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import  json
# import pandas as pd
# import json
app = Flask(__name__)
CORS(app)

#Tanushree Database credential
conn = psycopg2.connect(dbname="sql_demo", user="postgres",
                    password="currentele" , host="127.0.0.1")

#Vinayak Database credential
# conn = psycopg2.connect(dbname="postgres", user="postgres",
#                     password="123456" , host="127.0.0.1")

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


@app.route('/bookingStatus',methods=['POST', 'GET'])
def sellerform():
    cursor = conn.cursor()
    req = request.get_json()
    name = req['name']
    email=req['email']
    phone=req['phone']
    time=req['time']
    date=req['date']

    if request.method == 'POST':
        if name and email and phone and time and date :
            cursor = conn.cursor()
            sql = '''INSERT INTO public."bookingStatus" (name,email,phone,time,date)  VALUES ('{0}' ,'{1}' ,'{2}','{3}','{4}')'''.format(
                            name,email,phone,time,date)
           
            cursor.execute(sql)
                    
            conn.commit()
            cursor.close()
            resp = jsonify({'message': 'Room Booked Successfully', "status": True})
            resp.status_code = 200
            return resp

        

        # For empty values of email , password , username
        elif name == '' or email == '' or phone == '' or time == '' or date== '':
            resp = jsonify(
                {'message': 'Please fill the form correctly', 'status': False})
            resp.status_code = 200
            return resp
    elif request.method == 'GET':
        resp = jsonify(
            {'message': 'Bad Request! , Please check your request method', 'status': False})
        resp.status_code = 400
        return resp

    
       
if __name__ == '__main__':
    app.run()
