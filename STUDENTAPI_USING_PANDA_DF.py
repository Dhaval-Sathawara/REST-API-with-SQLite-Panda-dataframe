from flask import Flask, jsonify,request
import json
import sqlite3
import pandas as pd

app=Flask(__name__,static_folder='/static')

def get_html_body(html_table,title=""):
    styled_html = f"""
        <html>
        <head>
        <style>
        
        h2 {{color: darkred;
        font-family: cambria;
        padding: 8px;
        font-size: 32px;
        text-align: center;
        }}

       table {{
            width: 60%;
            border-collapse: collapse;
            margin: 20px auto;
        }}
        th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: skyblue;
            color: black;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        </style>
            
        </head>
        <body>
            <h2> Database {title}</h2> 
            {html_table}
        </body>
        </html>
        """
    return styled_html

def check_or_create_db():
    try:
        conn = sqlite3.connect('MYDB.db')
        cursor = conn.execute("SELECT * FROM STUDENT_TABLE")
        conn.commit()
        conn.close()
    except:
        conn = sqlite3.connect('MYDB.db')
        conn.execute('''CREATE TABLE STUDENT_TABLE
                 (NO INTEGER PRIMARY KEY AUTOINCREMENT,
                 USN INT NOT NULL,
                 NAME TEXT NOT NULL,
                 BRANCH TEXT NOT NULL,
                 MARKS INT NOT NULL);
                 ''')
        conn.commit()
        conn.close()

#=============================================================
@app.route('/',methods=['GET'])
def index_page():
    str1="""
<!DOCTYPE html>
<html>
<head>
<style>
body {background-color: WHITE;}
h1   {color: blue;}
h2    {color: darkred;}
</style>
</head>
<body>

<h1>Hi Dhaval,</h1>
<h2>This is Index page of Application Programming Interface (API).</h2>

</body>
</html>

    """
    return str1
#=============================================================


#  link rel="stylesheet" type="text/css" href="/MYSTYLE.css"/>
#=============================================================
@app.route('/getalldata',methods=['GET'])
def display_data():
    conn = sqlite3.connect('MYDB.db')
    try:
        df = pd.read_sql_query("SELECT * from STUDENT_TABLE", conn)
        conn.close()
        html_table = df.to_html(index=False,border=1)

        styled_html=get_html_body(html_table)
        
        return styled_html
    except:
        return jsonify({"message":"Error in GET all data"})
#=============================================================

#=============================================================
@app.route('/getno/<id>',methods=['GET'])
def display_id_data(id):
    conn = sqlite3.connect('MYDB.db')
    try:
        df = pd.read_sql_query(f"SELECT NO,USN,NAME,BRANCH,MARKS FROM STUDENT_TABLE WHERE NO = {id}", conn)
        conn.close()
        html_table = df.to_html(index=False,border=1)
        styled_html=get_html_body(html_table,title=f" of ID :: {id}")
        return styled_html
    except:
        return jsonify({"message":"Error in GET NO data"})
#=============================================================

#=============================================================
@app.route('/getname/<string:name>',methods=['GET'])
def display_name_data(name):
    conn = sqlite3.connect('MYDB.db')
    try:
        df = pd.read_sql_query(f"SELECT NO,USN,NAME,BRANCH,MARKS FROM STUDENT_TABLE WHERE NAME = '{name}'", conn)
        conn.close()
        html_table = df.to_html(index=False,border=1)
        styled_html=get_html_body(html_table,title=f" of Name :: {name}")
        return styled_html
    except:
        return jsonify({"message":"Error in GET NAME data"})
#=============================================================

#=============================================================
@app.route('/getbranch/<brname>',methods=['GET'])
def display_branch_data(brname):
    conn = sqlite3.connect('MYDB.db')
    try:
        df = pd.read_sql_query(f"SELECT NO,USN,NAME,BRANCH,MARKS FROM STUDENT_TABLE WHERE BRANCH = '{brname}'", conn)
        conn.close()
        html_table = df.to_html(index=False,border=1)
        styled_html=get_html_body(html_table,title=f" of Name :: {brname}")
        return styled_html
    except:
        return jsonify({"message":"Error in GET NAME data"})
#=============================================================

#=============================================================
@app.route('/updateno/<id>',methods=['PUT']) 
def update_id_data(id):
    conn = sqlite3.connect('MYDB.db')
    try:
        data = request.get_json()
        conn.execute(f"UPDATE STUDENT_TABLE set \
        USN = {data['USN']}, NAME = '{data['NAME']}', \
        BRANCH = '{data['BRANCH']}', MARKS = {data['MARKS']} where NO = {id}");
        conn.commit()
        conn.close()
        return data   
    except:
        conn.close()
        return jsonify({"message":"error in UPDATE NO. data"})
#=============================================================

#=============================================================
@app.route('/postdata', methods=['POST'])
def add_data():
    check_or_create_db()
    conn = sqlite3.connect('MYDB.db')
    try:
        data = request.get_json()
        conn.execute(f"INSERT INTO STUDENT_TABLE (USN,NAME,BRANCH,MARKS) \
        VALUES ({data['USN']},'{data['NAME']}', '{data['BRANCH']}', {data['MARKS']})");
        conn.commit()
        conn.close()
        
        return data    
    except:
        conn.close()
        return jsonify({"message":"Error in POST data"})
#=============================================================

#=============================================================
@app.route('/deleteno/<id>',methods=['DELETE']) 
def delete_id_data(id):
    conn = sqlite3.connect('MYDB.db')
    try:
        conn.execute(f"DELETE from STUDENT_TABLE where NO = {id}")
        conn.commit()
        conn.close()
        return jsonify({"message":f"data of {id} deleted successfully"})
    except:
        conn.close()
        return jsonify({"message":"error in DELETE NO. data"})
#=============================================================

#=============================================================
@app.route('/deleteall',methods=['DELETE']) 
def delete_all_data():
    try:
        conn = sqlite3.connect('MYDB.db')
        #drop table
        conn.execute("DROP TABLE STUDENT_TABLE")
        conn.close()

        conn = sqlite3.connect('MYDB.db')
        conn.execute('''CREATE TABLE STUDENT_TABLE
                 (NO INTEGER PRIMARY KEY AUTOINCREMENT,
                 USN INT NOT NULL,
                 NAME TEXT NOT NULL,
                 BRANCH TEXT NOT NULL,
                 MARKS INT NOT NULL);
                 ''')
        conn.commit()
        conn.close()
        
        return jsonify({"message":"All data deleted"})
    except:
        
        return jsonify({"message":"error in DELETE ALL data"})

#=============================================================

app.run(port=5432)
