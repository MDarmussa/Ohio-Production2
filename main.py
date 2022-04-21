from flask import Flask, request, render_template, redirect, url_for
# from flask import *
from flask_wtf import FlaskForm
import pandas as pd
import sqlite3
import os


app = Flask(__name__)


def create_interg_db():
     df = pd.read_excel('productiondata.xls')
     df = df.rename(columns={"API WELL  NUMBER": "well_number", "OIL":"oil", "GAS":"gas", "BRINE":"brine", "QUARTER 1,2,3,4": "quarter"})

     # Filtering Data by Quarters (please remove (#) on line 21 then commet out line 18 to test it)
     # 1- Q1 and Q3
     df = df[df['quarter'].eq(1) | df['quarter'].eq(3)]

     # 2-  Q1, Q3 and Q4
     # df = df[df['quarter'].eq(1) | df['quarter'].eq(3) | df['quarter'].eq(4)]

     # 2-  Q2 
     # df = df[df['quarter'].eq(2)]


     df = df.groupby(['well_number']).sum()
     final_df = df[['oil', 'gas', 'brine']]
     connection = sqlite3.connect('inerg.db')
     final_df.to_sql('data', connection, if_exists='replace')
     connection.close()


def get_db_connection():
     connection = sqlite3.connect('inerg.db')
     return connection


@app.route('/')
@app.route('/index')
def index():
     return render_template('index.html')
     


@app.route('/data', methods=['GET'])
def well():
     if request.method == 'GET':
          args = request.args
          well_number = args.get("well")
          connection = get_db_connection()
          cur = connection.cursor()
          cur.execute(f'SELECT * FROM data WHERE well_number = {well_number}')
          rows = cur.fetchall()
          print(rows)
          well_number, oil, gas, brine = rows[0]
          return {'brine':brine, 'gas':gas, 'oil':oil}
     else:
          return render_template('index.html')





if __name__=="__main__":
     create_interg_db()
     app.run(host="127.0.0.1", port=8080, debug=True)


