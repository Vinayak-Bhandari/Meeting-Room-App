# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 15:52:53 2022

@author: User
"""
from flask import Flask,request,jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import pandas as pd
import json
app = Flask(__name__)
CORS(app)


conn = psycopg2.connect(dbname="postgres", user="postgres",password="123456" , host="127.0.0.1")
print('Connected Successfully!!')

@app.route('/login',methods=["GET","POST"])
def login():
    cursor = conn.cursor()
    req = request.get_json()
    username = req['username']
    _password=req['password']
    
    if request.method == 'POST':
        if username and _password:
            # check user exists
            cursor = conn.cursor()
            # query to fetch the user details
            query='''select username,password,user_Id,user_type from public."Login" where username='{}' '''.format(username)
            print(query)
    
            cursor.execute(query)
            row = cursor.fetchone()
            
            try:
                
                username = row[0]
                password = row[1]
                user_id=row[2]
                user_types=row[3]
            except:
                pass
            
                
            if(row==None):
                resp = jsonify(
                    {'message': 'Entered Username and Password does not exist, Please register', 'status': False})
                resp.status_code = 200
                return resp
            # checking the user password is correct or not
            if row:
                if (_password==password):
                    cursor.close()
                    resp = jsonify({'message': 'Login Successfully', 'user_type':user_types,'user_id':user_id, 'status': True})
                    resp.status_code = 200
                    return resp

                # for invalid password
                else:
                    resp = jsonify(
                        {'message': 'Please enter correct password', 'status': False})
                    resp.status_code = 200
                    return resp

            # invalid email
            else:
                resp = jsonify(
                    {'message': 'Enter valid email', 'status': False})
                resp.status_code = 200
                return resp

        # empty values of email , password
        elif username == '' or password == '':
            resp = jsonify(
                {'message': 'Please fill your form correctly', 'status': False})
            resp.status_code = 200
            return resp

    # Bad request with invalid method
    elif request.method == 'GET':
        resp = jsonify(
            {'message': 'Bad Request! , Please check your request method', 'status': False})
        resp.status_code = 400
        return resp
    
@app.route('/register',methods=["GET","POST"])
def register():
    cursor = conn.cursor()
    req = request.get_json()
    username = req['username']
    email=req['email']
    password=req['password']
    phone=req['phone']
    
    if request.method=='POST':
        if username and email and password and phone:
            cursor.execute('''SELECT * from public."Login" where username='{}' '''.format(username))
            if cursor.fetchone() is not None:
                resp = jsonify(
                                {'message': 'Entered username  already exist , Please login', 'alreadyexist': True, "status": False})
                resp.status_code = 200
                return resp
   
            query='''insert into public."Login"(username , password , phone , email) values ('{0}' , '{1}' , '{2}' , '{3}')'''.format(username,password,phone,email)
    
            print(query)
    
            cursor.execute(query)
            conn.commit()
            cursor.close()
            esp = jsonify(
                {'message': 'Registered Successfully', "status": True})
            resp.status_code = 200
            return resp
 
        elif username== '' or password == '' or email == '' or phone == '':
            resp = jsonify(
                {'message': 'Please enter missed keys', 'status': False})
            resp.status_code = 200
            return resp
    elif request.method == 'GET':
        resp = jsonify(
            {'message': 'Bad Request! , Please check your request method', 'status': False})
        resp.status_code = 400
        return resp


    
@app.route('/bookingStatus',methods=['POST', 'GET'])
def sellerform():
    cursor = conn.cursor()
    req = request.get_json()
    name = req['name']
    email=req['email']
    phone=req['phone']
    time=req['time']
    date=req['date']
    room_id=req['room_id']
    user_id=req['user_id']
    room_name=req['room_name']
    room_url=req['room_url']

    if request.method == 'POST':
        if name and email and phone and time and date :
            cursor = conn.cursor()
            sql = '''INSERT INTO public."bookingStatus" (name,email,phone,time,date,room_id,user_id,room_name,room_url)  VALUES ('{0}' ,'{1}' ,'{2}','{3}','{4}','{5}','{6}','{7}','{8}')'''.format(
                            name,email,phone,time,date,room_id,user_id,room_name,room_url)
           
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
    
    
@app.route('/meetingRoom',methods=["GET","POST"])
def meetingRoom():
    cursor = conn.cursor()
    req = request.get_json()
    # room_id=req['room_id']
    roomCategary = req['room_category']
    
    if request.method == 'POST':
   # Bad request of invalid method
            cursor = conn.cursor()
            if(roomCategary=="small"):
                sql = ''' SELECT * FROM public."meetingRoom" where room_category='small' '''
            if(roomCategary=="medium"):
                sql = '''SELECT * FROM public."meetingRoom" where room_category='medium' '''  
            if(roomCategary=="Large"):
                sql = '''SELECT * FROM public."meetingRoom" where room_category='Large' '''
            cursor.execute(sql)
            row = cursor.fetchall()
            # checking the token access and reseting the password
            if row:
                # if 'username' in session:
                if row != None:
                    conn.commit()
                    cursor.close()
                    output = []
                    for s in row:
                        output.append({"room_id": s[0],
                                       "room_name": s[1],
                                       "room_description": s[2].replace('\n',''),
                                       "room_url": s[3],
                                       "inner_description":s[4].replace('\n',''),
                                       "room_availability":s[5].replace('\n','').split(',')
                                       })

                    # print(output)
                    return {"data" : output}

    # For invalid method
    elif request.method == 'POST':
        return jsonify({'message': 'Bad Request! , Please check your request method', 'status': False})
    
    
@app.route('/perticularRoom',methods=['GET','POST'])
def perticularRoom():
        cursor = conn.cursor()
        req = request.get_json()
        room_id = req['room_id']
    
        cursor = conn.cursor()
        query='SELECT * FROM public."meetingRoom" where room_id={}'.format(room_id);
        cursor.execute(query)
        data=cursor.fetchall()
        output=[]
        for s in data:
            output.append({"room_id": s[0],
                                       "room_name": s[1],
                                       "room_description": s[2].replace('\n',''),
                                       "room_url": s[3],
                                       "inner_description":s[4].replace('\n',''),
                                       "room_availability":s[5].replace('\n','').split(',')
                                       })
        return{"roomData":output}
  

@app.route('/alreadyBooked',methods=['GET','POST'])
def Booked():
        cursor = conn.cursor()
        query=''' SELECT name,phone,time,date,room_name,room_url FROM public."bookingStatus" ''';
        cursor.execute(query)
        data=cursor.fetchall()
        output=[]
        for s in data:
            output.append({"name": s[0],
                                       "phone": s[1],
                                       "time": s[2].strftime("%H:%M:%S"),
                                       "date": s[3].strftime("%d-%m-%Y"),
                                       "room_name":s[4],
                                       "room_url":s[5]
                                       })
        return {"bookedData":output,'status':True}
    
       
@app.route('/checkifbooked',methods=['GET','POST'])
def checkifbooked():
        cursor = conn.cursor()
        req = request.get_json()
        room_id = req['room_id']
        
        
        query=''' SELECT 1 FROM public."bookingStatus"  where room_id='{}' '''.format(room_id);
        cursor.execute(query)
        data=cursor.fetchall()
        
        try: 
            
            if (data[0][0]):
                resp = jsonify(
                {'message': 'Room Already booked,Choose another room', 'status': False})
                resp.status_code = 200
                return resp
        except:
                resp = jsonify(
                {'message': 'Book this room for the Meeting!!', 'status': True})
                resp.status_code = 200
                return resp
            
           
@app.route('/yourBookings',methods=['GET','POST'])
def yourBookings():
        cursor = conn.cursor()
        req = request.get_json()
        user_id = req['user_id']
    
        cursor = conn.cursor()
        query='''SELECT * FROM public."bookingStatus" where user_id='{}' '''.format(user_id);
        
        cursor.execute(query)
        data=cursor.fetchall()
        
        if len(data)>=1:
            output=[]
            for s in data:
                output.append({"room_id": s[5],
                                           "room_name": s[7],
                                           "name": s[0],
                                           "room_url": s[8],
                                           "email":s[1],
                                           "phone":s[2],
                                           "time": s[3].strftime("%H:%M:%S"),
                                           "date": s[4].strftime("%d-%m-%Y"),
                                           "user_id":s[6]
                                           })
            return{"yourData":output,"status":True}        
        else:
            return{"message":"Bookings are not Found for this user!","status":False}
        
        
@app.route('/cancelBooking',methods=['GET','POST'])
def cancelBooking():
        cursor = conn.cursor()
        req = request.get_json()
        room_id = req['room_id']
        
        if room_id:
    
            cursor = conn.cursor()
            query='''DELETE FROM public."bookingStatus" where room_id='{}' '''.format(room_id);
            
            cursor.execute(query)
            conn.commit()
            cursor.close()     
            return{"message":"Booking Canceled successfully!!","status": True}        
       
        else:
            return{"message":"Room Id not Found!!","status": False} 
            
    
if __name__ == '__main__':
   app.run()
   
   
  