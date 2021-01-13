from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
import io
import csv
 
app = Flask(__name__)
app.secret_key = "Faisal"
  
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testingdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM employee')
    data = cur.fetchall()
  
    cur.close()
    return render_template('index.html', employee = data)

@app.route('/new_user')
def add_user_view():
	return render_template('add.html')
 
@app.route('/add_contact', methods=['POST'])
def add_user():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur.execute("INSERT INTO employee (name, email, phone) VALUES (%s,%s,%s)", (fullname, email, phone))
        conn.commit()
        flash('Employee Added successfully')
        return redirect(url_for('Index'))
 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM employee WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', employee = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_employee(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE employee
            SET name = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Employee Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))

# @app.route('/search_user', methods=['POST', 'GET'])
# def search_user():
#     conn = mysql.connect()
#     cur = conn.cursor(pymysql.cursors.DictCursor)
#     if request.method == 'POST':
#         id = request.form['id']
#         return redirect('search.html/%s',id)

# @app.route('/search/<id>', methods = ['GET',])
# def show_user(id):
#     conn = mysql.connect()
#     cur = conn.cursor(pymysql.cursors.DictCursor)
  
#     cur.execute('SELECT * FROM employee WHERE id = %s', (id))
#     data = cur.fetchall()
#     cur.close()
#     print(data[0])
#     return render_template('search.html', employee = data[0])

# @app.route('/search/<id>', methods = ['POST', 'GET'])
# def get_userbyid(id):
#     conn = mysql.connect()
#     cur = conn.cursor(pymysql.cursors.DictCursor)
  
#     cur.execute('SELECT * FROM employee WHERE id = %s', (id))
#     data = cur.fetchall()
#     cur.close()
#     print(data[0])
#     return render_template('search.html', employee = data[0])
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM employee WHERE id = {0}'.format(id))
    conn.commit()
    flash('Employee Removed Successfully')
    return redirect(url_for('Index'))

@app.route('/download/report/csv')
def download_report():
 conn = None
 cursor = None
 try:
  conn = mysql.connect()
  cursor = conn.cursor(pymysql.cursors.DictCursor)
   
  cursor.execute("SELECT id, first_name, last_name, designation FROM employees")
  result = cursor.fetchall()
 
  output = io.StringIO()
  writer = csv.writer(output)
   
  line = ['Id, First Name, Last Name, Designation']
  writer.writerow(line)
 
  for row in result:
   line = [str(row['id']) + ',' + row['first_name'] + ',' + row['last_name'] + ',' + row['designation']]
   writer.writerow(line)
 
  output.seek(0)
   
  return response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()
 
# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
# </string:id></id></id>